"""
Megatron Understanding Layer

Phase 2 of the architecture: Extract higher-level understanding from events.
- Intent detection: What is the user trying to accomplish?
- Pattern recognition: What behaviors repeat across sessions?
- Memory type classification: decision, preference, blocker, goal, etc.
"""

import re
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Intent(Enum):
    """User intent categories."""

    # Action intents
    IMPLEMENT = "implement"  # Build/create something
    FIX = "fix"  # Fix a bug or issue
    REFACTOR = "refactor"  # Improve existing code
    TEST = "test"  # Write or run tests
    DEPLOY = "deploy"  # Deploy or release

    # Information intents
    UNDERSTAND = "understand"  # Learn how something works
    EXPLORE = "explore"  # Browse/search codebase
    RESEARCH = "research"  # Look up external info

    # Planning intents
    PLAN = "plan"  # Design or architect
    DECIDE = "decide"  # Make a decision
    PRIORITIZE = "prioritize"  # Order tasks

    # Session intents
    RESUME = "resume"  # Continue previous work
    STATUS = "status"  # Check progress
    REVIEW = "review"  # Review code/work

    # Other
    CHAT = "chat"  # Casual conversation
    UNKNOWN = "unknown"  # Can't determine


class MemoryType(Enum):
    """Memory type categories per AMP spec."""

    EXCHANGE = "exchange"  # Standard conversation
    DECISION = "decision"  # A decision was made
    PREFERENCE = "preference"  # User preference
    CONSTRAINT = "constraint"  # Technical constraint
    BLOCKER = "blocker"  # Something blocking progress
    ERROR = "error"  # Error encountered
    CODE_CONTEXT = "code_context"  # Code-specific context
    GOAL = "goal"  # What we're trying to achieve
    RATIONALE = "rationale"  # Why something was done
    REMEMBERED = "remembered"  # Explicitly remembered


@dataclass
class ExtractedIntent:
    """Result of intent extraction."""

    intent: Intent
    confidence: float  # 0-1
    topic: str  # What the intent is about
    goal: str  # The specific goal/objective
    keywords: list[str]  # Key terms extracted


@dataclass
class ExtractedUnderstanding:
    """Full understanding extracted from a message."""

    intent: ExtractedIntent
    memory_type: MemoryType
    decisions: list[str]  # Any decisions made
    blockers: list[str]  # Any blockers mentioned
    questions: list[str]  # Questions asked
    entities: list[str]  # Files, functions, concepts mentioned


# Intent detection patterns
INTENT_PATTERNS = {
    Intent.IMPLEMENT: [
        r"\b(implement|add|create|build|make|write|develop)\b",
        r"\b(new feature|add feature|build out)\b",
        r"let's (build|create|add|implement)",
    ],
    Intent.FIX: [
        r"\b(fix|debug|solve|resolve|repair)\b",
        r"\b(bug|error|issue|problem|broken)\b",
        r"(doesn't|does not|isn't|is not) (work|working)",
    ],
    Intent.REFACTOR: [
        r"\b(refactor|clean up|improve|optimize|simplify)\b",
        r"\b(restructure|reorganize|rewrite)\b",
    ],
    Intent.TEST: [
        r"\b(test|spec|coverage)\b",
        r"\b(write tests|run tests|add tests)\b",
    ],
    Intent.UNDERSTAND: [
        r"\b(how does|what is|explain|understand|tell me about)\b",
        r"\b(what\'s|where is|where are|show me)\b",
        r"\?$",  # Ends with question mark
    ],
    Intent.EXPLORE: [
        r"\b(find|search|look for|locate|grep)\b",
        r"\b(where|which files|what files)\b",
    ],
    Intent.RESEARCH: [
        r"\b(research|look up|check docs|best practice)\b",
        r"\b(how do others|what\'s the standard)\b",
    ],
    Intent.PLAN: [
        r"\b(plan|design|architect|structure)\b",
        r"\b(how should we|what\'s the approach)\b",
    ],
    Intent.DECIDE: [
        r"\b(decide|choose|pick|select|go with)\b",
        r"\b(should we|which one|option)\b",
    ],
    Intent.RESUME: [
        r"\b(resume|continue|pick up|where were we)\b",
        r"\b(back to|get back to)\b",
    ],
    Intent.STATUS: [
        r"\b(status|progress|where are we|what\'s done)\b",
        r"\b(how far|check on)\b",
    ],
    Intent.REVIEW: [
        r"\b(review|check|look at|examine)\b",
        r"\b(code review|pr review)\b",
    ],
}

# Decision extraction patterns
DECISION_PATTERNS = [
    r"let's go with (.+?)(?:\.|$)",
    r"let's use (.+?)(?:\.|$)",
    r"we('ll| will) use (.+?)(?:\.|$)",
    r"decided to (.+?)(?:\.|$)",
    r"going with (.+?)(?:\.|$)",
    r"the decision is (.+?)(?:\.|$)",
    r"chose (.+?)(?:\.|$)",
    r"settled on (.+?)(?:\.|$)",
]

# Blocker extraction patterns
BLOCKER_PATTERNS = [
    r"blocked on (.+?)(?:\.|$)",
    r"blocked by (.+?)(?:\.|$)",
    r"can't .+ until (.+?)(?:\.|$)",
    r"waiting on (.+?)(?:\.|$)",
    r"waiting for (.+?)(?:\.|$)",
    r"need (.+?) before",
    r"depends on (.+?)(?:\.|$)",
    r"stuck on (.+?)(?:\.|$)",
]

# Question extraction pattern
QUESTION_PATTERN = r"([^.!?]*\?)"

# Entity patterns (files, functions, concepts)
ENTITY_PATTERNS = [
    r"`([^`]+)`",  # Inline code
    r"([a-zA-Z_][a-zA-Z0-9_]*\.(?:py|ts|js|tsx|jsx|md|json))",  # File names
    r"([A-Z][a-zA-Z0-9]*(?:Component|Service|Manager|Handler|Controller))",  # Class names
    r"(?:function|def|class|const|let|var)\s+([a-zA-Z_][a-zA-Z0-9_]*)",  # Definitions
]


def extract_intent(message: str) -> ExtractedIntent:
    """
    Extract the primary intent from a user message.

    Returns the most likely intent with confidence score.
    """
    message_lower = message.lower()

    # Score each intent
    scores: dict[Intent, float] = {}

    for intent, patterns in INTENT_PATTERNS.items():
        score = 0.0
        matches = 0
        for pattern in patterns:
            if re.search(pattern, message_lower, re.IGNORECASE):
                matches += 1
                score += 0.3

        if matches > 0:
            scores[intent] = min(score, 1.0)

    # Default to CHAT for short messages, UNKNOWN for longer
    if not scores:
        if len(message) < 20:
            return ExtractedIntent(
                intent=Intent.CHAT, confidence=0.5, topic="", goal="", keywords=[]
            )
        return ExtractedIntent(
            intent=Intent.UNKNOWN, confidence=0.3, topic="", goal="", keywords=[]
        )

    # Get highest scoring intent
    best_intent = max(scores, key=scores.get)
    confidence = scores[best_intent]

    # Extract topic (first noun phrase or main subject)
    topic = extract_topic(message)

    # Extract goal (what specifically they want)
    goal = extract_goal(message, best_intent)

    # Extract keywords
    keywords = extract_keywords(message)

    return ExtractedIntent(
        intent=best_intent,
        confidence=confidence,
        topic=topic,
        goal=goal,
        keywords=keywords,
    )


def extract_topic(message: str) -> str:
    """Extract the main topic/subject from a message."""
    # Look for quoted terms
    quoted = re.findall(r'"([^"]+)"', message)
    if quoted:
        return quoted[0]

    # Look for inline code
    code = re.findall(r"`([^`]+)`", message)
    if code:
        return code[0]

    # Look for "the X" or "a X" patterns
    the_match = re.search(r"\b(?:the|a|an)\s+(\w+(?:\s+\w+)?)", message.lower())
    if the_match:
        return the_match.group(1)

    # Fall back to first significant word after action verb
    action_match = re.search(
        r"\b(?:implement|add|create|build|fix|refactor|test|find|explain)\s+(.+?)(?:\.|,|$)",
        message.lower(),
    )
    if action_match:
        return action_match.group(1)[:50]  # Limit length

    return ""


def extract_goal(message: str, intent: Intent) -> str:
    """Extract the specific goal based on intent type."""
    message_lower = message.lower()

    if intent == Intent.IMPLEMENT:
        match = re.search(
            r"(?:implement|add|create|build)\s+(.+?)(?:\.|,|$)", message_lower
        )
        if match:
            return match.group(1)[:100]

    elif intent == Intent.FIX:
        match = re.search(r"(?:fix|debug|solve)\s+(.+?)(?:\.|,|$)", message_lower)
        if match:
            return match.group(1)[:100]

    elif intent == Intent.UNDERSTAND:
        match = re.search(
            r"(?:how does|what is|explain)\s+(.+?)(?:\?|$)", message_lower
        )
        if match:
            return match.group(1)[:100]

    return ""


def extract_keywords(message: str) -> list[str]:
    """Extract key terms from a message."""
    # Remove common words
    stop_words = {
        "the",
        "a",
        "an",
        "is",
        "are",
        "was",
        "were",
        "be",
        "been",
        "have",
        "has",
        "had",
        "do",
        "does",
        "did",
        "will",
        "would",
        "could",
        "should",
        "may",
        "might",
        "must",
        "can",
        "to",
        "of",
        "in",
        "for",
        "on",
        "with",
        "at",
        "by",
        "from",
        "as",
        "into",
        "through",
        "during",
        "before",
        "after",
        "above",
        "below",
        "between",
        "under",
        "again",
        "further",
        "then",
        "once",
        "here",
        "there",
        "when",
        "where",
        "why",
        "how",
        "all",
        "each",
        "few",
        "more",
        "most",
        "other",
        "some",
        "such",
        "no",
        "nor",
        "not",
        "only",
        "own",
        "same",
        "so",
        "than",
        "too",
        "very",
        "just",
        "and",
        "but",
        "or",
        "if",
        "because",
        "until",
        "while",
        "it",
        "this",
        "that",
        "these",
        "those",
        "i",
        "me",
        "my",
        "we",
        "us",
        "you",
        "your",
        "he",
        "she",
        "they",
        "them",
        "what",
        "which",
        "let's",
        "lets",
        "let",
        "please",
        "can",
        "want",
        "need",
        "like",
    }

    # Extract words
    words = re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", message.lower())

    # Filter and dedupe
    keywords = []
    seen = set()
    for word in words:
        if word not in stop_words and word not in seen and len(word) > 2:
            seen.add(word)
            keywords.append(word)

    return keywords[:10]  # Limit to 10 keywords


def extract_decisions(message: str) -> list[str]:
    """Extract any decisions made in a message."""
    decisions = []
    message_lower = message.lower()

    for pattern in DECISION_PATTERNS:
        matches = re.findall(pattern, message_lower)
        for match in matches:
            if isinstance(match, tuple):
                match = match[-1]  # Get last group
            if match and len(match) > 5:
                decisions.append(match.strip())

    return decisions


def extract_blockers(message: str) -> list[str]:
    """Extract any blockers mentioned in a message."""
    blockers = []
    message_lower = message.lower()

    for pattern in BLOCKER_PATTERNS:
        matches = re.findall(pattern, message_lower)
        for match in matches:
            if match and len(match) > 5:
                blockers.append(match.strip())

    return blockers


def extract_questions(message: str) -> list[str]:
    """Extract questions from a message."""
    questions = re.findall(QUESTION_PATTERN, message)
    return [q.strip() for q in questions if len(q.strip()) > 10]


def extract_entities(message: str) -> list[str]:
    """Extract file names, function names, and other code entities."""
    entities = []
    seen = set()

    for pattern in ENTITY_PATTERNS:
        matches = re.findall(pattern, message)
        for match in matches:
            if match and match not in seen:
                seen.add(match)
                entities.append(match)

    return entities


def classify_memory_type(
    message: str,
    intent: Intent,
    has_decisions: bool,
    has_blockers: bool,
) -> MemoryType:
    """Classify the memory type based on content analysis."""

    # Explicit decisions
    if has_decisions:
        return MemoryType.DECISION

    # Blockers
    if has_blockers:
        return MemoryType.BLOCKER

    # Error messages
    if re.search(r"\b(error|exception|failed|traceback)\b", message.lower()):
        return MemoryType.ERROR

    # Goals
    if intent in (Intent.PLAN, Intent.IMPLEMENT) and re.search(
        r"\b(goal|objective|want to|trying to|need to)\b", message.lower()
    ):
        return MemoryType.GOAL

    # Preferences
    if re.search(r"\b(prefer|always|never|like to|don\'t like)\b", message.lower()):
        return MemoryType.PREFERENCE

    # Constraints
    if re.search(r"\b(must|require|constraint|limitation|can\'t)\b", message.lower()):
        return MemoryType.CONSTRAINT

    # Rationale (explaining why)
    if re.search(r"\b(because|reason|since|therefore|so that)\b", message.lower()):
        return MemoryType.RATIONALE

    # Code context (mentions specific files/functions)
    if re.search(r"\.(py|ts|js|tsx|jsx|go|rs)\b", message):
        return MemoryType.CODE_CONTEXT

    # Default to exchange
    return MemoryType.EXCHANGE


def extract_understanding(message: str, role: str = "user") -> ExtractedUnderstanding:
    """
    Full understanding extraction from a message.

    This is the main entry point for the understanding layer.
    """
    # Get intent
    intent = extract_intent(message)

    # Extract structured information
    decisions = extract_decisions(message)
    blockers = extract_blockers(message)
    questions = extract_questions(message)
    entities = extract_entities(message)

    # Classify memory type
    memory_type = classify_memory_type(
        message,
        intent.intent,
        len(decisions) > 0,
        len(blockers) > 0,
    )

    return ExtractedUnderstanding(
        intent=intent,
        memory_type=memory_type,
        decisions=decisions,
        blockers=blockers,
        questions=questions,
        entities=entities,
    )
