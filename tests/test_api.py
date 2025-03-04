import requests

# DATA_MANAGER_URL = "http://localhost:5000"
# RECOGNITION_SERVICE_URL = "http://localhost:5001"

# def test_data_manager_running():
#     response = requests.get(f"{DATA_MANAGER_URL}/")
#     assert response.status_code == 200
#     assert "Data Manager API is running!" in response.text

# def test_recognition_service_running():
#     response = requests.get(f"{RECOGNITION_SERVICE_URL}/")
#     assert response.status_code == 200
#     assert "Recognition Service is running!" in response.text

# def test_add_image():
#     image_data = {"name": "test_image", "path": "/images/test.jpg"}
#     response = requests.post(f"{DATA_MANAGER_URL}/images", json=image_data)
#     assert response.status_code == 201
#     assert "uploaded" in response.json()["status"]

# def test_recognition():
#     image_id = 1
#     response = requests.post(f"{RECOGNITION_SERVICE_URL}/recognize", json={"image_id": image_id})
#     assert response.status_code == 200
#     assert "processed" in response.json()["status"]


BASE_URL = "http://localhost:5000"  # Адрес сервиса

def test_upload_image():
    response = requests.post(f"{BASE_URL}/images", json={"path": "images/image1.png"})
    assert response.status_code == 200
    assert "image_id" in response.json()

def test_get_image():
    response = requests.get(f"{BASE_URL}/results/1")
    assert response.status_code == 200
    assert "nodes" in response.json()

def test_create_node():
    data = {"name": "Test Node", "type": "Test"}
    response = requests.post(f"{BASE_URL}/results/1/nodes", json=data)
    assert response.status_code == 201
    assert response.json()["node"]["name"] == "Test Node"

def test_update_node():
    data = {"name": "Updated Node", "type": "Test"}
    response = requests.put(f"{BASE_URL}/results/1/nodes/1", json=data)
    assert response.status_code == 200

def test_delete_node():
    response = requests.delete(f"{BASE_URL}/nodes/1")
    assert response.status_code == 200
