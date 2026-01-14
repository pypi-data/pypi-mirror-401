"""
File upload handling for NeuralForge.
"""

from typing import Optional
import io


class UploadFile:
    """
    Represents an uploaded file.
    
    Example:
        @app.post("/upload")
        async def upload_image(file: UploadFile):
            contents = await file.read()
            return {"filename": file.filename, "size": len(contents)}
    """

    def __init__(
        self,
        filename: str,
        content: bytes,
        content_type: Optional[str] = None
    ):
        self.filename = filename
        self._content = content
        self.content_type = content_type or "application/octet-stream"
        self._file = io.BytesIO(content)

    async def read(self, size: int = -1) -> bytes:
        """Read file contents."""
        return self._file.read(size)

    async def seek(self, offset: int) -> int:
        """Seek to position in file."""
        return self._file.seek(offset)

    async def close(self):
        """Close file."""
        self._file.close()

    @property
    def size(self) -> int:
        """Get file size in bytes."""
        return len(self._content)

    def __repr__(self) -> str:
        return f"UploadFile(filename='{self.filename}', size={self.size}, content_type='{self.content_type}')"
