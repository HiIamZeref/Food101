import torchvision.models as models
from torch import nn
import torch
from PIL import Image
from torchvision import transforms

class FoodClassifierModel():
    def __init__(self) -> None:
        model = models.densenet201(weights=None)
        classifier = nn.Sequential(
            nn.Linear(1920, 1024),
            nn.LeakyReLU(),
            nn.Linear(1024, 101),
        )
        model.classifier = classifier
        model.load_state_dict(torch.load('app/ai_models/food_101/food101-inception-model.pth', map_location=torch.device('cpu')))
        model.eval()
        self.model = model

        with open('app/ai_models/food_101/classes.txt', 'r') as f:
            self.labels = f.read().splitlines()

        print('Model loaded!')

    
    def predict(self, image: str):
        """

        Predict the class of the input image
        image: str, path to the image
        """
        # Opening image
        img = Image.open(image)

        # Transforming the image
        simple_transform = transforms.Compose([
            transforms.Resize((256, 256)),
            transforms.ToTensor(),
        ])

        img = simple_transform(img)

        # Adding batch dimension
        img = img.unsqueeze(0)

        # Making prediction
        with torch.inference_mode():
            # Forward pass
            output = self.model(img)

            # Getting probs
            probs = torch.nn.functional.softmax(output, dim=1)

            # Getting the top 5 classes (getting the top 5 probabilities and their classes its a suggestion from Copilot)
            top5_probs, top5_classes = torch.topk(probs, 5)

            # Getting the top 5 labels
            top5_labels = [self.labels[i] for i in top5_classes[0]]

            # Setting up the return dictionary
            response = {
                'top5_labels': top5_labels,
                'top5_probs': top5_probs[0].tolist()
            }

            return response


if __name__ == '__main__':
    model = FoodClassifierModel()
    response = model.predict('app/ai_models/food_101/pizza.jpeg')
    print(response)