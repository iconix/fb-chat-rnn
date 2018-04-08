# https://github.com/jrosebr1/simple-keras-rest-api

# USAGE
# Start the server:
# 	python run_keras_server.py
# Submit a request via cURL:
# 	curl -X POST -F image=@dog.jpg 'http://localhost:5000/predict'
# Submita a request via Python:
#	python simple_request.py

# import the necessary packages TODO:

import numpy as np
import flask
import io

# initialize our Flask application and the Keras model
app = flask.Flask(__name__)
model = None

def load_model():
	# load the pre-trained Keras model
	global model
	model = None # TODO:

def make_model(batch_size_override=None):
    if batch_size_override is None:
        batch_size_override = bs
    model = Sequential([
        Embedding(vocab_size, n_fac, input_length=nc, batch_input_shape=(batch_size_override,nc)),
        BatchNormalization(),
        LSTM(n_hidden, input_dim=n_fac, return_sequences=True, stateful=True, dropout_U=0.2, dropout_W=0.2,
             consume_less='gpu'),
        LSTM(n_hidden, input_dim=n_fac, return_sequences=True, stateful=True, dropout_U=0.2, dropout_W=0.2,
             consume_less='gpu'),
        TimeDistributed(Dense(n_hidden, activation='relu')),
        Dropout(0.2),
        TimeDistributed(Dense(vocab_size, activation='softmax'))
    ])
    model.compile(loss="sparse_categorical_crossentropy", optimizer=Adam())
    return model

def generate_conversation(m, seed, num_lines=5):
    pred_m = make_model(batch_size_override=1) # batch_size_override is the important bit
    for layer, pred_layer in zip(m.layers, pred_m.layers):
        pred_layer.set_weights(layer.get_weights())

    output = seed
    i = 0
    while i <= (num_lines*2):
        x = np.array([char_indices[c] for c in output[-nc:]])[np.newaxis,:]
        preds = pred_m.predict(x, verbose=0, batch_size=1)[0][-1]
        preds = preds / np.sum(preds)
        new_char = np.random.choice(chars, p=preds)
        output += new_char
        if new_char == '>':
            i += 1
    print(output)

@app.route("/predict", methods=["POST"])
def predict():
	# initialize the data dictionary that will be returned from the
	# view
	data = {"success": False}

	# ensure a json payload was properly uploaded to our endpoint
	if flask.request.method == "POST":
	    json = flask.request.get_json(force=True)
        # TODO: json should include: seed, num_lines (optional), valid characters (?)

        data["result"] = generate_conversation(seed, num_lines)
        data["success"] = True

	# return the data dictionary as a JSON response
	return flask.jsonify(data)

# if this is the main thread of execution first load the model and
# then start the server
if __name__ == "__main__":
	print(("* Loading Keras model and Flask starting server..."
		"please wait until server has fully started"))
	load_model()
	app.run()
