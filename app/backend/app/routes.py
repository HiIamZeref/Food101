from flask import Flask, request, jsonify
from ai_models.food_101.model import FoodClassifierModel
from PIL import Image
from flask_cors import CORS

# Instantiating the model
model = FoodClassifierModel()

# Instantiating the Flask app
app = Flask(__name__)
CORS(app)

@app.route('/make_predictions', methods=['POST'])
def make_predictions():
    # Check if the image exists in the request
    if 'image' not in request.files:
        return jsonify({'error': 'No image found in the request'}), 400
    
    # Getting the image
    image = request.files['image']

    # Making predictions
    predictions = model.predict(image)

    # Printing the predictions
    print(predictions)

    # Returning the predictions
    return jsonify(predictions), 200

if __name__ == '__main__':
    app.run(debug=True)