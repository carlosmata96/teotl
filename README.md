# Teotl
## API for recognition and comparation facial
### Introduction
> rest api service to detect faces, with the ability to detect similarities in two images with faces
## Create with
* python: version 3.6
* Flask 1.1.2
* face-recognition 1.3.0
## Installation

* python3 -m venv ./venv
* source venv/bin/activate
* pip3 install -r requirements.txt
* export FLASK_APP=main.py
* flask run

## Functions

> **/compareFaces** [POST]
>> compare two images to find facial similarities (with format Base64 JSON)
>> ### Parameters
>> * user_profile_picture : base 64 encode string of person
>> * user_webcam_photo : base 64 encode string imagen to compare

> **/compareFacesPath** [POST]
>> compare two images to find facial similarities (with format Path request file)
>> ### Parameters
>> * user_profile_picture : file of person
>> * user_webcam_photo : file imagen to compare

> **/detectFaces** [POST]
>> analyzes an image to detect faces (with format Path request file)
>> ### Parameters
>> * profile_picture : file imagen to search faces