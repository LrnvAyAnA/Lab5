from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

DATA_MANAGER_URL = "http://lab5-data_manager-1:5000"  # URL API data-manager

@app.route('/')
def home():
    return "Recognition Service is running!"

@app.route('/recognize', methods=['POST'])
def recognize():
    data = request.json
    image_id = data.get("image_id")
    
    if not image_id:
        return jsonify({"error": "Missing image_id"}), 400
    
    # Получаем данные изображения из data-manager
    response = requests.get(f"{DATA_MANAGER_URL}/images/{image_id}")
    if response.status_code != 200:
        return jsonify({"error": "Image not found"}), 404

    image_data = response.json()
    image_name = image_data.get("name")

    # Используем имя изображения вместо обработки
    nodes = [{"name": image_name, "type": "image"}]

    # Отправляем узлы в data-manager
    for node in nodes:
        requests.post(f"{DATA_MANAGER_URL}/results/{image_id}/nodes", json=node)

    return jsonify({"status": "processed", "nodes": nodes})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
