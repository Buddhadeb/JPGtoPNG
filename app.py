from flask import Flask, render_template, request, send_file, jsonify
from PIL import Image
import io
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    conversion_type = request.form.get('conversion_type', '')

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Only JPG and PNG files are allowed'}), 400

    try:
        img = Image.open(file.stream)
        output = io.BytesIO()

        if conversion_type == 'jpg_to_png':
            # Convert to RGBA if needed for PNG transparency support
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                img = img.convert('RGBA')
            else:
                img = img.convert('RGB')
            img.save(output, format='PNG', optimize=True)
            output.seek(0)
            download_name = os.path.splitext(file.filename)[0] + '.png'
            mimetype = 'image/png'

        elif conversion_type == 'png_to_jpg':
            # Flatten transparency onto white background for JPG
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'P':
                    img = img.convert('RGBA')
                if img.mode in ('RGBA', 'LA'):
                    background.paste(img, mask=img.split()[-1])
                else:
                    background.paste(img)
                img = background
            else:
                img = img.convert('RGB')
            img.save(output, format='JPEG', quality=95, optimize=True)
            output.seek(0)
            download_name = os.path.splitext(file.filename)[0] + '.jpg'
            mimetype = 'image/jpeg'
        else:
            return jsonify({'error': 'Invalid conversion type'}), 400

        return send_file(
            output,
            mimetype=mimetype,
            as_attachment=True,
            download_name=download_name
        )

    except Exception as e:
        return jsonify({'error': f'Conversion failed: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
