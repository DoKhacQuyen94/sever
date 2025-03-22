@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    file = request.files['image']
    keyword = request.form.get('keyword')  # Lấy từ khóa cần tìm từ request
    image = Image.open(io.BytesIO(file.read()))

    # Trích xuất văn bản và tọa độ
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)

    results = []
    for i in range(len(data['text'])):
        text = data['text'][i].strip()
        if keyword and keyword.lower() in text.lower():  # Chỉ lấy text chứa keyword
            results.append({
                "text": text,
                "x": data['left'][i],
                "y": data['top'][i],
                "width": data['width'][i],
                "height": data['height'][i]
            })

    return jsonify(results)
