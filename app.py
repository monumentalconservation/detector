from flask import Flask, jsonify, request
from model import get_prediction, batch_prediction
from service_streamer import ThreadedStreamer
from PIL import Image
import urllib.request

app = Flask(__name__)
streamer = ThreadedStreamer(batch_prediction, batch_size=64)

@app.route('/')
def hello_world():
    return 'Hello, World!'

    
@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        img_bytes = file.read()
        class_id, class_name = get_prediction(img_bytes)
        return jsonify({'class_id': class_id, 'class_name': class_name})


@app.route('/stream_predict', methods=['POST'])
def stream_predict():
    print('Stream predicting in progress!!')
    if request.method == 'POST':
        file = request.files['file']
        img_bytes = file.read()
        class_id, class_name = streamer.predict([img_bytes])[0]
        return jsonify({'class_id': class_id, 'class_name': class_name})


@app.route('/stream_url_predict', methods=['POST'])
def stream_url_predict():
    print('Stream predicting from url in progress!!')
    if request.method == 'POST':
        file_url = request.form.get('file_url')
        im = urllib.request.urlopen(file_url).read()

        class_id, class_name = streamer.predict([im])[0]
        return jsonify({'class_id': class_id, 'class_name': class_name})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)