import "./App.css";
import { useState } from "react";
import { makePrediction } from "./services/FoodClassifierApi";

function App() {
  const [image, setImage] = useState(null);
  const [imageUrl, setImageUrl] = useState(null);
  const [predictionData, setPredictionData] = useState(null);

  const onImageChange = (event) => {
    const selectedImage = event.target.files[0];
    setImage(selectedImage);
    const imageUrl = URL.createObjectURL(selectedImage);
    setImageUrl(imageUrl);
  };

  const handleFileUpload = () => {
    const imageForm = new FormData();
    imageForm.append("image", image);

    makePrediction(imageForm).then((response) => {
      const responseData = response.data;

      setPredictionData(responseData);
    });
  };
  return (
    <>
      <div>
        <h1>Food Prediction App!</h1>
        <h2>
          This is a simple food prediction app built with React + Typescript and
          Flask + Python.
        </h2>
        <h2>
          The app predicts the type of food based on the image you upload.
        </h2>
        <input type="file" accept="image/*" onChange={onImageChange} />
        <button onClick={handleFileUpload}>Make prediction!</button>
        {imageUrl && (
          <img
            src={imageUrl}
            alt="food"
            style={{ maxHeight: "300px", maxWidth: "300px" }}
          />
        )}
        {predictionData && (
          <div>
            <h2>
              The food in the image is:{" "}
              <strong>{predictionData.top5_labels[0]}</strong>
            </h2>
            <h2>
              Probability:{" "}
              <strong>
                {(predictionData.top5_probs[0] * 100).toFixed(2)}%
              </strong>
            </h2>
          </div>
        )}
      </div>
    </>
  );
}

export default App;
