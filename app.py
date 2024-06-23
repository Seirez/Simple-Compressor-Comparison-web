import os
import time
import gzip
import lzma
from flask import Flask, render_template, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['COMPRESSED_FOLDER'] = 'compressed'
app.config['DECOMPRESSED_FOLDER'] = 'decompressed'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['COMPRESSED_FOLDER'], exist_ok=True)
os.makedirs(app.config['DECOMPRESSED_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS_AUDIO = {'mp3', 'wav', 'ogg'}
ALLOWED_EXTENSIONS_IMAGE = {'jpg', 'jpeg', 'png', 'bmp'}
ALLOWED_EXTENSIONS_VIDEO = {'mp4', 'avi', 'mov'}
ALLOWED_EXTENSIONS_COMPRESSED = {'bin'}

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def compress_file(file_path, algorithm):
    with open(file_path, 'rb') as f_in:
        file_data = f_in.read()

    start_time = time.time()

    if algorithm == "gzip":
        compressed_data = gzip.compress(file_data)
    elif algorithm == "lzma":
        compressed_data = lzma.compress(file_data)
    else:
        raise ValueError("Unknown compression algorithm")

    elapsed_time = time.time() - start_time
    return compressed_data, elapsed_time

def decompress_file(file_path, algorithm):
    with open(file_path, 'rb') as f_in:
        compressed_data = f_in.read()

    start_time = time.time()

    if algorithm == "gzip":
        decompressed_data = gzip.decompress(compressed_data)
    elif algorithm == "lzma":
        decompressed_data = lzma.decompress(compressed_data)
    else:
        raise ValueError("Unknown decompression algorithm")

    elapsed_time = time.time() - start_time
    return decompressed_data, elapsed_time

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compress_audio', methods=['GET', 'POST'])
def compress_audio():
    if request.method == 'POST':
        file = request.files['file']
        algorithm = request.form['algorithm']

        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS_AUDIO):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            compressed_data, elapsed_time = compress_file(file_path, algorithm)
            compressed_filename = f"compressed_{filename}.bin"
            compressed_file_path = os.path.join(app.config['COMPRESSED_FOLDER'], compressed_filename)

            with open(compressed_file_path, 'wb') as f_out:
                f_out.write(compressed_data)

            file_size = len(compressed_data) / 1024

            return render_template('result.html', task="Audio Compression", elapsed_time=elapsed_time,
                                   file_size=file_size, download_url=url_for('download_file', filename=compressed_filename))

    return redirect(url_for('index'))

@app.route('/decompress_audio', methods=['GET', 'POST'])
def decompress_audio():
    if request.method == 'POST':
        file = request.files['file']
        algorithm = request.form['algorithm']

        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS_COMPRESSED):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            decompressed_data, elapsed_time = decompress_file(file_path, algorithm)
            decompressed_filename = f"decompressed_{filename}.wav"
            decompressed_file_path = os.path.join(app.config['DECOMPRESSED_FOLDER'], decompressed_filename)

            with open(decompressed_file_path, 'wb') as f_out:
                f_out.write(decompressed_data)

            file_size = len(decompressed_data) / 1024

            return render_template('result.html', task="Audio Decompression", elapsed_time=elapsed_time,
                                   file_size=file_size, download_url=url_for('download_file', filename=decompressed_filename))

    return redirect(url_for('index'))

@app.route('/compress_image', methods=['GET', 'POST'])
def compress_image():
    if request.method == 'POST':
        file = request.files['file']
        algorithm = request.form['algorithm']

        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS_IMAGE):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            compressed_data, elapsed_time = compress_file(file_path, algorithm)
            compressed_filename = f"compressed_{filename}.bin"
            compressed_file_path = os.path.join(app.config['COMPRESSED_FOLDER'], compressed_filename)

            with open(compressed_file_path, 'wb') as f_out:
                f_out.write(compressed_data)

            file_size = len(compressed_data) / 1024

            return render_template('result.html', task="Image Compression", elapsed_time=elapsed_time,
                                   file_size=file_size, download_url=url_for('download_file', filename=compressed_filename))

    return redirect(url_for('index'))

@app.route('/decompress_image', methods=['GET', 'POST'])
def decompress_image():
    if request.method == 'POST':
        file = request.files['file']
        algorithm = request.form['algorithm']

        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS_COMPRESSED):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            decompressed_data, elapsed_time = decompress_file(file_path, algorithm)
            decompressed_filename = f"decompressed_{filename}.jpg"
            decompressed_file_path = os.path.join(app.config['DECOMPRESSED_FOLDER'], decompressed_filename)

            with open(decompressed_file_path, 'wb') as f_out:
                f_out.write(decompressed_data)

            file_size = len(decompressed_data) / 1024

            return render_template('result.html', task="Image Decompression", elapsed_time=elapsed_time,
                                   file_size=file_size, download_url=url_for('download_file', filename=decompressed_filename))

    return redirect(url_for('index'))

@app.route('/compress_video', methods=['GET', 'POST'])
def compress_video():
    if request.method == 'POST':
        file = request.files['file']
        algorithm = request.form['algorithm']

        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS_VIDEO):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            compressed_data, elapsed_time = compress_file(file_path, algorithm)
            compressed_filename = f"compressed_{filename}.bin"
            compressed_file_path = os.path.join(app.config['COMPRESSED_FOLDER'], compressed_filename)

            with open(compressed_file_path, 'wb') as f_out:
                f_out.write(compressed_data)

            file_size = len(compressed_data) / 1024

            return render_template('result.html', task="Video Compression", elapsed_time=elapsed_time,
                                   file_size=file_size, download_url=url_for('download_file', filename=compressed_filename))

    return redirect(url_for('index'))

@app.route('/decompress_video', methods=['GET', 'POST'])
def decompress_video():
    if request.method == 'POST':
        file = request.files['file']
        algorithm = request.form['algorithm']

        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS_COMPRESSED):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            decompressed_data, elapsed_time = decompress_file(file_path, algorithm)
            decompressed_filename = f"decompressed_{filename}.mp4"
            decompressed_file_path = os.path.join(app.config['DECOMPRESSED_FOLDER'], decompressed_filename)

            with open(decompressed_file_path, 'wb') as f_out:
                f_out.write(decompressed_data)

            file_size = len(decompressed_data) / 1024

            return render_template('result.html', task="Video Decompression", elapsed_time=elapsed_time,
                                   file_size=file_size, download_url=url_for('download_file', filename=decompressed_filename))

    return redirect(url_for('index'))

@app.route('/download/<filename>')
def download_file(filename):
    if filename.startswith('compressed_'):
        folder = app.config['COMPRESSED_FOLDER']
    elif filename.startswith('decompressed_'):
        folder = app.config['DECOMPRESSED_FOLDER']
    else:
        folder = app.config['UPLOAD_FOLDER']
    return send_file(os.path.join(folder, filename), as_attachment=True, download_name=filename)

if __name__ == '__main__':
    app.run(debug=True)