import json
import glob
import os
import requests
import shutil

from PIL import Image

FACE_DETECT_API = "https://westeurope.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceAttributes=age,gender,emotion"
SOURCE_DIR = 'images'
OUTPUT_DIR = 'output'

def getApiKey():
    with open('config.json', 'r') as f:
        settings = json.load(f)
    return settings['apiKey']

def fileNameWithoutExtension(filePath):
    return filePath.split(os.sep)[-1].split('.')[0]

def getFilesToProcess():
    files = glob.glob('{}/*.jpg'.format(SOURCE_DIR), recursive=False)
    return [(f, fileNameWithoutExtension(f)) for f in files]

def processFile(apiKey, inputFile):
    headers = {
        'Ocp-Apim-Subscription-Key': apiKey,
        'Content-Type': 'application/octet-stream'
    }
    data = open(inputFile, 'rb').read()
    res = requests.post(FACE_DETECT_API, data=data, headers=headers)
    return res.json()

def processFace(face, inputFile, outputFile):
    fr = face['faceRectangle']
    image = Image.open(inputFile)
    cropped = image.crop(
        (
            fr['left'],
            fr['top'],
            fr['left'] + fr['width'],
            fr['top'] + fr['height']
        )
    )
    cropped.save('{}/{}-{}.jpg'.format(OUTPUT_DIR, outputFile, face['faceId']), 'PNG')

def run():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.mkdir(OUTPUT_DIR)
    apiKey = getApiKey()
    files = getFilesToProcess()
    for file in files:
        faces = processFile(apiKey, file[0])
        for face in faces:
            processFace(face, file[0], file[1])

if __name__ == "__main__":
    run()
