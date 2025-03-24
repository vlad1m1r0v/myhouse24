from io import BytesIO, StringIO
from tempfile import NamedTemporaryFile
from xlsx2html import xlsx2html
from weasyprint import HTML

class FileConverterService:
    @staticmethod
    def xlsx_to_pdf(spreadsheet: BytesIO) -> BytesIO:
        with NamedTemporaryFile(suffix=".xlsx", delete=True) as temp_xlsx:
            temp_xlsx.write(spreadsheet.getvalue())
            temp_xlsx.flush()

            html_output = StringIO()
            xlsx2html(temp_xlsx.name, html_output)
            html_content = html_output.getvalue()

        pdf_bytes = HTML(string=html_content).write_pdf()
        return BytesIO(pdf_bytes)