from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
import os
import numpy as np
from PIL import Image

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecrettodolistpassword1'
Bootstrap(app)


@app.route('/', methods=["GET", "POST"])
def home():

    return render_template("home.html")


@app.route('/image', methods=["GET", "POST"])
def image():
    file_path = request.files['file_path'].filename
    
    img = Image.open(file_path).convert('RGB')

    h,w = img.size
    print(img.size)

    img_colors = {}
    for pixel_h in range(h):
        for pixel_w in range(w):
            r,g,b = img.getpixel((pixel_h,pixel_w))
            pixel_color = "#{:02x}{:02x}{:02x}".format(r,g,b)
            if pixel_color not in img_colors:
                img_colors[pixel_color] = 1
            else:
                img_colors[pixel_color] +=1

     
    return render_template("image.html", file=file_path, colors=sorted(img_colors.items(), key = lambda x: x[1], reverse=True)[:10])

if __name__ == "__main__":
    app.run(debug=True)
