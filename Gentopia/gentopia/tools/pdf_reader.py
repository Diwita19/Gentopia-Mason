from typing import Any, AnyStr, Optional, Type  # Import Any and other necessary types
from gentopia.tools.basetool import *
import urllib.request  # For making HTTP requests to fetch the PDF
import PyPDF2  # For reading and extracting text from PDF files
import io  # For handling in-memory byte streams

# Define the schema for the arguments required by the PDF reader
class PDFReaderArgs(BaseModel):
    query: str = Field(..., description="URL of the PDF document to be read")

# The PDFReader tool for extracting text from a remote PDF URL
class PDFReader(BaseTool):
    name = "pdf_reader"
    description = "Extract text from a PDF document at a given URL"

    args_schema: Optional[Type[BaseModel]] = PDFReaderArgs

    # Method for synchronously running the tool
    def _run(self, query: AnyStr) -> str:
        try:
            # Make a request to the provided URL to fetch the PDF file
            req = urllib.request.Request(query, headers={'User-Agent': "Magic Browser"})
            remote_file = urllib.request.urlopen(req).read()

            # Convert the downloaded PDF content into a BytesIO object
            remote_file_bytes = io.BytesIO(remote_file)

            # Initialize the PDF reader with the in-memory file
            pdf_reader = PyPDF2.PdfReader(remote_file_bytes)

            # Extract text from each page and join them into a single string
            text = "\n\n".join(pdf_reader.pages[i].extract_text() for i in range(len(pdf_reader.pages)))

            return text

        except Exception as e:
            # Raise an error if the URL is invalid or the PDF is inaccessible
            raise ValueError("Failed to read the PDF. Please check the URL or the PDF accessibility.") from e

    # Placeholder for asynchronous version (if needed later)
    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

if __name__ == "__main__":
    # Example: Run the PDFReader tool with a sample PDF URL
    ans = PDFReader()._run("https://arxiv.org/pdf/2201.05966.pdf")
    print(ans)