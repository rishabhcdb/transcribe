from flask import Flask, render_template, request, jsonify
import whisper
import os

app = Flask(__name__)

# Load Whisper model once
model = whisper.load_model("base")

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if 'audio' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['audio']
    filepath = os.path.join("uploads", file.filename)
    os.makedirs("uploads", exist_ok=True)
    file.save(filepath)

    # Transcribe
    result = model.transcribe(filepath)
    os.remove(filepath)  # cleanup

    return jsonify({'text': result['text']})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
