# face-recognition-co-workers

## How it works ?
The main core of this web service is the library provided by https://github.com/ageitgey/face_recognition  
This library provide face recognition powered by deep learning algorithm with a precision of 99.38%  

The WebService was built using Flask which is the simplest Web Framework.  
This WebService is runed in a Docker Container to avoid the constraint linked to the Face Recognition Library  

## Why not use a ready to go service ?
This would have greatly simplified the work however no free Webservice coresponded to our needs.  
The most know one AWS needed credential and the number of free request was limited and the option to have a database of faces was not that accessible.  
In the end if we choose a "free" ready to go service we should have spent a lot of time configuring.  

We decided to go with the most interesting option by creating one

## Flask Webservice  

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

