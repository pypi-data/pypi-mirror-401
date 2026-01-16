#!/usr/bin/env python3
"""
PreToolUse hook to intercept RAG Memory ingest operations.
Requires explicit user approval before any content is ingested.

Handles ALL parameters for ALL ingest tools:
- ingest_text: content, collection_name, document_title, metadata, include_chunk_ids, mode, topic, reviewed_by_human, actor_type
- ingest_url: url, collection_name, mode, follow_links, max_pages, metadata, include_document_ids, dry_run, topic, reviewed_by_human, actor_type
- ingest_file: file_path, collection_name, metadata, include_chunk_ids, mode, topic, reviewed_by_human, actor_type
- ingest_directory: directory_path, collection_name, file_extensions, recursive, metadata, include_document_ids, mode, topic, reviewed_by_human, actor_type
"""
import json
import sys

# Read hook input from stdin
try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    # Invalid input, allow by default (shouldn't happen)
    sys.exit(0)

tool_name = input_data.get("tool_name", "")
tool_input = input_data.get("tool_input", {})

# Only intercept RAG Memory ingest operations
if not tool_name.startswith("mcp__rag-memory__ingest_"):
    sys.exit(0)  # Not an ingest tool, allow

# Extract common parameters
collection = tool_input.get("collection_name", "Unknown")
topic = tool_input.get("topic")
if topic is None:
    topic = "None"
mode = tool_input.get("mode", "ingest")
metadata = tool_input.get("metadata")
reviewed_by_human = tool_input.get("reviewed_by_human", False)
actor_type = tool_input.get("actor_type", "agent")

# Build content preview and details based on tool type
content_lines = []
details_lines = []

if "ingest_url" in tool_name:
    url = tool_input.get("url", "")
    content_lines.append(f"URL: {url}")

    # URL-specific parameters
    follow_links = tool_input.get("follow_links", False)
    max_pages = tool_input.get("max_pages", 10)
    dry_run = tool_input.get("dry_run", False)
    include_document_ids = tool_input.get("include_document_ids", False)

    if follow_links:
        content_lines.append(f"  └─ Will crawl up to {max_pages} pages")
    if dry_run:
        details_lines.append("⚠️  DRY RUN MODE - Preview only, no actual ingest")
    if include_document_ids:
        details_lines.append("Will return document IDs")

elif "ingest_file" in tool_name:
    file_path = tool_input.get("file_path", "")
    content_lines.append(f"File: {file_path}")

    # File-specific parameters
    include_chunk_ids = tool_input.get("include_chunk_ids", False)
    if include_chunk_ids:
        details_lines.append("Will return chunk IDs")

elif "ingest_directory" in tool_name:
    dir_path = tool_input.get("directory_path", "")
    content_lines.append(f"Directory: {dir_path}")

    # Directory-specific parameters
    file_extensions = tool_input.get("file_extensions")
    recursive = tool_input.get("recursive", False)
    include_document_ids = tool_input.get("include_document_ids", False)

    if file_extensions:
        ext_str = ", ".join(file_extensions)
        content_lines.append(f"  └─ File types: {ext_str}")
    else:
        content_lines.append("  └─ File types: .txt, .md (default)")

    if recursive:
        content_lines.append("  └─ Recursive: YES (includes subdirectories)")
    else:
        content_lines.append("  └─ Recursive: NO (current directory only)")

    if include_document_ids:
        details_lines.append("Will return document IDs")

elif "ingest_text" in tool_name:
    text = tool_input.get("content", "")
    document_title = tool_input.get("document_title")
    include_chunk_ids = tool_input.get("include_chunk_ids", False)

    preview = text[:100]
    if len(text) > 100:
        preview += "..."
    content_lines.append(f'Text: "{preview}"')

    if document_title:
        content_lines.append(f"  └─ Title: {document_title}")
    else:
        content_lines.append("  └─ Title: (auto-generated)")

    if include_chunk_ids:
        details_lines.append("Will return chunk IDs")

else:
    content_lines.append("Unknown content type")

# Add mode information if not default
if mode == "reingest":
    details_lines.append("⚠️  MODE: REINGEST - Will delete existing content and replace")

# Add metadata information if present
if metadata:
    # Show metadata keys (not values, might be sensitive)
    metadata_keys = ", ".join(metadata.keys())
    details_lines.append(f"Custom metadata: {metadata_keys}")

# Add reviewed_by_human flag if set
if reviewed_by_human:
    details_lines.append("✓ Marked as reviewed by human")

# Add actor_type if not default
if actor_type != "agent":
    details_lines.append(f"Actor: {actor_type}")

# Build final approval message
message_parts = ["RAG Memory Ingest Request\n"]
message_parts.append(f"Collection: {collection}")
message_parts.append(f"Topic: {topic}")
message_parts.append("")
message_parts.extend(content_lines)

if details_lines:
    message_parts.append("")
    message_parts.extend(details_lines)

message_parts.append("")
message_parts.append("Approve this ingest?")

message = "\n".join(message_parts)

# Return decision: ask user for approval
output = {
    "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "ask",
        "permissionDecisionReason": message
    }
}

print(json.dumps(output))
sys.exit(0)
