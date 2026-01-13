"""Project-local memory - the Megatron core."""

import fcntl
import json
import os
import tempfile
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

import chromadb
from chromadb.config import Settings

from .chunker import Chunk, chunk_by_exchange
from .parser import Message, parse_transcript


@dataclass
class WorkStreamTask:
    """A single task within a work stream."""

    id: str
    content: str
    status: str  # pending | in_progress | completed | blocked
    created_at: str
    completed_at: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "content": self.content,
            "status": self.status,
            "created_at": self.created_at,
            "completed_at": self.completed_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "WorkStreamTask":
        return cls(
            id=data["id"],
            content=data["content"],
            status=data["status"],
            created_at=data["created_at"],
            completed_at=data.get("completed_at"),
        )


@dataclass
class WorkStream:
    """A structured work stream with tracked progress."""

    id: str
    name: str
    tasks: list[WorkStreamTask]
    current_task_index: int  # Which task is active (-1 if none)
    status: str  # active | paused | completed
    created_at: str
    updated_at: str

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "tasks": [t.to_dict() for t in self.tasks],
            "current_task_index": self.current_task_index,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "WorkStream":
        return cls(
            id=data["id"],
            name=data["name"],
            tasks=[WorkStreamTask.from_dict(t) for t in data.get("tasks", [])],
            current_task_index=data.get("current_task_index", -1),
            status=data.get("status", "active"),
            created_at=data["created_at"],
            updated_at=data["updated_at"],
        )

    def get_current_task(self) -> Optional[WorkStreamTask]:
        """Get the currently active task."""
        if 0 <= self.current_task_index < len(self.tasks):
            return self.tasks[self.current_task_index]
        return None

    def get_progress_display(self) -> str:
        """Generate a progress display string."""
        lines = []
        for i, task in enumerate(self.tasks):
            if task.status == "completed":
                icon = "✅"
            elif task.status == "in_progress" or i == self.current_task_index:
                icon = "⏳"
            elif task.status == "blocked":
                icon = "🚫"
            else:
                icon = "○"

            marker = " ← YOU ARE HERE" if i == self.current_task_index else ""
            lines.append(f"{icon} {task.content}{marker}")
        return "\n".join(lines)


@dataclass
class SessionState:
    session_id: str
    timestamp: str
    cwd: str
    last_exchanges: list[dict]  # Recent conversation chunks
    active_todos: list[dict]  # Current todo items
    plan_files: dict[str, str]  # path -> content of active plan files
    in_progress: str  # What was being worked on
    last_error: Optional[str]  # Any recent error/blocker
    decisions: list[dict] = None  # Key decisions made
    blockers: list[dict] = None  # Things blocking progress
    work_streams: list[dict] = None  # Active work streams

    def __post_init__(self):
        if self.decisions is None:
            self.decisions = []
        if self.blockers is None:
            self.blockers = []
        if self.work_streams is None:
            self.work_streams = []


class ProjectMemory:
    """
    Project-local semantic memory.

    Each project gets its own:
    - Vector index (ChromaDB)
    - State snapshots
    - Isolated context
    """

    MEMORY_DIR = ".megatron"

    def __init__(self, project_path: Path):
        self.project_path = Path(project_path).resolve()
        self.memory_path = self.project_path / self.MEMORY_DIR
        self.memory_path.mkdir(parents=True, exist_ok=True)

        # Project-local ChromaDB
        self.client = chromadb.PersistentClient(
            path=str(self.memory_path / "index"),
            settings=Settings(anonymized_telemetry=False),
        )
        self.collection = self.client.get_or_create_collection(
            name="project_memory",
            metadata={"hnsw:space": "cosine"},
        )

    def index_chunk(self, chunk: Chunk) -> None:
        """Index a single chunk immediately (for live indexing)."""
        self.collection.upsert(
            ids=[chunk.id],
            documents=[chunk.content],
            metadatas=[
                {
                    "session_id": chunk.session_id,
                    "timestamp": chunk.timestamp,
                    **chunk.metadata,
                }
            ],
        )

    def index_transcript(self, transcript_path: Path) -> int:
        """Index a full transcript file."""
        messages = list(parse_transcript(transcript_path))
        if not messages:
            return 0

        chunks = chunk_by_exchange(messages)
        for chunk in chunks:
            self.index_chunk(chunk)

        return len(chunks)

    def query(
        self,
        query: str,
        n_results: int = 5,
        memory_type: Optional[str] = None,
        intent: Optional[str] = None,
        time_after: Optional[str] = None,
        time_before: Optional[str] = None,
    ) -> list[dict]:
        """
        Query project memory with optional filters.

        Args:
            query: Semantic search query
            n_results: Number of results to return
            memory_type: Filter by memory type (decision, blocker, preference, etc.)
            intent: Filter by intent (implement, fix, understand, etc.)
            time_after: Only return memories after this ISO timestamp
            time_before: Only return memories before this ISO timestamp
        """
        # Build where clause for ChromaDB filters
        where = None
        where_clauses = []

        if memory_type:
            where_clauses.append({"memory_type": memory_type})
        if intent:
            where_clauses.append({"intent": intent})

        if len(where_clauses) == 1:
            where = where_clauses[0]
        elif len(where_clauses) > 1:
            where = {"$and": where_clauses}

        results = self.collection.query(
            query_texts=[query],
            n_results=n_results * 2 if (time_after or time_before) else n_results,
            where=where,
            include=["documents", "metadatas", "distances"],
        )

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        results_list = [
            {
                "content": doc,
                "score": 1 - dist,
                "metadata": meta,
            }
            for doc, meta, dist in zip(documents, metadatas, distances)
        ]

        # Apply timestamp filters (ChromaDB doesn't support timestamp comparison in where)
        if time_after or time_before:
            # Parse filter timestamps once
            try:
                time_after_dt = datetime.fromisoformat(time_after.replace("Z", "+00:00")) if time_after else None
            except ValueError:
                time_after_dt = None
            try:
                time_before_dt = datetime.fromisoformat(time_before.replace("Z", "+00:00")) if time_before else None
            except ValueError:
                time_before_dt = None

            filtered = []
            for r in results_list:
                ts = r["metadata"].get("timestamp", "")
                if not ts:
                    continue
                try:
                    ts_dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                except ValueError:
                    continue  # Skip entries with invalid timestamps
                if time_after_dt and ts_dt < time_after_dt:
                    continue
                if time_before_dt and ts_dt > time_before_dt:
                    continue
                filtered.append(r)
            results_list = filtered[:n_results]

        return results_list

    def save_state(self, state: SessionState) -> None:
        """Save session state for resume capability using atomic write."""
        state_file = self.memory_path / "state.json"

        # Write to temp file first, then atomic rename
        fd, tmp_path = tempfile.mkstemp(
            dir=self.memory_path,
            prefix=".state_",
            suffix=".tmp"
        )
        try:
            with os.fdopen(fd, "w") as f:
                # Acquire exclusive lock during write
                fcntl.flock(f.fileno(), fcntl.LOCK_EX)
                try:
                    json.dump(asdict(state), f, indent=2)
                    f.flush()
                    os.fsync(f.fileno())
                finally:
                    fcntl.flock(f.fileno(), fcntl.LOCK_UN)
            # Atomic rename
            os.rename(tmp_path, state_file)
        except Exception:
            # Clean up temp file on error
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
            raise

    def load_state(self) -> Optional[SessionState]:
        """Load the last session state."""
        state_file = self.memory_path / "state.json"
        if not state_file.exists():
            return None

        with open(state_file, "r") as f:
            data = json.load(f)
            return SessionState(**data)

    def extract_and_save_state(self, transcript_path: Path) -> Optional[SessionState]:
        """
        Extract session state from transcript and save it.

        This captures:
        - The last few exchanges (actual conversation content)
        - What was being worked on (extracted from context)
        - Key decisions made
        - Blockers encountered
        - Session metadata
        """
        messages = list(parse_transcript(transcript_path))
        if not messages:
            return None

        # Get session info from the last message
        last_msg = messages[-1]
        session_id = last_msg.session_id
        timestamp = last_msg.timestamp

        # Get the last N exchanges (user + assistant pairs)
        last_exchanges = self._extract_last_exchanges(messages, n_exchanges=5)

        # Extract what was being worked on from recent conversation
        in_progress = self._extract_focus(messages)

        # Look for any todo patterns in recent messages
        active_todos = self._extract_todos(messages)

        # Check for plan files
        plan_files = self._find_plan_files()

        # Check for errors/blockers in recent messages
        last_error = self._extract_last_error(messages)

        # Extract decisions made during the session
        decisions = self._extract_decisions(messages)

        # Extract blockers mentioned
        blockers = self._extract_blockers(messages)

        state = SessionState(
            session_id=session_id,
            timestamp=timestamp,
            cwd=str(self.project_path),
            last_exchanges=last_exchanges,
            active_todos=active_todos,
            plan_files=plan_files,
            in_progress=in_progress,
            last_error=last_error,
            decisions=decisions,
            blockers=blockers,
        )

        self.save_state(state)
        return state

    def _extract_last_exchanges(
        self, messages: list[Message], n_exchanges: int = 5
    ) -> list[dict]:
        """Extract the last N user-assistant exchanges."""
        exchanges = []
        current_exchange = {}

        for msg in messages:
            if msg.role == "user":
                # Start new exchange
                if current_exchange:
                    exchanges.append(current_exchange)
                current_exchange = {
                    "user": msg.content,
                    "assistant": "",
                    "timestamp": msg.timestamp,
                }
            elif msg.role == "assistant" and current_exchange:
                # Add to current exchange (concatenate if multiple assistant messages)
                if current_exchange["assistant"]:
                    current_exchange["assistant"] += "\n" + msg.content
                else:
                    current_exchange["assistant"] = msg.content

        # Don't forget the last exchange
        if current_exchange:
            exchanges.append(current_exchange)

        # Return last N exchanges
        return exchanges[-n_exchanges:]

    def _extract_focus(self, messages: list[Message]) -> str:
        """
        Extract what was being worked on from recent messages.

        Looks for patterns like:
        - Recent user requests
        - TodoWrite tool usage
        - Explicit statements about current work
        """
        # Get the last few user messages to understand focus
        user_messages = [m for m in messages if m.role == "user"][-5:]

        if not user_messages:
            return ""

        # The most recent substantial user message is likely the current focus
        for msg in reversed(user_messages):
            content = msg.content.strip()
            # Skip very short messages (like "yes", "ok", "continue")
            if len(content) > 20 and not content.startswith("<"):
                # Truncate if too long
                if len(content) > 200:
                    return content[:200] + "..."
                return content

        return ""

    def _extract_todos(self, messages: list[Message]) -> list[dict]:
        """Extract any todo items mentioned in recent messages."""
        todos = []

        # Look for TodoWrite patterns in assistant messages
        for msg in reversed(messages[-20:]):
            if msg.role == "assistant" and "todo" in msg.content.lower():
                # Try to extract todo items (simple pattern matching)
                lines = msg.content.split("\n")
                for line in lines:
                    line = line.strip()
                    # Look for checkbox patterns
                    if line.startswith("- [ ]"):
                        todos.append({"content": line[5:].strip(), "status": "pending"})
                    elif line.startswith("- [x]"):
                        todos.append(
                            {"content": line[5:].strip(), "status": "completed"}
                        )
                    elif "in_progress" in line.lower() or "in progress" in line.lower():
                        # Try to extract the task
                        if "]" in line:
                            task = line.split("]", 1)[-1].strip()
                            if task:
                                todos.append({"content": task, "status": "in_progress"})

                if todos:
                    break  # Use the most recent todo list found

        return todos

    def _find_plan_files(self) -> dict[str, str]:
        """Find any active plan files in the project."""
        plan_files = {}

        # Check common plan file locations
        plan_paths = [
            self.project_path / "plan.md",
            self.project_path / ".claude" / "plan.md",
            self.project_path / "PLAN.md",
        ]

        # Also check .artifacts for Harness plans
        artifacts_dir = self.project_path / ".artifacts"
        if artifacts_dir.exists():
            for plan_file in artifacts_dir.glob("*/plan.md"):
                plan_paths.append(plan_file)

        for path in plan_paths:
            if path.exists():
                try:
                    content = path.read_text()
                    # Only include if it has content
                    if content.strip():
                        plan_files[str(path.relative_to(self.project_path))] = content
                except Exception:
                    continue

        return plan_files

    def _extract_last_error(self, messages: list[Message]) -> Optional[str]:
        """Look for recent errors or blockers in the conversation."""
        error_keywords = [
            "error",
            "failed",
            "exception",
            "traceback",
            "cannot",
            "unable",
        ]

        for msg in reversed(messages[-10:]):
            content_lower = msg.content.lower()
            for keyword in error_keywords:
                if keyword in content_lower:
                    # Found a potential error - extract relevant part
                    lines = msg.content.split("\n")
                    for line in lines:
                        if any(kw in line.lower() for kw in error_keywords):
                            return line[:200]  # Truncate if needed

        return None

    def _extract_decisions(self, messages: list[Message]) -> list[dict]:
        """
        Extract decisions made during the conversation.

        Looks for patterns like:
        - "let's go with X"
        - "we decided to X"
        - "we'll use X"
        - "going with X"
        - "the decision is X"
        """
        decisions = []
        decision_patterns = [
            "let's go with",
            "let's use",
            "we decided",
            "we'll use",
            "we'll go with",
            "going with",
            "the decision is",
            "decided to",
            "choosing",
            "we chose",
            "settled on",
            "the approach is",
            "the plan is",
        ]

        for msg in messages[-30:]:  # Look at recent messages
            content_lower = msg.content.lower()
            for pattern in decision_patterns:
                if pattern in content_lower:
                    # Extract the sentence containing the decision
                    lines = msg.content.split("\n")
                    for line in lines:
                        if pattern in line.lower():
                            # Clean up the line
                            decision_text = line.strip()
                            if len(decision_text) > 20:  # Skip very short matches
                                decisions.append(
                                    {
                                        "content": decision_text[:300],
                                        "timestamp": msg.timestamp,
                                        "role": msg.role,
                                    }
                                )
                                break
                    break  # One decision per message max

        # Deduplicate and return most recent
        seen = set()
        unique_decisions = []
        for d in reversed(decisions):
            key = d["content"][:50].lower()
            if key not in seen:
                seen.add(key)
                unique_decisions.append(d)

        return list(reversed(unique_decisions[-5:]))  # Last 5 unique decisions

    def _extract_blockers(self, messages: list[Message]) -> list[dict]:
        """
        Extract blockers mentioned in the conversation.

        Looks for patterns like:
        - "blocked on X"
        - "can't do X until Y"
        - "waiting on X"
        - "need X before"
        - "depends on X"
        """
        blockers = []
        blocker_patterns = [
            "blocked on",
            "blocked by",
            "can't do .* until",
            "cannot .* until",
            "waiting on",
            "waiting for",
            "need .* before",
            "needs .* first",
            "depends on",
            "dependent on",
            "prerequisite",
            "have to .* first",
            "gotta .* first",
            "stuck on",
            "stuck at",
        ]

        import re

        for msg in messages[-20:]:
            content_lower = msg.content.lower()
            for pattern in blocker_patterns:
                if re.search(pattern, content_lower):
                    # Extract the sentence containing the blocker
                    lines = msg.content.split("\n")
                    for line in lines:
                        if re.search(pattern, line.lower()):
                            blocker_text = line.strip()
                            if len(blocker_text) > 15:
                                blockers.append(
                                    {
                                        "content": blocker_text[:300],
                                        "timestamp": msg.timestamp,
                                        "role": msg.role,
                                    }
                                )
                                break
                    break

        # Return unique blockers
        seen = set()
        unique_blockers = []
        for b in blockers:
            key = b["content"][:50].lower()
            if key not in seen:
                seen.add(key)
                unique_blockers.append(b)

        return unique_blockers[-3:]  # Last 3 blockers

    def _get_harness_state(self) -> list[dict]:
        """Check for active Harness features in .artifacts/."""
        artifacts_dir = self.project_path / ".artifacts"
        if not artifacts_dir.exists():
            return []

        features = []
        for progress_file in artifacts_dir.glob("*/progress.md"):
            feature_slug = progress_file.parent.name
            try:
                content = progress_file.read_text()
                # Extract phase from content
                phase = "unknown"
                phase_line = None
                for line in content.split("\n"):
                    if line.startswith("Phase:"):
                        phase_line = line.replace("Phase:", "").strip()
                        break
                    # Also check for checkbox format
                    if "- [ ]" in line and "Phase" in line:
                        # This is the next incomplete phase
                        phase = (
                            line.split("Phase")[1].split(":")[0].strip()
                            if "Phase" in line
                            else "unknown"
                        )
                        break
                    if "- [x]" in line and "Phase" in line:
                        # Track the last completed phase
                        phase = (
                            line.split("Phase")[1].split(":")[0].strip()
                            if "Phase" in line
                            else "unknown"
                        )

                features.append(
                    {
                        "slug": feature_slug,
                        "phase": phase_line or phase,
                        "path": str(progress_file),
                    }
                )
            except Exception:
                continue

        return features

    def get_resume_context(self, n_recent: int = 3) -> str:
        """
        Get context for resuming work.

        Priority order:
        1. Active work streams (structured progress tracking)
        2. Last session state (actual exchanges, focus, todos, decisions, blockers)
        3. Harness feature state (structured workflows)
        4. Falls back to semantic search if no state saved
        """
        parts = ["# Resume Context\n"]

        # Check for active work streams first - this is the primary progress indicator
        active_stream = self.get_active_stream()
        if active_stream:
            parts.append(f"## Active Work Stream: {active_stream.name}")
            parts.append(f"*Updated: {active_stream.updated_at}*\n")
            parts.append("**Progress:**")
            parts.append(active_stream.get_progress_display())
            parts.append("")

        # Load last saved state
        state = self.load_state()
        if state:
            parts.append("## Last Session")
            parts.append(f"*{state.timestamp}*\n")

            if state.in_progress:
                parts.append(f"**Working on:** {state.in_progress}\n")

            # Show blockers prominently at the top
            blockers = getattr(state, "blockers", []) or []
            if blockers:
                parts.append("**⚠️ Blockers:**")
                for blocker in blockers:
                    parts.append(f"  - {blocker.get('content', '')}")
                parts.append("")

            if state.active_todos:
                parts.append("**Progress:**")
                for todo in state.active_todos:
                    status = todo.get("status", "pending")
                    icon = (
                        "⏳"
                        if status == "in_progress"
                        else "○"
                        if status == "pending"
                        else "✅"
                    )
                    parts.append(f"  {icon} {todo.get('content', '')}")
                parts.append("")

            # Show key decisions
            decisions = getattr(state, "decisions", []) or []
            if decisions:
                parts.append("**Key Decisions:**")
                for decision in decisions:
                    parts.append(f"  • {decision.get('content', '')}")
                parts.append("")

            if state.last_error:
                parts.append(f"**Last Error:** {state.last_error}\n")

            # Show actual last exchanges from the session
            if state.last_exchanges:
                parts.append("**Recent Conversation:**\n")
                for i, exchange in enumerate(state.last_exchanges[-n_recent:], 1):
                    parts.append(f"### Exchange {i}")
                    user_content = exchange.get("user", "")
                    if len(user_content) > 300:
                        user_content = user_content[:300] + "..."
                    parts.append(f"**User:** {user_content}")

                    assistant_content = exchange.get("assistant", "")
                    if len(assistant_content) > 500:
                        assistant_content = assistant_content[:500] + "..."
                    parts.append(f"**Assistant:** {assistant_content}\n")
                parts.append("")

            if state.plan_files:
                parts.append("**Active Plans:**")
                for path, content in state.plan_files.items():
                    parts.append(f"\n### {path}")
                    if len(content) > 1000:
                        content = content[:1000] + "\n...(truncated)"
                    parts.append(f"```\n{content}\n```")
                parts.append("")

        # Check Harness state for structured workflows
        harness_features = self._get_harness_state()
        if harness_features:
            parts.append("## Active Harness Features\n")
            for feature in harness_features:
                parts.append(f"- **{feature['slug']}** - Phase {feature['phase']}")
                parts.append(
                    f"  Resume with: `/harness:orchestrator {feature['slug']}`"
                )
            parts.append("")

        # If no state saved, fall back to semantic search
        if not state:
            parts.append("## Recent Context (from semantic search)\n")
            parts.append(
                "*No session state saved. Showing semantically similar exchanges.*\n"
            )
            recent = self.query("recent work progress tasks", n_results=n_recent)
            if recent:
                for i, result in enumerate(recent, 1):
                    parts.append(f"### Exchange {i} (relevance: {result['score']:.2f})")
                    content = result["content"]
                    if len(content) > 800:
                        content = content[:800] + "\n...(truncated)"
                    parts.append(content)
                    parts.append("")
            else:
                parts.append("*No memory indexed yet.*\n")

        parts.append("---")
        return "\n".join(parts)

    # ===== Work Stream Management =====

    def get_work_streams(self) -> list[WorkStream]:
        """Get all work streams from current state."""
        state = self.load_state()
        if not state or not state.work_streams:
            return []
        return [WorkStream.from_dict(ws) for ws in state.work_streams]

    def get_active_stream(self) -> Optional[WorkStream]:
        """Get the currently active work stream."""
        streams = self.get_work_streams()
        for stream in streams:
            if stream.status == "active":
                return stream
        return None

    def create_work_stream(self, name: str, tasks: list[str]) -> WorkStream:
        """Create a new work stream with the given tasks."""
        now = datetime.now().isoformat()
        stream_id = f"ws-{uuid.uuid4().hex[:8]}"

        stream_tasks = [
            WorkStreamTask(
                id=f"task-{i}",
                content=task,
                status="pending" if i > 0 else "in_progress",
                created_at=now,
            )
            for i, task in enumerate(tasks)
        ]

        stream = WorkStream(
            id=stream_id,
            name=name,
            tasks=stream_tasks,
            current_task_index=0 if tasks else -1,
            status="active",
            created_at=now,
            updated_at=now,
        )

        # Mark first task as in_progress
        if stream.tasks:
            stream.tasks[0].status = "in_progress"

        # Save to state
        state = self.load_state()
        if not state:
            # Create minimal state if none exists
            state = SessionState(
                session_id="",
                timestamp=now,
                cwd=str(self.project_path),
                last_exchanges=[],
                active_todos=[],
                plan_files={},
                in_progress="",
                last_error=None,
            )

        # Pause any existing active streams
        for ws_dict in state.work_streams:
            if ws_dict.get("status") == "active":
                ws_dict["status"] = "paused"
        state.work_streams.append(stream.to_dict())
        self.save_state(state)

        return stream

    def update_work_stream(
        self,
        stream_id: str,
        complete_task: Optional[int] = None,
        set_current: Optional[int] = None,
        add_task: Optional[str] = None,
        set_status: Optional[str] = None,
    ) -> Optional[WorkStream]:
        """Update a work stream."""
        state = self.load_state()
        if not state:
            return None

        now = datetime.now().isoformat()

        for i, ws_dict in enumerate(state.work_streams):
            if ws_dict.get("id") == stream_id:
                stream = WorkStream.from_dict(ws_dict)

                # Complete a task
                if complete_task is not None and 0 <= complete_task < len(stream.tasks):
                    stream.tasks[complete_task].status = "completed"
                    stream.tasks[complete_task].completed_at = now

                    # Auto-advance to next pending task
                    for j, task in enumerate(stream.tasks):
                        if task.status == "pending":
                            stream.current_task_index = j
                            stream.tasks[j].status = "in_progress"
                            break
                    else:
                        # All tasks complete
                        stream.current_task_index = -1
                        stream.status = "completed"

                # Set current task manually
                if set_current is not None and 0 <= set_current < len(stream.tasks):
                    # Mark old current as pending (if not completed)
                    if stream.current_task_index >= 0:
                        old_task = stream.tasks[stream.current_task_index]
                        if old_task.status == "in_progress":
                            old_task.status = "pending"

                    stream.current_task_index = set_current
                    stream.tasks[set_current].status = "in_progress"

                # Add a new task
                if add_task:
                    new_task = WorkStreamTask(
                        id=f"task-{len(stream.tasks)}",
                        content=add_task,
                        status="pending",
                        created_at=now,
                    )
                    stream.tasks.append(new_task)

                # Set stream status
                if set_status in ("active", "paused", "completed"):
                    stream.status = set_status

                stream.updated_at = now
                state.work_streams[i] = stream.to_dict()
                self.save_state(state)
                return stream

        return None

    def complete_current_task(
        self, stream_id: Optional[str] = None
    ) -> Optional[WorkStream]:
        """Complete the current task in the active (or specified) stream."""
        if stream_id:
            streams = self.get_work_streams()
            stream = next((s for s in streams if s.id == stream_id), None)
        else:
            stream = self.get_active_stream()

        if not stream or stream.current_task_index < 0:
            return None

        return self.update_work_stream(
            stream.id, complete_task=stream.current_task_index
        )

    def get_stats(self) -> dict:
        """Get memory statistics."""
        return {
            "project": str(self.project_path),
            "total_chunks": self.collection.count(),
            "memory_path": str(self.memory_path),
        }

    def forget(
        self,
        session_id: Optional[str] = None,
        memory_type: Optional[str] = None,
        before: Optional[str] = None,
    ) -> int:
        """
        Delete memories matching criteria.

        AMP spec: memory/forget operation.
        Returns count of deleted chunks.
        """
        # Build where clause for ChromaDB
        where_clauses = []

        if session_id:
            where_clauses.append({"session_id": session_id})

        if memory_type:
            where_clauses.append({"type": memory_type})

        # ChromaDB doesn't support timestamp comparison directly,
        # so we need to query first then filter
        if not where_clauses and not before:
            return 0

        # Build the where filter
        if len(where_clauses) == 1:
            where = where_clauses[0]
        elif len(where_clauses) > 1:
            where = {"$and": where_clauses}
        else:
            where = None

        try:
            # Get matching IDs
            if where:
                results = self.collection.get(where=where, include=["metadatas"])
            else:
                results = self.collection.get(include=["metadatas"])

            ids_to_delete = results.get("ids", [])
            metadatas = results.get("metadatas", [])

            # Filter by timestamp if 'before' is specified
            if before and ids_to_delete:
                try:
                    before_dt = datetime.fromisoformat(before.replace("Z", "+00:00"))
                except ValueError:
                    before_dt = None

                if before_dt:
                    filtered_ids = []
                    for id_, meta in zip(ids_to_delete, metadatas):
                        timestamp = meta.get("timestamp", "")
                        if not timestamp:
                            continue
                        try:
                            ts_dt = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
                            if ts_dt < before_dt:
                                filtered_ids.append(id_)
                        except ValueError:
                            continue  # Skip entries with invalid timestamps
                    ids_to_delete = filtered_ids

            if not ids_to_delete:
                return 0

            # Delete the chunks
            self.collection.delete(ids=ids_to_delete)
            return len(ids_to_delete)

        except Exception as e:
            # Don't crash on delete errors
            return 0


def get_project_memory(cwd: Optional[Path] = None) -> ProjectMemory:
    """Get or create project memory for the current/specified directory."""
    if cwd is None:
        cwd = Path.cwd()
    return ProjectMemory(cwd)


def find_project_transcript(project_path: Path) -> Optional[Path]:
    """Find the most recent transcript for a project."""
    claude_projects = Path.home() / ".claude" / "projects"
    if not claude_projects.exists():
        return None

    project_path = Path(project_path).resolve()

    # Try exact match first, then parent directories
    paths_to_try = [project_path]

    # Add parent paths up to home
    current = project_path
    while current != current.parent and current != Path.home():
        current = current.parent
        paths_to_try.append(current)

    for path in paths_to_try:
        # Encode path the way Claude does (replace / with -)
        encoded = str(path).replace("/", "-")
        project_transcript_dir = claude_projects / encoded

        if project_transcript_dir.exists():
            transcripts = list(project_transcript_dir.glob("*.jsonl"))
            if transcripts:
                return max(transcripts, key=lambda p: p.stat().st_mtime)

    return None
