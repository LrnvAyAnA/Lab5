from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/recognize', methods=['POST'])
def recognize():
    data = request.json
    image_id = data.get("image_id")
    return jsonify({"image_id": image_id, "result": "Recognized Object"}), 200

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)