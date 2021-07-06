from flask import Flask, render_template, request, flash, redirect
import os
from color_extracting import extract_dominant_colors
import pyperclip

app = Flask(__name__)
app.config['SECRET_KEY'] = '//////'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['ALLOWED_EXTENSIONS'] = ['png', 'jpg', 'jpeg']


@app.route('/', methods=['GET', 'POST'])
def index():
    colors = extract_dominant_colors('static/uploads/default.jpg', 10)
    if request.method == "POST":

        if request.files:
            image = request.files["image"]

            try:
                image.save(os.path.join('static/uploads/', image.filename))
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


@app.route('/to_clipboard/<color>')
def to_clipboard(color):
    pyperclip.copy(f'#{color}')
    return redirect('/')


if __name__ == '__main__':
    app.run()
