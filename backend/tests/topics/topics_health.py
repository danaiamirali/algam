import pytest
import requests

def test_main():
    # Test the main page
    response = requests.get("http://127.0.0.1:8000/topics/10")
    assert response.status_code == 200
    print("Endpoint /topics/{num_topics} is healthy.")

if __name__ == "__main__":
    test_main()