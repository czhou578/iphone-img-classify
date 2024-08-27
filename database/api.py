import nltk
from nltk.corpus import wordnet as wn
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os
import glob
import subprocess
import base64
import io
import pyheif
from PIL import Image
import os
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

load_dotenv()

conn = sqlite3.connect('pictures.db', check_same_thread=False)
cursor = conn.cursor()

nltk.download('wordnet')
windows_image_path = os.environ['FILE_PATH']
wsl_path = subprocess.check_output(['wslpath', windows_image_path]).decode().strip()
image_extensions = ["*.HEIC", "*.heic"]
img_paths = []

for ext in image_extensions:
    img_paths.extend(glob.glob(os.path.join(wsl_path, ext)))


with open("../nn-model/imagenet_class_index.json") as f:
    class_idx = json.load(f)

vocab_list = [] # get all the keys

for entry in class_idx.values():
    vocab_list.append(entry[1])

def semantic_similarity(word1, word2):
    synsets1 = wn.synsets(word1)
    synsets2 = wn.synsets(word2)
    
    max_similarity = 0
    
    for synset1 in synsets1:
        for synset2 in synsets2:
            similarity = synset1.path_similarity(synset2)
            if similarity and similarity > max_similarity:
                max_similarity = similarity
    
    return max_similarity

def keyword_to_nearest_key(target_word, word_list, top_n=1):
    similarities = [(word, semantic_similarity(target_word, word)) for word in word_list]
    similarities.sort(key=lambda x: x[1], reverse=True)
    print(similarities[:top_n])

    return similarities[:top_n][0]

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
    print('keyword in query', keyword)
    cursor.execute("SELECT * FROM images where keywords = (?)", (keyword, ))
    rows = cursor.fetchall()
    print(rows)
    return rows

# handle '0' result from similar words
@app.route('/get-images', methods=['GET'])
def queryImagesKeyword():
    keyword = request.args.get('keyword')
    if keyword not in vocab_list:
        keyword = keyword_to_nearest_key(keyword, vocab_list)
    
    print('keyword is, ', keyword)
    rows = queryImages(keyword)
    
    # rows = queryImages(keyword[0]) if type(keyword) is list or tuple else queryImages(keyword)
    matching_imgs = []

    for id, _ in rows:
        matching_img_path = os.path.join(wsl_path, img_paths[id - 1])
        if os.path.exists(matching_img_path) and (matching_img_path.endswith('.heic') or matching_img_path.endswith('.HEIC')):
            encoded_image_path = encode_image(matching_img_path)

            matching_imgs.append({"path": encoded_image_path})

    return jsonify(matching_imgs), 200
    
if __name__ == '__main__':
    app.run(host='192.168.81.153', port=8080)


    


