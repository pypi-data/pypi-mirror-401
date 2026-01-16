"""Document chunking for text embedding."""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Chunk:
    """A chunk of text from a document."""

    index: int
    text: str
    start_offset: int
    end_offset: int
    token_count: int


class DocumentChunker:
    """Split documents into overlapping chunks for embedding.

    Uses character-based chunking with smart boundary detection.
    Approximates ~4 characters per token for sizing.
    """

    # Break point characters in order of preference
    BREAK_CHARS = ["\n\n", "\n", ". ", "! ", "? ", "; ", ", ", " "]

    def __init__(
        self,
        chunk_size: int = 512,
        chunk_overlap: int = 64,
        chars_per_token: int = 4,
    ):
        """
        Initialize the chunker.

        Args:
            chunk_size: Target number of tokens per chunk
            chunk_overlap: Number of tokens to overlap between chunks
            chars_per_token: Approximate characters per token (default 4)
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.chars_per_token = chars_per_token

        # Convert to character counts
        self.char_size = chunk_size * chars_per_token
        self.char_overlap = chunk_overlap * chars_per_token

    def chunk_text(self, text: str) -> List[Chunk]:
        """
        Split text into overlapping chunks.

        Args:
            text: The text to chunk

        Returns:
            List of Chunk objects
        """
        if not text or not text.strip():
            return []

        # Normalize whitespace
        text = text.strip()

        chunks = []
        start = 0
        index = 0

        while start < len(text):
            # Calculate end position
            end = min(start + self.char_size, len(text))

            # If not at end of text, find a good break point
            if end < len(text):
                end = self._find_break_point(text, start, end)

            # Extract chunk text
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append(Chunk(
                    index=index,
                    text=chunk_text,
                    start_offset=start,
                    end_offset=end,
                    token_count=len(chunk_text) // self.chars_per_token,
                ))
                index += 1

            # Move start position (with overlap)
            # Don't overlap if we're at the end
            if end >= len(text):
                break

            start = end - self.char_overlap

            # Ensure we make progress
            if start <= chunks[-1].start_offset if chunks else 0:
                start = end

        return chunks

    def _find_break_point(self, text: str, start: int, end: int) -> int:
        """
        Find the best break point near the target end position.

        Looks for break characters in the last 20% of the chunk,
        preferring paragraph breaks over sentence breaks over word breaks.

        Args:
            text: Full text
            start: Start of current chunk
            end: Target end position

        Returns:
            Adjusted end position at a good break point
        """
        # Search in the last 20% of the chunk for a break
        search_start = end - int((end - start) * 0.2)
        search_region = text[search_start:end]

        # Try each break character in order of preference
        for break_char in self.BREAK_CHARS:
            # Find the last occurrence of this break char
            idx = search_region.rfind(break_char)
            if idx != -1:
                # Return position after the break character
                return search_start + idx + len(break_char)

        # No good break found, just use the target end
        return end

    def estimate_chunks(self, text_length: int) -> int:
        """
        Estimate the number of chunks for a given text length.

        Args:
            text_length: Number of characters in the text

        Returns:
            Estimated number of chunks
        """
        if text_length <= self.char_size:
            return 1

        # Account for overlap
        effective_size = self.char_size - self.char_overlap
        return max(1, (text_length - self.char_overlap) // effective_size + 1)


def chunk_document(
    content: str,
    chunk_size: int = 512,
    chunk_overlap: int = 64,
) -> List[Dict]:
    """
    Convenience function to chunk document content.

    Args:
        content: Text content to chunk
        chunk_size: Target tokens per chunk
        chunk_overlap: Overlap tokens between chunks

    Returns:
        List of chunk dictionaries ready for API submission
    """
    chunker = DocumentChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = chunker.chunk_text(content)

    return [
        {
            "chunk_index": c.index,
            "chunk_text": c.text,
            "start_offset": c.start_offset,
            "end_offset": c.end_offset,
            "token_count": c.token_count,
        }
        for c in chunks
    ]
