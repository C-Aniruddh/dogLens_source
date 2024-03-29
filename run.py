
from flask import Flask, render_template, url_for, request, session, redirect, send_from_directory
import os
from werkzeug.utils import secure_filename
import tensorflow as tf, sys
import json

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')

ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def hello():
    return "Hello World! -- Bow bow"

@app.route('/verify/<breed_name>&<file_name>', methods=['POST','GET'])
def verify(breed_name, file_name):
    directory_name = 'tf_files/dog_photos/%s' % (breed_name)
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    comm = 'cp static/uploads/%s tf_files/dog_photos/%s/%s' % (file_name, breed_name, file_name)
    os.system(comm)
    return json.dumps({'action' : 'success'})

@app.route('/new_breed/<breed_name>&<file_name>', methods=['POST', 'GET'])
def new_food(breed_name, file_name):
    directory_name = 'tf_files/dog_photos/%s' % (breed_name)
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    comm = 'cp static/uploads/%s tf_files/dog_photos/%s/%s' % (file_name, breed_name, file_name)
    os.system(comm)
    return json.dumps({'action' : 'success'})

@app.route('/submit', methods=['POST', 'GET'])
def submit():
    if request.method == 'POST':
        file = request.files['song_upload']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            fname = filename
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], fname)
            fname_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            download_link = '/downloads/%s' % fname
            image_data = tf.gfile.FastGFile(full_path, 'rb').read()
            # Loads label file, strips off carriage return
            label_lines = [line.rstrip() for line
                               in tf.gfile.GFile("tf_files/retrained_labels.txt")]
            # Unpersists graph from file
            with tf.gfile.FastGFile("tf_files/retrained_graph.pb", 'rb') as f:
                graph_def = tf.GraphDef()
                graph_def.ParseFromString(f.read())
                _ = tf.import_graph_def(graph_def, name='')

            with tf.Session() as sess:
                # Feed the image_data as input to the graph and get first prediction
                softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

                predictions = sess.run(softmax_tensor, \
                         {'DecodeJpeg/contents:0': image_data})

                # Sort to show labels of first prediction in order of confidence
                top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
                print top_k
                object_list = []
		object_score = []
                for node_id in top_k:
            	    print node_id
                    human_string = label_lines[node_id]
                    object_list.append(human_string)
            	    score = predictions[0][node_id]
		    object_score.append(score)
                    print('%s (score = %.5f)' % (human_string, score))
                print object_list
                print object_list[0]
                detected_dog = str(object_list[0])
   		if object_score[0] < 0.25:
		    detected_dog = 'Could not find a dog, please retry.'
		print detected_dog
		return json.dumps({'breed_detected': str(detected_dog), 'predict_one':str(object_list[1]), 'predict_two':str(object_list[2])})
    return render_template('submit.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=2409)
