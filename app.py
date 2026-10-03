from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
# use
import keras
import numpy as np
from PIL import Image
import base64
import io

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template("index.html")


model = keras.Sequential([
    keras.layers.Conv2D(
        32, (3, 3),
        activation='relu',
        input_shape=(28, 28, 1)
    ),

    keras.layers.MaxPooling2D(2, 2),

    keras.layers.Conv2D(
        64, (3, 3),
        activation='relu'
    ),

    keras.layers.MaxPooling2D(2, 2),

    keras.layers.Flatten(),

    keras.layers.Dense(120, activation='relu'),

    keras.layers.Dropout(0.2),

    keras.layers.Dense(10, activation='softmax')
])

def preprocess_canvas_image(pil_image):
    img = pil_image.convert('L')
    img_array = np.array(img)

    coords = np.argwhere(img_array < 235)
    y0, x0 = coords.min(axis=0)
    y1, x1 = coords.max(axis=0) + 1

    cropped = img_array[y0:y1, x0:x1]
    cropped_img = Image.fromarray(cropped)

    h, w = cropped.shape
    if h > w:
        new_h = 20
        new_w = max(1, int(w * (20 / h)))
    else:
        new_w = 20
        new_h = max(1, int(h * (20 / w)))
    resized = cropped_img.resize((new_w, new_h))

    final = Image.new('L', (28, 28), 255)
    paste_x = (28 - new_w) // 2
    paste_y = (28 - new_h) // 2
    final.paste(resized, (paste_x, paste_y))

    final.save("new.png")

    final_array = 255 - np.array(final).astype('float32')
    final_array = final_array / 255.0
    return final_array.reshape(1, 28, 28, 1)



model.load_weights("mnist_cnn.weights.h5")


@app.route('/predict', methods=["POST"])
def predict():
    data = request.get_json()
    image_data = data["imageData"]
    image_data = image_data.split(",")[1]

    image_bytes = base64.b64decode(image_data)
    image = Image.open(io.BytesIO(image_bytes))

    image = preprocess_canvas_image(image)

    prediction = model.predict(image)

    predicted_digit = np.argmax(prediction)
    confidence = np.max(prediction)

    return jsonify({
        "Prediction": int(predicted_digit),
        "Probability": float(confidence)
    })


if __name__ == "__main__":
    app.run(debug=True, port=5001)



















# IF WE SENT THE IMAGE TO THE JS

# def predict():
#     image_file = request.files['image'] # collecting
#     image = Image.open(image_file) # opening
#     image = image.convert('L') # gray scaling
#     image = image.resize((28, 28)) # reshaping to required dimensions

#     # here CNN EXPECTS (1, 28, 28,1 ) S0

#     image = np.array(image) # taking the image as a numpy array
#     image = image/255.0 # like normalizing the pixels
#     image = image.reshape(-1, 28, 28, 1)

#     prediction = model.predict(image) # It gives

#     # index:        0    1    2    3    4    5    6    7    8    9
#     # probability: .01  .02  .01  .03  .02  .05  .80  .03  .02  .01

#     predicted_digit = np.argmax(prediction) # takes the index 6
#     confidence = np.max(prediction) # takes the probability 0.8

#     return jsonify({
#         "Prediction" : int(predicted_digit),
#         "Probability" : float(confidence)
#     })


