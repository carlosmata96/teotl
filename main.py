from flask import Flask, request, render_template
from PIL import Image
from base64 import b64decode
from re import sub
import face_recognition
from io import BytesIO
import logging
import numpy as np

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

app = Flask(__name__)
app.config.from_pyfile('config.py')

@app.route('/',methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/compareFaces', methods=['POST'])
def compareFaces():
    data = request.json
    if 'user_profile_picture' not in data:
        app.logger.error('Not photo profile')
        return 'False'
    if 'user_webcam_photo' not in data:
        app.logger.error('Not photo to Compare')
        return 'False'
    photoBase = sub('^data:image/.+;base64,', '', data['user_profile_picture'])
    photoComparation = sub('^data:image/.+;base64,', '', data['user_webcam_photo'])
    profile_image = __veryfyImg(face_recognition.load_image_file(BytesIO(b64decode(photoBase))))
    unknown_image = __veryfyImg(face_recognition.load_image_file(BytesIO(b64decode(photoComparation))))
    profile_face_location = face_recognition.face_locations(profile_image)
    if len(profile_face_location) == 0:
        profile_face_location = face_recognition.face_locations(profile_image, model='cnn')
    profile_encoding = face_recognition.face_encodings(profile_image, known_face_locations=profile_face_location)
    unknown_face_location = face_recognition.face_locations(unknown_image)
    if len(unknown_face_location) == 0:
        unknown_face_location = face_recognition.face_locations(unknown_image, model='cnn')
    if len(profile_encoding) == 0:
        app.logger.error('Face profile not found')
        return 'False'
    unknown_encoding = face_recognition.face_encodings(unknown_image, known_face_locations=unknown_face_location)
    if len(unknown_encoding) == 0:
        app.logger.error('Face to compare not found')
        return 'False'
    results = face_recognition.compare_faces(unknown_encoding, profile_encoding[0], app.config['TOLERANCE'])
    return str(results[0])


@app.route('/compareFacesPath', methods=['POST'])
def compareFacesPath():
    if 'user_profile_picture' not in request.files:
        app.logger.error('Not photo profile')
        return 'False'
    if 'user_webcam_photo' not in request.files:
        app.logger.error('Not photo to compare')
        return 'False'
    photoBase = request.files['user_profile_picture']
    photoComparation = request.files['user_webcam_photo']
    profile_image = __veryfyImg(face_recognition.load_image_file(photoBase))
    unknown_image = __veryfyImg(face_recognition.load_image_file(photoComparation))
    profile_face_location = face_recognition.face_locations(profile_image)
    if len(profile_face_location) == 0:
        profile_face_location = face_recognition.face_locations(profile_image, model='cnn')
    profile_encoding = face_recognition.face_encodings(profile_image, known_face_locations=profile_face_location)
    unknown_face_location = face_recognition.face_locations(unknown_image)
    if len(unknown_face_location) == 0:
        unknown_face_location = face_recognition.face_locations(unknown_image, model='cnn')
    unknown_encoding = face_recognition.face_encodings(unknown_image, known_face_locations=unknown_face_location)
    if len(profile_encoding) == 0:
        app.logger.error('Face profile not found')
        return 'False'
    if len(unknown_encoding) == 0:
        app.logger.error('Face to compare not found')
        return 'False'
    results = face_recognition.compare_faces(unknown_encoding, profile_encoding[0], app.config['TOLERANCE'])
    return str(results[0])


@app.route('/detectFace', methods=['POST'])
def detectFace():
    if 'profile_picture' not in request.files:
        app.logger.error('Image not found')
        return 'False'
    photoBase = request.files['profile_picture']
    known_image = face_recognition.load_image_file(photoBase)
    photo_face_location = __veryfyImg(face_recognition.face_locations(known_image))
    if len(photo_face_location) == 0:
        photo_face_location = face_recognition.face_locations(known_image, model='cnn')
    faces_encoding = face_recognition.face_encodings(known_image, known_face_locations=photo_face_location)
    if len(faces_encoding) == 0:
        app.logger.error('Face not found')
        return 'False'
    return 'True'


def __veryfyImg(array):
    sizeMin = app.config['SIZE_CONVERT']
    img = Image.fromarray(array)
    width, height = img.size
    diffWidth = width - sizeMin
    diffHeight = height - sizeMin
    if diffWidth > 0 or diffHeight > 0:
        if diffWidth > diffHeight:
            newWidth = sizeMin
            newHeight = (height * newWidth) / width
        else:
            newHeight = sizeMin
            newWidth = (width * newHeight) / height
        img = img.resize((int(newWidth), int(newHeight)))
    return np.array(img)
