from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
import os
import libs.cv2 as cv2
from voiceid.sr import Voiceid
from voiceid.db import GMMVoiceDB


@api_view(['GET'])
def ping(request):
	return Response({'message':'Welcome to Vive Forensics.'})

@api_view(['POST'])
def whosefaceisinthis(request):
	image = request.data['image']
	with open(os.path.join(settings.MEDIA_ROOT,str(image)),'wb+') as destination:
		for chunk in image.chunks():
			destination.write(chunk)
	faceCascade = cv2.CascadeClassifier(os.path.join(settings.STATIC_ROOT,'haarcascade_frontalface_default.xml'))
	image = cv2.imread(os.path.join(settings.MEDIA_ROOT,str(image)))
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	faces = faceCascade.detectMultiScale(
	    gray,
	    scaleFactor=1.2,
	    minNeighbors=5,
	    minSize=(30, 30),
	    flags = cv2.cv.CV_HAAR_SCALE_IMAGE
	)
	print 
	for (x, y, w, h) in faces:
		cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
	face_count = len(faces)
	message = 'Found {0} face{1}!'.format(face_count,'' if face_count ==1 else 's' )
	return Response({'message': message	})

@api_view(['POST'])
def whosevoiceisinthis(request):
	audio = request.data['audio']
	db = GMMVoiceDB(os.path.join(settings.STATIC_ROOT,'voicedb'))
	with open(os.path.join(settings.MEDIA_ROOT,str(audio)),'wb+') as destination:
		for chunk in audio.chunks():
			destination.write(chunk)
	v = Voiceid(db, os.path.join(settings.MEDIA_ROOT,str(audio)))
	v.extract_speakers()
	voice_count = 0
	for c in v.get_clusters():
		voice_count += 1
	message = 'Found {0} voice{1}!'.format(voice_count,'' if voice_count ==1 else 's' )
	return Response({'message': message	})

@api_view(['POST'])
def whosefingerprintisinthis(request):
	image = request.data['image']
	with open(os.path.join(settings.MEDIA_ROOT,str(image)),'wb+') as destination:
		for chunk in image.chunks():
			destination.write(image)
	return Response({'message': 'Found your voice' 	})

@api_view(['GET'])
def whosecarisinthis(request):
	print request.data
	return Response({'message': 'Found your voice' 	})
