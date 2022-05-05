#pip3 install pytest
import requests

#region updater
UPDATER_BASE_URL = "http://localhost:8094"
SPA_PDF_NAME = "TestSPA.pdf"
SPA_PDF_PATH = "./tests/TestSPA.pdf"

def test_upload_spa():
    response = requests.post(f"{UPDATER_BASE_URL}/upload", files= {'file': open(SPA_PDF_PATH, 'rb')})
    assert response.status_code == 200

def test_view():
    response = requests.get(f"{UPDATER_BASE_URL}/file/{SPA_PDF_NAME}")
    assert response.status_code == 200

def test_download():
    response = requests.get(f"{UPDATER_BASE_URL}/download/{SPA_PDF_NAME}")
    assert response.status_code == 200
#endregion 

if __name__ ==  "__main__":
    test_upload_spa()