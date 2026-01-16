#!/usr/bin/env python3
"""
Test script for Semplex API endpoints.

Uses sample data from debug_output.jsonl to test:
- POST /api/metadata (tabular file metadata)
- POST /api/document-chunks (document chunk embeddings)

Usage:
    # Test production
    python scripts/test_deployment.py

    # Test local development
    python scripts/test_deployment.py --local

    # Test with API key
    python scripts/test_deployment.py --api-key YOUR_KEY --email your@email.com

    # Verbose output
    python scripts/test_deployment.py -v
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import httpx
except ImportError:
    print("Error: httpx is required. Install with: pip install httpx")
    sys.exit(1)


# Sample test payloads (simplified from debug_output.jsonl)
SAMPLE_METADATA_PAYLOAD = {
    "filename": "test-file.tsv",
    "filepath": "/test/path/test-file.tsv",
    "file_type": ".tsv",
    "file_size": 1024,
    "file_owner": "test-user",
    "modified_at": "2026-01-14T12:00:00.000000",
    "extracted_at": "2026-01-14T12:00:01.000000",
    "error": None,
    "headers": ["Column1", "Column2", "Column3"],
    "header_row_index": 0,
    "metadata_rows": None,
    "row_count": None,
    "total_row_count": None,
    "data_row_count": None,
    "column_count": 3,
    "delimiter": "'\\t'",
    "user_email": None,  # Will be set from args
    "machine_name": "test-machine",
    "organization_handle": None,
}

SAMPLE_DOCUMENT_CHUNKS_PAYLOAD = {
    "file_id": "test123abc456def789",
    "filepath": "/test/path/test-document.md",
    "filename": "test-document.md",
    "file_type": ".md",
    "file_size": 2048,
    "chunks": [
        {
            "chunk_index": 0,
            "chunk_text": "# Test Document\n\nThis is a test document for verifying the document chunks API endpoint.",
            "start_offset": 0,
            "end_offset": 89,
            "token_count": 20,
        },
        {
            "chunk_index": 1,
            "chunk_text": "## Section 2\n\nThis is the second chunk with some overlap from the first chunk.",
            "start_offset": 70,
            "end_offset": 148,
            "token_count": 18,
        },
    ],
    "store_text": False,
    "user_email": None,  # Will be set from args
    "machine_name": "test-machine",
    "organization_handle": None,
}


def load_sample_from_debug(debug_file: Path, endpoint_type: str) -> Optional[Dict[str, Any]]:
    """Load a real sample payload from debug_output.jsonl."""
    if not debug_file.exists():
        return None

    target_url_part = "api/metadata" if endpoint_type == "metadata" else "api/document-chunks"

    with open(debug_file, "r") as f:
        content = f.read()

    # Split by separator
    entries = content.split("=" * 80)

    for entry in entries:
        entry = entry.strip()
        if not entry:
            continue
        try:
            data = json.loads(entry)
            if target_url_part in data.get("url", ""):
                return data.get("body")
        except json.JSONDecodeError:
            continue

    return None


def test_endpoint(
    base_url: str,
    endpoint: str,
    payload: Dict[str, Any],
    api_key: Optional[str] = None,
    verbose: bool = False,
) -> bool:
    """Test a single API endpoint."""
    url = f"{base_url}{endpoint}"

    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    if verbose:
        print(f"\n{'='*60}")
        print(f"Testing: {url}")
        print(f"Headers: {headers}")
        print(f"Payload (truncated):")
        payload_preview = json.dumps(payload, indent=2)
        if len(payload_preview) > 500:
            print(payload_preview[:500] + "\n... (truncated)")
        else:
            print(payload_preview)
        print(f"{'='*60}")

    try:
        with httpx.Client(timeout=30) as client:
            response = client.post(url, json=payload, headers=headers)

        if verbose:
            print(f"\nResponse Status: {response.status_code}")
            print(f"Response Body: {response.text[:1000] if len(response.text) > 1000 else response.text}")

        if response.status_code in (200, 201):
            print(f"✓ {endpoint} - Success ({response.status_code})")
            return True
        elif response.status_code == 401:
            print(f"✗ {endpoint} - Unauthorized (401) - API key may be invalid or missing")
            return False
        elif response.status_code == 403:
            print(f"✗ {endpoint} - Forbidden (403) - Permission denied")
            return False
        else:
            print(f"✗ {endpoint} - Failed ({response.status_code}): {response.text[:200]}")
            return False

    except httpx.ConnectError as e:
        print(f"✗ {endpoint} - Connection failed: {e}")
        return False
    except httpx.TimeoutException:
        print(f"✗ {endpoint} - Request timed out")
        return False
    except Exception as e:
        print(f"✗ {endpoint} - Error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Test Semplex API endpoints")
    parser.add_argument(
        "--local",
        action="store_true",
        help="Test local development server (http://localhost:3000)",
    )
    parser.add_argument(
        "--url",
        type=str,
        help="Custom base URL (overrides --local)",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default=os.environ.get("SEMPLEX_API_KEY"),
        help="API key for authentication (or set SEMPLEX_API_KEY env var)",
    )
    parser.add_argument(
        "--email",
        type=str,
        default=os.environ.get("SEMPLEX_USER_EMAIL"),
        help="User email for requests (or set SEMPLEX_USER_EMAIL env var)",
    )
    parser.add_argument(
        "--use-debug-data",
        action="store_true",
        help="Use real sample data from debug_output.jsonl instead of test data",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output",
    )
    parser.add_argument(
        "--metadata-only",
        action="store_true",
        help="Only test /api/metadata endpoint",
    )
    parser.add_argument(
        "--chunks-only",
        action="store_true",
        help="Only test /api/document-chunks endpoint",
    )

    args = parser.parse_args()

    # Determine base URL
    if args.url:
        base_url = args.url.rstrip("/")
    elif args.local:
        base_url = "http://localhost:3000"
    else:
        base_url = "https://semplex.simage.ai"

    print(f"Testing Semplex API at: {base_url}")
    print(f"API Key: {'(set)' if args.api_key else '(not set)'}")
    print(f"Email: {args.email or '(not set)'}")
    print()

    # Prepare payloads
    debug_file = Path(__file__).parent.parent / "debug_output.jsonl"

    if args.use_debug_data and debug_file.exists():
        print("Using real sample data from debug_output.jsonl")
        metadata_payload = load_sample_from_debug(debug_file, "metadata") or SAMPLE_METADATA_PAYLOAD
        chunks_payload = load_sample_from_debug(debug_file, "chunks") or SAMPLE_DOCUMENT_CHUNKS_PAYLOAD
    else:
        metadata_payload = SAMPLE_METADATA_PAYLOAD.copy()
        chunks_payload = SAMPLE_DOCUMENT_CHUNKS_PAYLOAD.copy()

    # Set user email if provided
    if args.email:
        metadata_payload["user_email"] = args.email
        chunks_payload["user_email"] = args.email

    # Run tests
    results = []

    if not args.chunks_only:
        print("\n--- Testing /api/metadata ---")
        success = test_endpoint(
            base_url,
            "/api/metadata",
            metadata_payload,
            api_key=args.api_key,
            verbose=args.verbose,
        )
        results.append(("metadata", success))

    if not args.metadata_only:
        print("\n--- Testing /api/document-chunks ---")
        success = test_endpoint(
            base_url,
            "/api/document-chunks",
            chunks_payload,
            api_key=args.api_key,
            verbose=args.verbose,
        )
        results.append(("document-chunks", success))

    # Summary
    print("\n" + "=" * 40)
    print("Summary:")
    all_passed = True
    for name, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"  {name}: {status}")
        if not success:
            all_passed = False

    if all_passed:
        print("\nAll tests passed!")
        return 0
    else:
        print("\nSome tests failed.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
