#import gpt_2_simple as gpt2
import os
import requests
from Helpers.DatabaseAccessor import DatabaseAccessor
import pymongo

# Base model definition
MODEL_NAME = "124M"


def download_model():
    if not os.path.isdir(os.path.join("models", MODEL_NAME)):
        print(f"Downloading {MODEL_NAME} model...")
        gpt2.download_gpt2(model_name=MODEL_NAME)


def download_train_text(file_name):
    if not os.path.isfile(file_name):
        url = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
        data = requests.get(url)

        with open(file_name, 'w') as f:
            f.write(data.text)


def fine_train(session, file_name):
    # Steps is max number of training steps
    gpt2.finetune(session, file_name, model_name=MODEL_NAME, steps=1000)


def generate(session):
    gpt2.load_gpt2(session, model_name=MODEL_NAME)  # No needed if you has executed "fine training"
    gpt2.generate(session)

def database_connect():
    database = DatabaseAccessor('mongodb://localhost:27017/', 'test', 'testparrafos')
    database.connect()
    return database

def get_collection(database):
    return database.get_gollection().find({})

def write_txt_to_train(text, output_file_name = 'train.txt'):
    output_file = open(output_file_name, 'w')
    for paragraph in text:
        output_file.write(paragraph['texto'] + '\n')
    output_file.close()

database = database_connect()
collection = get_collection(database)
write_txt_to_train(collection)

download_model()
download_train_text("train.txt")

sess = gpt2.start_tf_sess()
fine_train(sess, "train.txt")
generate(sess)
