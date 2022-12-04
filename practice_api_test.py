from practice_api import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_one():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Question one": "What year were you born? Please provide your answer as a JSON in the format {\'birth_year\': YOUR_ANSWER} through a POST API request to http://localhost:8000/, where the value of your answer is an integer"}

def test_two():
    response = client.post(
        "/",
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        json={"birth_year": 1975},
    )
    assert response.status_code == 200
    assert response.json() == {"Question two": "How much do you weigh (in kg)? Please provide your answer as a JSON in the format {\'weight\': YOUR_ANSWER} through a POST API request to http://localhost:8000/weight, where the value of your answer is an integer"}

def test_three():
    response = client.post(
        "/",
        headers={"Accept": "application/json", "Content-Type": "application/json"},
        json={"birth_year": 2000},
    )
    assert response.status_code == 200
    assert response.json() == {"Question two": "Do you dye your hair? Please provide your answer as a JSON in the format {\'hair_dye\': YOUR_ANSWER} through a POST API request to http://localhost:8000/hair_dye, where the value of your answer is an boolean"}