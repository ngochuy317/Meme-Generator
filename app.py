import random
import os
import requests
from flask import Flask, render_template, abort, request
from QuoteEngine import Ingestor
from QuoteEngine.ingestor_interface import QuoteModel
from MemeGenerator import MemeEngine

# @TODO Import your Ingestor and MemeEngine classes

app = Flask(__name__)

meme = MemeEngine('./static')


def setup():
    """ Load all resources """

    quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                   './_data/DogQuotes/DogQuotesDOCX.docx',
                   './_data/DogQuotes/DogQuotesPDF.pdf',
                   './_data/DogQuotes/DogQuotesCSV.csv']

    # TODO: Use the Ingestor class to parse all files in the
    # quote_files variable
    quotes = []
    for f in quote_files:
        quotes.extend(Ingestor.parse(f))

    images_path = "./_data/photos/dog/"

    # TODO: Use the pythons standard library os class to find all
    # images within the images images_path directory
    imgs = []
    for file in os.listdir(images_path):
        if file.endswith(".jpg"):
            imgs.append(os.path.join(images_path, file))

    return quotes, imgs


quotes, imgs = setup()


@app.route('/')
def meme_rand():
    """ Generate a random meme """

    # @TODO:
    # Use the random python standard library class to:
    # 1. select a random image from imgs array
    # 2. select a random quote from the quotes array

    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.body, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """ User input for meme information """
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """ Create a user defined meme """

    # @TODO:
    # 1. Use requests to save the image from the image_url
    #    form param to a temp local file.
    # 2. Use the meme object to generate a meme using this temp
    #    file and the body and author form paramaters.
    # 3. Remove the temporary saved image.

    image_url = request.form["image_url"]
    if not image_url:
        return render_template('meme_form.html')

    try:
        r = requests.get(image_url, verify=False)
        tmp = f'./tmp/{random.randint(0,100000000)}.png'
        with open(tmp, 'wb') as open_file:
            open_file.write(r.content)
            body = request.form["body"]
            if body is None:
                quote_files = [
                    './_data/DogQuotes/DogQuotesTXT.txt',
                    './_data/DogQuotes/DogQuotesDOCX.docx',
                    './_data/DogQuotes/DogQuotesPDF.pdf',
                    './_data/DogQuotes/DogQuotesCSV.csv'
                ]
                quotes = []
                for f in quote_files:
                    quotes.extend(Ingestor.parse(f))
                quote = random.choice(quotes)
            else:
                quote = QuoteModel(body, request.form["author"])
            path = meme.make_meme(tmp, quote.body, quote.author)
            os.remove(tmp)
            return render_template('meme.html', path=path)
    except Exception as e:
        print(f"Has Error when saving image| {e}")
        return render_template('meme_form.html')


if __name__ == "__main__":
    app.run()
