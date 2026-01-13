"""
Megatron MCP Server - Semantic memory for Claude Code.

Run with: python -m megatron_mcp.mcp_server
"""

import json
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

from .project_memory import ProjectMemory, SessionState, find_project_transcript


class MegatronMCPServer:
    """MCP Server providing semantic memory tools."""

    def __init__(self):
        self.memories: dict[str, ProjectMemory] = {}

    def get_memory(self, project_path: str) -> ProjectMemory:
        """Get or create memory for a project."""
        # Normalize path to prevent cache key collisions (e.g., /foo vs /foo/)
        normalized_path = str(Path(project_path).resolve())
        if normalized_path not in self.memories:
            self.memories[normalized_path] = ProjectMemory(Path(normalized_path))
        return self.memories[normalized_path]

    def handle_request(self, request: dict) -> dict:
        """Handle an MCP request."""
        method = request.get("method", "")
        params = request.get("params", {})
        req_id = request.get("id")

        if method == "initialize":
            return self._initialize(req_id, params)
        elif method == "tools/list":
            return self._list_tools(req_id)
        elif method == "tools/call":
            return self._call_tool(req_id, params)
        else:
            return self._error(req_id, -32601, f"Method not found: {method}")

    def _initialize(self, req_id: Any, params: dict) -> dict:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "megatron-memory", "version": "1.0.0"},
            },
        }

    def _list_tools(self, req_id: Any) -> dict:
        tools = [
            {
                "name": "memory_search",
                "description": "Search project semantic memory for relevant past context. Use when you need to find previous discussions, decisions, or code patterns from past sessions. Supports filtering by memory_type (decision, blocker, preference, error, goal, etc.) and intent (implement, fix, understand, plan, etc.).",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "What to search for (semantic search, not keyword)",
                        },
                        "project_path": {
                            "type": "string",
                            "description": "Project directory path (defaults to cwd)",
                        },
                        "n_results": {
                            "type": "integer",
                            "description": "Number of results (default 5)",
                            "default": 5,
                        },
                        "memory_type": {
                            "type": "string",
                            "description": "Filter by memory type: exchange, decision, preference, constraint, blocker, error, code_context, goal, rationale, remembered",
                            "enum": [
                                "exchange",
                                "decision",
                                "preference",
                                "constraint",
                                "blocker",
                                "error",
                                "code_context",
                                "goal",
                                "rationale",
                                "remembered",
                            ],
                        },
                        "intent": {
                            "type": "string",
                            "description": "Filter by intent: implement, fix, refactor, test, deploy, understand, explore, research, plan, decide, prioritize, resume, status, review, chat",
                            "enum": [
                                "implement",
                                "fix",
                                "refactor",
                                "test",
                                "deploy",
                                "understand",
                                "explore",
                                "research",
                                "plan",
                                "decide",
                                "prioritize",
                                "resume",
                                "status",
                                "review",
                                "chat",
                            ],
                        },
                        "time_after": {
                            "type": "string",
                            "description": "Only return memories after this ISO timestamp (e.g., 2025-01-01T00:00:00)",
                        },
                        "time_before": {
                            "type": "string",
                            "description": "Only return memories before this ISO timestamp",
                        },
                    },
                    "required": ["query"],
                },
            },
            {
                "name": "memory_resume",
                "description": "Get context to resume previous work. Returns last session state, active todos, plan files, and recent exchanges. Use when user says 'resume', 'continue', or 'where were we'.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "project_path": {
                            "type": "string",
                            "description": "Project directory path (defaults to cwd)",
                        }
                    },
                },
            },
            {
                "name": "memory_remember",
                "description": "Explicitly remember something important for future sessions. Use for key decisions, user preferences, important patterns, or anything that should persist.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "content": {
                            "type": "string",
                            "description": "What to remember",
                        },
                        "project_path": {
                            "type": "string",
                            "description": "Project directory path (defaults to cwd)",
                        },
                        "tags": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "Optional tags for categorization",
                        },
                    },
                    "required": ["content"],
                },
            },
            {
                "name": "memory_sync",
                "description": "Sync memory from the current session transcript. Use to ensure latest exchanges are indexed.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "project_path": {
                            "type": "string",
                            "description": "Project directory path (defaults to cwd)",
                        }
                    },
                },
            },
            {
                "name": "memory_stats",
                "description": "Get statistics about project memory - how many chunks indexed, memory location, etc.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "project_path": {
                            "type": "string",
                            "description": "Project directory path (defaults to cwd)",
                        }
                    },
                },
            },
            {
                "name": "memory_forget",
                "description": "Delete memories matching criteria. Use to remove outdated or incorrect context. Supports filtering by session_id or memory_type.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "project_path": {
                            "type": "string",
                            "description": "Project directory path (defaults to cwd)",
                        },
                        "session_id": {
                            "type": "string",
                            "description": "Delete all memories from this session",
                        },
                        "memory_type": {
                            "type": "string",
                            "description": "Delete all memories of this type (e.g., 'live_indexed', 'remembered')",
                        },
                        "before": {
                            "type": "string",
                            "description": "Delete memories before this ISO timestamp",
                        },
                    },
                },
            },
            # Work Stream tools
            {
                "name": "stream_create",
                "description": "Create a new work stream to track progress on a multi-step task. Use when starting a significant piece of work that spans multiple steps or sessions.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name of the work stream (e.g., 'Implement dark mode')",
                        },
                        "tasks": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of tasks to complete",
                        },
                        "project_path": {
                            "type": "string",
                            "description": "Project directory path (defaults to cwd)",
                        },
                    },
                    "required": ["name", "tasks"],
                },
            },
            {
                "name": "stream_status",
                "description": "Get the current status of active work streams. Shows progress and what task is current.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "project_path": {
                            "type": "string",
                            "description": "Project directory path (defaults to cwd)",
                        },
                    },
                },
            },
            {
                "name": "stream_complete",
                "description": "Mark the current task in the active work stream as completed. Automatically advances to the next task.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "project_path": {
                            "type": "string",
                            "description": "Project directory path (defaults to cwd)",
                        },
                        "stream_id": {
                            "type": "string",
                            "description": "Specific stream ID (optional, defaults to active stream)",
                        },
                    },
                },
            },
            {
                "name": "stream_update",
                "description": "Update a work stream - add tasks, jump to a specific task, or change status.",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "stream_id": {
                            "type": "string",
                            "description": "The stream ID to update",
                        },
                        "add_task": {
                            "type": "string",
                            "description": "Add a new task to the stream",
                        },
                        "set_current": {
                            "type": "integer",
                            "description": "Jump to task at this index (0-based)",
                        },
                        "set_status": {
                            "type": "string",
                            "enum": ["active", "paused", "completed"],
                            "description": "Set the stream status",
                        },
                        "project_path": {
                            "type": "string",
                            "description": "Project directory path (defaults to cwd)",
                        },
                    },
                    "required": ["stream_id"],
                },
            },
        ]

        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": tools}}

    def _call_tool(self, req_id: Any, params: dict) -> dict:
        tool_name = params.get("name", "")
        args = params.get("arguments", {})

        try:
            if tool_name == "memory_search":
                result = self._memory_search(args)
            elif tool_name == "memory_resume":
                result = self._memory_resume(args)
            elif tool_name == "memory_remember":
                result = self._memory_remember(args)
            elif tool_name == "memory_sync":
                result = self._memory_sync(args)
            elif tool_name == "memory_stats":
                result = self._memory_stats(args)
            elif tool_name == "memory_forget":
                result = self._memory_forget(args)
            elif tool_name == "stream_create":
                result = self._stream_create(args)
            elif tool_name == "stream_status":
                result = self._stream_status(args)
            elif tool_name == "stream_complete":
                result = self._stream_complete(args)
            elif tool_name == "stream_update":
                result = self._stream_update(args)
            else:
                return self._error(req_id, -32602, f"Unknown tool: {tool_name}")

            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": result}]},
            }
        except Exception as e:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": f"Error: {str(e)}"}],
                    "isError": True,
                },
            }

    def _memory_search(self, args: dict) -> str:
        query = args.get("query", "")
        project_path = args.get("project_path", str(Path.cwd()))
        n_results = min(args.get("n_results", 5), 100)  # Cap at 100 to prevent DoS
        memory_type = args.get("memory_type")
        intent = args.get("intent")
        time_after = args.get("time_after")
        time_before = args.get("time_before")

        memory = self.get_memory(project_path)
        results = memory.query(
            query,
            n_results=n_results,
            memory_type=memory_type,
            intent=intent,
            time_after=time_after,
            time_before=time_before,
        )

        if not results:
            filters_used = []
            if memory_type:
                filters_used.append(f"type={memory_type}")
            if intent:
                filters_used.append(f"intent={intent}")
            filter_str = (
                f" (filters: {', '.join(filters_used)})" if filters_used else ""
            )
            return f"No relevant memories found{filter_str}."

        # Build header with active filters
        header_parts = [f"# Memory Search: '{query}'"]
        if memory_type or intent or time_after or time_before:
            filters = []
            if memory_type:
                filters.append(f"type={memory_type}")
            if intent:
                filters.append(f"intent={intent}")
            if time_after:
                filters.append(f"after={time_after}")
            if time_before:
                filters.append(f"before={time_before}")
            header_parts.append(f"*Filters: {', '.join(filters)}*")
        header_parts.append("")

        output = header_parts
        for i, result in enumerate(results, 1):
            meta = result.get("metadata", {})
            type_badge = (
                f"[{meta.get('memory_type', 'exchange')}]"
                if meta.get("memory_type")
                else ""
            )
            output.append(
                f"## Result {i} {type_badge} (relevance: {result['score']:.2f})"
            )
            content = result.get("content") or "(no content)"
            output.append(content)
            output.append("")

        return "\n".join(output)

    def _memory_resume(self, args: dict) -> str:
        project_path = args.get("project_path", str(Path.cwd()))
        memory = self.get_memory(project_path)
        return memory.get_resume_context()

    def _memory_remember(self, args: dict) -> str:
        content = args.get("content", "")
        project_path = args.get("project_path", str(Path.cwd()))
        tags = args.get("tags", [])

        if not content:
            return "Error: No content provided to remember."

        memory = self.get_memory(project_path)

        # Create a special "remembered" chunk
        from .chunker import Chunk

        chunk = Chunk(
            id=f"remembered:{uuid.uuid4().hex[:8]}:{datetime.now().isoformat()}",
            content=f"[REMEMBERED] {content}",
            session_id="manual",
            timestamp=datetime.now().isoformat(),
            metadata={
                "type": "remembered",
                "tags": ",".join(tags) if tags else "",
            },
        )

        memory.index_chunk(chunk)
        return f"✓ Remembered: {content[:100]}{'...' if len(content) > 100 else ''}"

    def _memory_sync(self, args: dict) -> str:
        project_path = args.get("project_path", str(Path.cwd()))
        memory = self.get_memory(project_path)

        transcript = find_project_transcript(Path(project_path))
        if not transcript:
            return "No transcript found for this project."

        count = memory.index_transcript(transcript)
        return f"Synced {count} chunks from current session."

    def _memory_stats(self, args: dict) -> str:
        project_path = args.get("project_path", str(Path.cwd()))
        memory = self.get_memory(project_path)
        stats = memory.get_stats()

        return f"""# Memory Stats

**Project:** {stats["project"]}
**Indexed Chunks:** {stats["total_chunks"]}
**Memory Path:** {stats["memory_path"]}
"""

    def _memory_forget(self, args: dict) -> str:
        project_path = args.get("project_path", str(Path.cwd()))
        session_id = args.get("session_id")
        memory_type = args.get("memory_type")
        before = args.get("before")

        if not session_id and not memory_type and not before:
            return "Error: Must provide at least one filter (session_id, memory_type, or before)"

        memory = self.get_memory(project_path)
        deleted = memory.forget(
            session_id=session_id, memory_type=memory_type, before=before
        )

        return f"✓ Deleted {deleted} memories"

    # ===== Work Stream Tools =====

    def _stream_create(self, args: dict) -> str:
        name = args.get("name", "")
        tasks = args.get("tasks", [])
        project_path = args.get("project_path", str(Path.cwd()))

        if not name:
            return "Error: Stream name is required"
        if not tasks:
            return "Error: At least one task is required"

        memory = self.get_memory(project_path)
        stream = memory.create_work_stream(name, tasks)

        output = [f"# Work Stream Created: {stream.name}\n"]
        output.append(f"**ID:** `{stream.id}`\n")
        output.append("**Tasks:**")
        output.append(stream.get_progress_display())

        return "\n".join(output)

    def _stream_status(self, args: dict) -> str:
        project_path = args.get("project_path", str(Path.cwd()))
        memory = self.get_memory(project_path)

        streams = memory.get_work_streams()
        if not streams:
            return "No work streams found."

        output = ["# Work Streams\n"]

        for stream in streams:
            status_icon = (
                "🟢"
                if stream.status == "active"
                else "⏸️"
                if stream.status == "paused"
                else "✅"
            )
            output.append(f"## {status_icon} {stream.name}")
            output.append(f"*ID: `{stream.id}` | Status: {stream.status}*\n")
            output.append(stream.get_progress_display())
            output.append("")

        return "\n".join(output)

    def _stream_complete(self, args: dict) -> str:
        project_path = args.get("project_path", str(Path.cwd()))
        stream_id = args.get("stream_id")

        memory = self.get_memory(project_path)
        stream = memory.complete_current_task(stream_id)

        if not stream:
            return "Error: No active stream or task to complete"

        current = stream.get_current_task()
        if current:
            return f"✓ Task completed. Now on: **{current.content}**\n\n{stream.get_progress_display()}"
        else:
            return f"✓ All tasks completed! Work stream '{stream.name}' is done.\n\n{stream.get_progress_display()}"

    def _stream_update(self, args: dict) -> str:
        stream_id = args.get("stream_id", "")
        project_path = args.get("project_path", str(Path.cwd()))

        if not stream_id:
            return "Error: stream_id is required"

        memory = self.get_memory(project_path)

        stream = memory.update_work_stream(
            stream_id=stream_id,
            add_task=args.get("add_task"),
            set_current=args.get("set_current"),
            set_status=args.get("set_status"),
        )

        if not stream:
            return f"Error: Stream '{stream_id}' not found"

        output = [f"# Updated: {stream.name}\n"]
        output.append(stream.get_progress_display())

        return "\n".join(output)

    def _error(self, req_id: Any, code: int, message: str) -> dict:
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "error": {"code": code, "message": message},
        }

    def run(self):
        """Run the MCP server on stdio."""
        while True:
            try:
                line = sys.stdin.readline()
                if not line:
                    break

                request = json.loads(line)
                response = self.handle_request(request)

                sys.stdout.write(json.dumps(response) + "\n")
                sys.stdout.flush()

            except json.JSONDecodeError:
                continue
            except KeyboardInterrupt:
                break


def main():
    server = MegatronMCPServer()
    server.run()


if __name__ == "__main__":
    main()
