#pip3 install pytest, requests
#pytest ./tests/tests.py
import requests, json
#region uploader
UPLOADER_BASE_URL = "http://localhost:8094"
SPA_PDF_NAME = "TestSPA.pdf"
SPA_PDF_PATH = "./tests/TestSPA.pdf"
ENG_PDF_NAME = "TestENG.pdf"
ENG_PDF_PATH = "./tests/TestENG.pdf"

def test_upload_spa():
    response = requests.post(f"{UPLOADER_BASE_URL}/upload", files= {'file': open(SPA_PDF_PATH, 'rb')})
    assert response.status_code == 200

def test_upload_eng():
    response = requests.post(f"{UPLOADER_BASE_URL}/upload", files= {'file': open(ENG_PDF_PATH, 'rb')})
    #should fail
    assert response.status_code == 400

def test_view_spa():
    response = requests.get(f"{UPLOADER_BASE_URL}/file/{SPA_PDF_NAME}")
    assert response.status_code == 200

def test_download_spa():
    response = requests.get(f"{UPLOADER_BASE_URL}/download/{SPA_PDF_NAME}")
    assert response.status_code == 200

def test_view_eng():
    response = requests.get(f"{UPLOADER_BASE_URL}/file/{ENG_PDF_NAME}")
    assert response.status_code == 500

def test_download_eng():
    response = requests.get(f"{UPLOADER_BASE_URL}/download/{ENG_PDF_NAME}")
    assert response.status_code == 500
#endregion 

#region facade
FACADE_BASE_URL = "http://localhost:8093"
QUERY = "test"
def test_query():
    response = requests.get(f"{FACADE_BASE_URL}/query?query={QUERY}")
    assert response.status_code == 200

def test_suggest():
    response = requests.get(f"{FACADE_BASE_URL}/suggest?query={QUERY}")
    assert response.status_code == 200
#endregion 

#region synonym updater
UPDATER_BASE_URL = "http://localhost:8092"
SYNONYM_LIST = ["PALACIO", "CASTILLO"]

def test_update_synonym():
    response = requests.post(f"{UPDATER_BASE_URL}/update", data = json.dumps(SYNONYM_LIST))
    assert response.status_code == 201

#endregion 

#region synonym api
SYNONYM_BASE_URL = "http://localhost:8091"
WORD_SPA = "palacio"
WORD_ENG = "castle"

def test_spa_synonym():
    response = requests.get(f"{SYNONYM_BASE_URL}/spa?word={WORD_SPA}")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_eng_synonym():
    response = requests.get(f"{SYNONYM_BASE_URL}/eng?word={WORD_ENG}")
    assert response.status_code == 200
    assert len(response.json()) > 0

#endregion
if __name__ ==  "__main__":
    test_upload_spa()