# face-recognition-co-workers
By Shraddha, DaiQiao and Paul

# How it works ?
The main core of this web service is the library provided by https://github.com/ageitgey/face_recognition  
This library provide face recognition powered by deep learning algorithm with a precision of 99.38%  

The WebService was built using Flask which is the simplest Web Framework.  
This WebService is runed in a Docker Container to avoid the constraint linked to the Face Recognition Library

To run it locally you need to install docker (https://docs.docker.com/get-docker/)  

Clone this repository
```shell
git clone https://github.com/go-roots/face-recognition-co-workers.git
```
```shell
cd face-recognition-co-workers
```
Build the Docker Image (It take a few minutes)
```shell
docker build -t face-recognition-co-workers:init .
```
Run the WebService on localhost:5000
```shell
docker run -d -p 5000:5000 face-recognition-co-workers:init
```

# Why not use a ready to go service ?
This would have greatly simplified the work however no free Webservice coresponded to our needs.  
The most know one AWS needed credential and the number of free request was limited and the option to have a database of faces was not that accessible.  
In the end if we choose a "free" ready to go service we should have spent a lot of time configuring.  

We decided to go with the most interesting option by creating one

## Constraints
Quite a few constraints have been balanced with this WebService.  
The Face-Recognition is quite heavy with a lot of dependencies and consume a lot of memory to run making it complicated to process complicate task for small computers such as Raspberry Pi.
It only work on Unix environment set up with precise libraries so it was decided to use Docker to work with a stable environment.

## Communication with the Co-Workers API
The WebService work with the CO-Workers API (NodeJs) that handle security and ensure consistency in the DataBase. To connect this API a Admin Token is needed.  


## Usages  
The web service for Face Recognition   
The web service is host on http://206.189.55.55/   
It handle 2 route  

### GET http://206.189.55.55/

It load the image from the MongoDb database and encode them.   
It is a costly operation and it is not needed to do it often.   
The query take ~30 seconds to answer

### POST http://206.189.55.55/?room=<NAME of the ROOM\>

This post request take in Parameter the <NAME of the ROOM\> that detected the faces.   
It also take a img file which is the photo to process in the file of the HTTP request.
It return the user who moved and to which room.

