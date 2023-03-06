from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from datetime import date, datetime, time
import PyPDF2
from google.cloud import texttospeech
from google.cloud import storage
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:\directed-beacon-372206-8321d370824f.json"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'xxxxxxxxxx'
Bootstrap(app)


@app.route('/', methods=["GET", "POST"])
def home():

    return render_template("home.html")


@app.route('/player', methods=["GET", "POST"])
def player():

  
    file_path = request.files['file_path'].filename

    pdffile = open(file_path, 'rb')
    pdfreader = PyPDF2.PdfFileReader(pdffile)
    pages = pdfreader.numPages
    pageobj = pdfreader.getPage(0)
    text = pageobj.extractText()

       
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.OGG_OPUS)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    # The response's audio_content is binary.
    with open("static/audio/output.ogg", "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "output.ogg"')

    return render_template("player.html", text=text, file=file_path)

if __name__ == "__main__":
    app.run(debug=True)
