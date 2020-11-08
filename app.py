# This is the web service to update position based on the pictures send by the differents pictures send by the captors in the building

# Face recognition alo used https://github.com/ageitgey/face_recognition
import face_recognition

# For the HTTP requests on the API 
import requests 

#For file handling
import os
import sys
import json
from io import open as iopen

from flask import Flask, jsonify, request, redirect, Response

app = Flask(__name__)

# Global Variables

# All type of image that can be send
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# All the encoded user images
ENCODED_USR_IMG = []

#Token to use the Go-Roots API
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjVkN2E1MTRiNWQyYzEyYzc0NDliZTA0NiIsImlhdCI6MTYwNDQxMTkzMiwiZXhwIjoxNjA5NTk1OTMyfQ.9cQCiTr0BTcbciw5iPxNz-2S2SKflfR9hPJ4Zu7n728"

#Load and encrypt the images of the DB
def loadImages():
    print("Loading the files", file=sys.stderr)
    
    # Request to gat all the USERS in the app
    r = requests.get('https://co-workers.herokuapp.com/api/cw-api/profiles', headers={'Authorization': 'Bearer '+TOKEN})
    rep = r.json()
    
    for x in rep['data']:
       
        #Prepare the saving of the image 
        o = x['photo'].split('/')
        src = o[-1]

        #Query to obtain the file img
        i = requests.get(x['photo'], stream = True)
    
        #Save the img
        with iopen(src, 'wb') as file:
            file.write(i.content)

        #Load the saved img with face-recognition
        img = face_recognition.load_image_file(src)
        
        #Array of all the faces found in the img (normally one)
        allRecFace = face_recognition.face_encodings(img)

        #If a face is recognised
        if (len(allRecFace) > 0):
            #Add to ENCODED_USR_IMG the user and his img
            img_encoded = face_recognition.face_encodings(img)[0]  
            ENCODED_USR_IMG.append({'user':x['user'], 'img':img_encoded})
        else:
            #Put NULL in the img
            ENCODED_USR_IMG.append({'user':x['user'], 'img':'null'})

    #To test the encoding
    #print("ENCODED_USR_IMG - loadImg", file=sys.stderr)
    #print(ENCODED_USR_IMG, file=sys.stderr)


# Check if the file is a img
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Check if the image contain users, return the list of user found in img
def find_users_in_image(file_stream):
    #Array of the users founds in file_stream
    found_users = []
    # Load the uploaded image file
    img = face_recognition.load_image_file(file_stream)
    # Get face encodings for any faces in the uploaded image
    unknown_face_encodings = face_recognition.face_encodings(img)
    #print("Starting the matching", file=sys.stderr)

    if len(unknown_face_encodings) > 0:
        #Go by all the person in the picture
        for i in range(0,len(unknown_face_encodings)):
            #Check in the encoded user
            for j in ENCODED_USR_IMG:
                #print("Searching in db", file=sys.stderr)
                
                #Compare only if there an human in img
                if(j['img']!='null'):
                    match_results = face_recognition.compare_faces([j['img']], unknown_face_encodings[i])
                    #There a match we add to found user !
                    if match_results[0] == True:
                        #print("found matches", file=sys.stderr)
                        usrId = j['user']
                        found_users.append({"user":usrId})

    #Cast the String of oject to JSON
    return found_users
    
#Update the position based on identification
def update_position(room, user_list):
    endpoint = "https://co-workers.herokuapp.com/api/cw-api/rooms/moveIn/" + room
    data = {"users" : user_list}
    #header = {"Authorization": "Bearer "+TOKEN}
    #print("endpoint", file=sys.stderr)
    #print(endpoint, file=sys.stderr)
    #print("data", file=sys.stderr)
    #print(data, file=sys.stderr)
    r = requests.put(endpoint, headers={'Authorization': 'Bearer '+TOKEN}, json=data)
    return r


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    #Route to test an img send by the sensor
    if request.method == 'POST':
        #File is the img send by the sensor
        file = request.files['file']
        room = request.args.get('room')
        #If the file is conform
        if file and allowed_file(file.filename):
            #The image file seems valid detect faces
            users = find_users_in_image(file)
            #print({"users": users}, file=sys.stderr)
            r = update_position(room, users)
            #print(r, file=sys.stderr)
            return jsonify({"users":users, "room": room})

        #Throw error
        else:
            return 'Error file'

    # The GET route load the images
    if request.method == 'GET':
        loadImages()
        return '''
        Loading Images of the Database
        '''




if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
    loadImages()