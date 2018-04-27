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

def get_api_key():
    with open('config.json', 'r') as f:
        settings = json.load(f)
    return settings['apiKey']

def filename_without_extension(filepath):
    return filepath.split(os.sep)[-1].split('.')[0]

def get_files_to_process():
    files = glob.glob('{}/*.jpg'.format(SOURCE_DIR), recursive=False)
    return [(f, filename_without_extension(f)) for f in files]

def process_file(api_key, input_file):
    headers = {
        'Ocp-Apim-Subscription-Key': api_key,
        'Content-Type': 'application/octet-stream'
    }
    data = open(input_file, 'rb').read()
    res = requests.post(FACE_DETECT_API, data=data, headers=headers)
    return res.json()

def process_face(face, input_file, output_file):
    fr = face['faceRectangle']
    image = Image.open(input_file)
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
    file_info = 'Age: {}\nGender: {}\n\n'.format(fa['age'], fa['gender'])
    file_info += '\n'.join(['{}: {:.2f}%'.format(k, v * 100) for k, v in em.items()])
    cropped.thumbnail((180, 180))
    card = Image.new("RGB", (440, 240), "#FFFFFF")
    card.paste(cropped, (30, 30))
    draw = ImageDraw.Draw(card)
    draw.multiline_text((240, 30), file_info, fill=0, font=FONT)
    del draw
    card.save('{}/{}-{}.png'.format(OUTPUT_DIR, output_file, face['faceId']), 'PNG')

def run():
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.mkdir(OUTPUT_DIR)
    api_key = get_api_key()
    files = get_files_to_process()
    for file in files:
        faces = process_file(api_key, file[0])
        for face in faces:
            process_face(face, file[0], file[1])

if __name__ == "__main__":
    run()
