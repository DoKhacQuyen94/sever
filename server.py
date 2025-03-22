from flask import Flask, request, jsonify
import pytesseract
from PIL import Image
import io
import cv2 

app = Flask(__name__)
@app.route('/', methods=['GET'])
def home():
    return "Server is running!", 200

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file part"}), 400
    
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400
    
#     text_to_find = request.form.get('text', '').strip()
    
#     image = Image.open(io.BytesIO(file.read()))
#     data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    
#     results = []
#     for i in range(len(data['text'])):
#         if text_to_find.lower() in data['text'][i].strip().lower():
#             results.append({
#                 "text": data['text'][i],
#                 "x": data['left'][i],
#                 "y": data['top'][i],
#                 "width": data['width'][i],
#                 "height": data['height'][i]
#             })
    
#     return jsonify({
#         "found": len(results) > 0,
#         "matches": results
#     })
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    text_to_find = request.form.get('text', '').strip()
    template_file = request.files.get('template')  # Hình ảnh con cần tìm
    
    image = Image.open(io.BytesIO(file.read()))
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)  # Chuyển sang OpenCV format
    
    results = []
    
    # Tìm văn bản nếu có text_to_find
    if text_to_find:
        data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
        for i in range(len(data['text'])):
            if text_to_find.lower() in data['text'][i].strip().lower():
                results.append({
                    "type": "text",
                    "text": data['text'][i],
                    "x": data['left'][i],
                    "y": data['top'][i],
                    "width": data['width'][i],
                    "height": data['height'][i]
                })
    
    # Tìm hình ảnh con nếu có file template
    if template_file:
        template = Image.open(io.BytesIO(template_file.read()))
        template_cv = cv2.cvtColor(np.array(template), cv2.COLOR_RGB2BGR)
        
        result = cv2.matchTemplate(image_cv, template_cv, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8  # Ngưỡng để nhận diện hình ảnh con
        loc = np.where(result >= threshold)
        
        for pt in zip(*loc[::-1]):
            results.append({
                "type": "image",
                "x": int(pt[0]),
                "y": int(pt[1]),
                "width": template_cv.shape[1],
                "height": template_cv.shape[0]
            })
    
    return jsonify({
        "found": len(results) > 0,
        "matches": results
    })
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
