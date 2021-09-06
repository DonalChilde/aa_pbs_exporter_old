from tests.aa_pbs_exporter.conftest import FileResource

from aa_pbs_exporter.app_lib.pypdf4_text_grab import PageContent, get_page_contents


def test_get_page_contents(pairing_package_pdf: FileResource):
    print(pairing_package_pdf)
    file_path = pairing_package_pdf.file_path
    contents = get_page_contents(file_path)
    assert len(contents) > 2
    for page in contents:
        print("page:", page.page_number)
        print(page.page_text)
    assert False
