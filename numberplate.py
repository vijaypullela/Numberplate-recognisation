import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import cv2

app = Flask(__name__)
app.secret_key = "secret key"
UPLOAD_FOLDER = 'static/uploads/'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed')
        return render_template('upload.html', filename=filename)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route("/<filename>")
def display_image(filename):
    def rect(test_img, face):
        (x, y, w, h) = face
        cv2.rectangle(test_img, (x, y), (x + w, y + h), (255, 0, 0), thickness=2)
        image = test_img[y:y + h, x:x + w]
        print(filename[-3:])
        value=''
        if filename[-3:]=='jpg':
            value='png'
        if filename[-3:]=='png':
            value='jpg'
        print(f"static/uploads/{filename[:-3]}{value}")
        cv2.imwrite(f'static/uploads/{filename[:-3]}{value}',image)
        file=f'{filename[:-3]}{value}'
        return file

    test_img = cv2.imread(f"static/uploads/{filename}")
    grey_img = cv2.cvtColor(test_img, cv2.COLOR_BGR2GRAY)
    cascade = cv2.CascadeClassifier(r'C:\Users\ajay\PycharmProjects\file\numberplate.xml')
    face = cascade.detectMultiScale(grey_img, scaleFactor=1.09, minNeighbors=1)
    try:
        for i in face:
            file=rect(test_img, i)
            return redirect(url_for('static', filename='uploads/' + file))  # , code=301)
    except:
        print('Number plate not found')
    print('display_image filename: ' )

if __name__ == "__main__":
    app.debug=True
    app.run()
