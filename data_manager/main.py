from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Папка для хранения изображений
IMAGES_FOLDER = "images"  # Путь к папке с изображениями

if not os.path.exists(IMAGES_FOLDER):
    os.makedirs(IMAGES_FOLDER)

# Простая структура для хранения данных об изображениях (вместо базы данных)
images_data = {}

@app.route('/')
def index():
    return "Data Manager API is running!"

# Добавление изображения
@app.route('/images', methods=['POST'])
def add_image():
    data = request.json
    if not data or "name" not in data or "path" not in data:
        return jsonify({"error": "Invalid input"}), 400

    # Генерируем уникальный ID для изображения
    image_id = len(images_data) + 1
    image_path = os.path.join(IMAGES_FOLDER, data["name"])

    # Копируем изображение в папку, если оно существует
    if os.path.exists(data["path"]):
        with open(data["path"], "rb") as fsrc:
            with open(image_path, "wb") as fdst:
                fdst.write(fsrc.read())

    images_data[image_id] = {"name": data["name"], "path": image_path}
    return jsonify({"id": image_id, "status": "uploaded", "connections": [], "nodes": []}), 201

# Получение изображения
@app.route('/images/<int:image_id>', methods=['GET'])
def get_image(image_id):
    image = images_data.get(image_id)
    if not image:
        return jsonify({"error": "Image not found"}), 404
    return jsonify(image), 200

# Обновление данных изображения
@app.route('/images/<int:image_id>', methods=['PUT'])
def update_image_metadata(image_id):
    image = images_data.get(image_id)
    if not image:
        return jsonify({"error": "Image not found"}), 404

    data = request.json
    image["name"] = data.get("name", image["name"])
    image["path"] = data.get("path", image["path"])

    return jsonify({"status": "metadata updated", "image": image}), 200

# Удаление изображения
@app.route('/images/<int:image_id>', methods=['DELETE'])
def delete_image(image_id):
    image = images_data.get(image_id)
    if not image:
        return jsonify({"error": "Image not found"}), 404

    del images_data[image_id]
    return jsonify({"status": "deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
