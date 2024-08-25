import nltk
from nltk.corpus import wordnet as wn
import json
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS
import sqlite3
import os
import glob
import subprocess
import base64
import io
import pyheif
from PIL import Image

app = Flask(__name__)
CORS(app)

conn = sqlite3.connect('pictures.db', check_same_thread=False)
cursor = conn.cursor()

nltk.download('wordnet')
windows_image_path = "C:\\Users\\mycol\\Documents\\iphone-photos"
wsl_path = subprocess.check_output(['wslpath', windows_image_path]).decode().strip()
image_extensions = ["*.HEIC", "*.heic"]
img_paths = []

for ext in image_extensions:
    img_paths.extend(glob.glob(os.path.join(wsl_path, ext)))


with open("../nn-model/imagenet_class_index.json") as f:
    class_idx = json.load(f)

vocab_list = class_idx.keys() # get all the keys

def keyword_to_nearest_key(keyword):
    target_synsets = wn.synsets(keyword)
    word_list_synsets = [wn.synsets(word) for word in vocab_list]

    max_similarity = 0
    closest_word = None
    for word_synset in word_list_synsets:
        for target_synset in target_synsets:
            # print(word_synset)
            # print(target_synset)
            if len(word_synset) > 0:
                similarity = target_synset.wup_similarity(word_synset[0])
                if similarity > max_similarity:
                    max_similarity = similarity
                    closest_word = word_synset[0].lemmas()[0].name()
    
    print('closest word is ', closest_word, ' and the max similar is, ', max_similarity)
    return closest_word, max_similarity

def encode_image(image_path):
    # Read and convert the .heic file to a PIL image
    heif_file = pyheif.read(image_path)
    image = Image.frombytes(
        heif_file.mode, 
        heif_file.size, 
        heif_file.data, 
        "raw", 
        heif_file.mode, 
        heif_file.stride,
    )

    # Convert the PIL image to a bytes buffer
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")  # You can save it in other formats like PNG as well
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")

    return img_str

def queryImages(keyword):
    cursor.execute("SELECT * FROM images where keywords = (?)", (keyword, ))
    rows = cursor.fetchall()
    print(rows)
    return rows

@app.route('/get-images', methods=['GET'])
def queryImagesKeyword():
    keyword = request.args.get('keyword')
    if keyword not in vocab_list:
        keyword = keyword_to_nearest_key(keyword)

    rows = queryImages(keyword)
    matching_imgs = []

    for id, _ in rows:
        matching_img_path = os.path.join(wsl_path, img_paths[id - 1])
        if os.path.exists(matching_img_path) and matching_img_path.endswith('.heic'):
            encoded_image_path = encode_image(matching_img_path)

            matching_imgs.append({"path": encoded_image_path})

    return jsonify(matching_imgs), 200
    
if __name__ == '__main__':
    app.run(host='192.168.81.153', port=8080)


    


