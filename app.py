from flask import Flask, render_template, request, jsonify
import whisper

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    # Save the file temporarily
    filepath = f'temp_audio_{file.filename}'
    file.save(filepath)

    # Transcribe using Whisper
    model = whisper.load_model("base")
    result = model.transcribe(filepath)

    return jsonify({'text': result['text']})

if __name__ == '__main__':
    app.run(debug=True)
