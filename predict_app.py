import base64
import numpy as np
import io
from PIL import Image
import tensorflow as tf
import keras
from keras import backend as K
from keras.models import Sequential
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from flask import request
from flask import jsonify
from flask import Flask
import weakref
import os
#to disable tensorflow warning (press 'ctrl'+'/' after selecting these 7 lines)
#to prevent the warning : Allocation of 411041792 exceeds 10% of system memory.
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
#Just disables the warning, doesn't enable AVX/FMA 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
#keep_dims is deprecated, use keepdims instead
tf.logging.set_verbosity(tf.logging.ERROR)


app = Flask(__name__)

def get_model():
	global model,graph
	graph = tf.get_default_graph()
	model = load_model('VGG16_cats_and_dogs.h5')
	model._make_predict_function()
	print(" * Model Loaded!")

def preprocess_image(image, target_size):
	if image.mode != "RGB":
		image = image.convert("RGB")
	image = image.resize(target_size)
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)

	return image

print(" *Loading Keras model...")
get_model()

@app.route("/predict" , methods=["POST"])
def predict():
	message = request.get_json(force=True)
	encoded = message['image']
	decoded = base64.b64decode(encoded)
	image = Image.open(io.BytesIO(decoded))
	processed_image = preprocess_image(image , target_size=(224,224))

	with graph.as_default():
		prediction = model.predict(processed_image).tolist()
	response = {
		'prediction' : {
			'dog' : prediction[0][0],
			'cat' : prediction[0][1]
		}
	}
	return jsonify(response) 


# set FLASK_APP=predict_app.py
# flask run --host=0.0.0.0 