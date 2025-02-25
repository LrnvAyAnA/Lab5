from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
db = SQLAlchemy(app)

class ImageData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    path = db.Column(db.String(200), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/images', methods=['POST'])
def add_image():
    data = request.json
    new_image = ImageData(name=data["name"], path=data["path"])
    db.session.add(new_image)
    db.session.commit()
    return jsonify({"id": new_image.id}), 201

@app.route('/images', methods=['GET'])
def get_images():
    images = ImageData.query.all()
    return jsonify([{"id": img.id, "name": img.name, "path": img.path} for img in images])

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

# Простое хранилище данных
# data = {}
# next_node_id = 1

# # POST /images
# @app.route('/images', methods=['POST'])
# def upload_image():
#     image_id = len(data) + 1
#     data[image_id] = {"nodes": [], "connections": []}
    
#     # Возвращаем нужный формат ответа
#     return jsonify({
#         "image_id": image_id,
#         "status": "uploaded",
#         "connections": [],  # Добавляем connections, как указано в ошибке
#         "nodes": []         # Добавляем nodes, как указано в ошибке
#     }), 201

# # POST /results/<image_id>/nodes
# @app.route('/results/<int:image_id>/nodes', methods=['POST'])
# def create_node(image_id):
#     if image_id not in data:
#         return jsonify({"error": "Image not found"}), 404

#     global next_node_id
#     node_data = request.json
#     node = {
#         "id": next_node_id,
#         "name": node_data.get("name", "Unnamed Node"),
#         "type": node_data.get("type", "Unknown")
#     }
#     data[image_id]["nodes"].append(node)
#     next_node_id += 1

#     return jsonify({"status": "created", "image_id": image_id, "node": node}), 200

# # GET /results/<image_id>
# @app.route('/results/<int:image_id>', methods=['GET'])
# def get_results(image_id):
#     if image_id not in data:
#         return jsonify({"error": "Image not found"}), 404
    
#     # Включаем image_id и статус в ответ
#     result = data[image_id]
#     result["image_id"] = image_id  # Добавляем image_id
#     result["status"] = "success"   # Добавляем статус
    
#     return jsonify(result), 201

# # PUT /images/<image_id>
# @app.route('/images/<int:image_id>', methods=['PUT'])
# def update_image_metadata(image_id):
#     if image_id not in data:
#         return jsonify({"error": "Image not found"}), 404

#     # Обновление метаданных
#     metadata = request.json
#     data[image_id]["metadata"] = {
#         "title": metadata.get("title", "Untitled"),
#         "description": metadata.get("description", "No description")
#     }

#     return jsonify({"status": "metadata updated", "metadata": data[image_id]["metadata"]}), 200

# # PUT /results/<image_id>/nodes/<node_id>
# @app.route('/results/<int:image_id>/nodes/<int:node_id>', methods=['PUT'])
# def update_node(image_id, node_id):
#     if image_id not in data:
#         return jsonify({"error": "Image not found"}), 404
    
#     nodes = data[image_id]["nodes"]
#     for node in nodes:
#         if node["id"] == node_id:
#             node.update(request.json)
#             return jsonify({"status": "updated"}), 200
    
#     return jsonify({"error": "Node not found"}), 404

# # DELETE /results/<image_id>
# @app.route('/results/<int:image_id>', methods=['DELETE'])
# def delete_results(image_id):
#     if image_id not in data:
#         return jsonify({"error": "Image not found"}), 404
    
#     del data[image_id]
#     return jsonify({"status": "deleted"}), 200

# # GET /nodes/<node_id>
# @app.route('/nodes/<int:node_id>', methods=['GET'])
# def get_node(node_id):
#     for image_id, content in data.items():
#         for node in content["nodes"]:
#             if node["id"] == node_id:
#                 return jsonify(node), 200
#     return jsonify({"error": "Node not found"}), 404

# # DELETE /nodes/<node_id>
# @app.route('/nodes/<int:node_id>', methods=['DELETE'])
# def delete_node(node_id):
#     """
#     Удаляет узел с указанным node_id из всех изображений.
#     """
#     for image_id, content in data.items():
#         nodes = content["nodes"]
#         for node in nodes:
#             if node["id"] == node_id:
#                 nodes.remove(node)
#                 return jsonify({"status": "Node deleted"}), 200

#     return jsonify({"error": "Node not found"}), 404

# # POST /results/export
# @app.route('/results/export', methods=['POST'])
# def export_results():
#     request_data = request.json
#     image_id = request_data.get("image_id")
#     format = request_data.get("format", "json")
    
#     if image_id not in data:
#         return jsonify({"error": "Image not found"}), 404
    
#     if format == "json":
#         return jsonify({"status": "exported", "data": data[image_id]}), 200
#     elif format == "plantuml":
#         return jsonify({"status": "exported", "file": "exported_diagram.puml"}), 200
#     else:
#         return jsonify({"error": "Unsupported format"}), 400

# if __name__ == '__main__':
#     app.run(debug=True)
