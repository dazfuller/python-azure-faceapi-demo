import json
import glob
import os
import requests
import shutil

from PIL import Image, ImageDraw, ImageFont

FACE_DETECT_API = "https://westeurope.api.cognitive.microsoft.com/face/v1.0/detect?returnFaceAttributes=age,gender,emotion"
SOURCE_DIR = 'images'
OUTPUT_DIR = 'output'
FONT = ImageFont.truetype('/Library/Fonts/Microsoft/Consolas.ttf', 14)

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
    fa = face['faceAttributes']
    em = fa['emotion']
    faceInfo = 'Age: {}\nGender: {}\n\n'.format(fa['age'], fa['gender'])
    faceInfo += '\n'.join(['{}: {:.2f}%'.format(k, v * 100) for k, v in em.items()])
    cropped.thumbnail((180, 180))
    card = Image.new("RGB", (440, 240), "#FFFFFF")
    card.paste(cropped, (30, 30))
    draw = ImageDraw.Draw(card)
    draw.multiline_text((240, 30), faceInfo, fill=0, font=FONT)
    del draw
    card.save('{}/{}-{}.jpg'.format(OUTPUT_DIR, outputFile, face['faceId']), 'PNG')

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
