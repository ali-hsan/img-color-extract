from flask import Flask, render_template, request, flash, redirect
import os
from color_extracting import extract_dominant_colors
from PIL import Image

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = ['png', 'jpg', 'jpeg']


@app.route('/', methods=['GET', 'POST'])
def index():
    colors = extract_dominant_colors('static/uploads/default.jpg', 11)
    if request.method == "POST":

        if request.files:
            image = request.files["image"]

            try:
                image.save(os.path.join('static/uploads/', image.filename))
                
                # Optimize Image Before Saving
                picture = Image.open(f'static/uploads/{image.filename}')
                picture.thumbnail((530, 585))
                picture.save(f'static/uploads/{image.filename}')
            except IsADirectoryError:
                flash('Select an Image First!')
                return render_template('index.html', uploaded_image='uploads/default.jpg', colors=colors)

            colors = extract_dominant_colors(f'static/uploads/{image.filename}', 10)
            return render_template('index.html', uploaded_image=f'uploads/{image.filename}', colors=colors)

    # delete the files from upload folder after every revisit to home page
    total_files = os.listdir(os.path.join('static/uploads/'))
    for file in total_files:
        if file != 'default.jpg':
            os.remove(os.path.join(f'static/uploads/{file}'))

    return render_template('index.html', uploaded_image='uploads/default.jpg', colors=colors)



if __name__ == '__main__':
    app.run()
