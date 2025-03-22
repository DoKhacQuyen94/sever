from flask import Flask, request, jsonify
from PIL import Image
import io
import pytesseract

# Định nghĩa đường dẫn Tesseract
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

app = Flask(__name__)
@app.route('/', methods=['GET'])
def home():
    return "Server is running!", 200

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    image = Image.open(io.BytesIO(file.read()))

    # Trích xuất văn bản và tọa độ
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    results = []
    for i in range(len(data['text'])):
        if data['text'][i].strip():
            results.append({
                "text": data['text'][i],
                "x": data['left'][i],
                "y": data['top'][i],
                "width": data['width'][i],
                "height": data['height'][i]
            })

    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
