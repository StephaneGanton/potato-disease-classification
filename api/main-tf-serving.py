from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image # used to read image in python
import tensorflow as tf
import requests


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Global variables
TF_PORT = 8501 #CHANGE PORT NUMBER ACCORDINGLY

endpoint = "http://localhost:8501/v1/models/potato_disease_model:predict" # will use latest version 

CLASS_NAMES = ['Early Blight', 'Late Blight', 'healthy']


@app.get("/ping")
async def ping():
    return "Hi, server running !"

@app.post("/predict")
async def predict( file:UploadFile = File() ):
    
    np_arrayed_image = image_to_numpy_array(await file.read())
    batch_img = np.expand_dims(np_arrayed_image, 0)
    
    json_data = {
        "instances" : batch_img.tolist()
    }

    response = requests.post(endpoint, json = json_data )
    
    prediction = np.array(response.json()["predictions"][0])

    index = np.argmax(prediction)
    predicted_class = CLASS_NAMES[index]
    confidence = np.max(prediction)

    return { "class": predicted_class, "confidence": float(confidence) }


def image_to_numpy_array (data)->np.ndarray:
    pil_image = Image.open(BytesIO(data))
    np_image = np.array(pil_image)

    return np_image


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=9000)