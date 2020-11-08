# face-recognition-co-workers
The web service for Face Recognition   
The web service is host on http://206.189.55.55/   
It handle 2 route  
## GET http://206.189.55.55/

It load the image from the database and encode them   
It is a costly operation and it is not needed to do it often   

## POST http://206.189.55.55/?room=<NAME of the ROOM\>
This post request take in Parameter the <NAME of the ROOM\> that detected the faces   
It also take a img file which is the photo to process in the file of the HTTP request
