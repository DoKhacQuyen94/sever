from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import io

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    text_to_find = request.form.get('text', '').strip()
    
    image = Image.open(io.BytesIO(file.read()))
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    
    results = []
    for i in range(len(data['text'])):
        if text_to_find.lower() in data['text'][i].strip().lower():
            results.append({
                "text": data['text'][i],
                "x": data['left'][i],
                "y": data['top'][i],
                "width": data['width'][i],
                "height": data['height'][i]
            })
    
    return jsonify({
        "found": len(results) > 0,
        "matches": results
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
