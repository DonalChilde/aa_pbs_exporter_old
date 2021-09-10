from PyPDF4 import PdfFileReader
from tests.aa_pbs_exporter.conftest import FileResource

from aa_pbs_exporter.app_lib.pypdf4_util import TextPage, text_pages


def test_text_page(pairing_package_pdf: FileResource):
    print(pairing_package_pdf)
    file_path = pairing_package_pdf.file_path
    count = 0
    for page in text_pages(file_path):
        count += 1
        print("page:", page.page_number)
        print(page.page_text)
    assert count > 2


def test_pdf_info(pairing_package_pdf: FileResource):
    file_path = pairing_package_pdf.file_path
    with open(file_path, "rb") as file:
        read_pdf = PdfFileReader(file)
        print(read_pdf.documentInfo)
    assert False
