from io import BytesIO
from pypdf import PdfWriter


class PDFRepository:
    def merge_files(self, files: list[BytesIO]) -> BytesIO:
        merger = PdfWriter()
        for file in files:
            merger.append(file)

        output = BytesIO()
        merger.write(output)
        return output

    def encrypt(self, file: BytesIO, password: str) -> BytesIO:
        writer = PdfWriter()
        writer.append(file)
        writer.encrypt(password)

        output = BytesIO()
        writer.write(output)
        return output
