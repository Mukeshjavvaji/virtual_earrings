from django.shortcuts import render
import cv2
import cvzone

from virtual_earring.settings import BASE_DIR

face_n = 1
earring_n = 1

# Create your views here.
def index(request):
    message = {'face': face_n, 'earring': earring_n}
    return render(request, 'index.html', message)

def display(request, fn, en):
    face_n = fn
    earring_n = en
    print(fn ,en)
    face = 'static/images/face_' + str(fn) + '.jpg'
    earring = 'static/images/earring_' + str(en) + '.png'
    cap = cv2.imread(face)
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    NoseCascade = cv2.CascadeClassifier('earrings/nariz.xml')
    overlay = cv2.imread(earring, cv2.IMREAD_UNCHANGED)

    gray_scale = cv2.cvtColor(cap, cv2.COLOR_BGR2GRAY)
    face_features = faceCascade.detectMultiScale(gray_scale, 1.1, 10)
    approx = face_features[0][1] + face_features[0][3] // 2

    for (x, y, w, h) in face_features:
        coords = [x, y, w, h]
    
    nose_features = NoseCascade.detectMultiScale(gray_scale, 1.1, 4)
    overlay_resize = cv2.resize(overlay, (int(coords[2]//5), int(coords[3]//5)))
    reduction = (coords[2]//5)//2
    for (x, y, w, h) in nose_features:
        if y in range(approx-10, approx+10):
            left_coordinate = ((((x + (w//2))-coords[2]//2)+5)-reduction, y+h-10)
            right_coordinate = ((((x + (w//2))+coords[2]//2)-5)-reduction, y+h-10)
            cap = cvzone.overlayPNG(cap, overlay_resize, left_coordinate)
            cap = cvzone.overlayPNG(cap, overlay_resize, right_coordinate)
    location = 'static/images/cv2_image.jpg'
    cv2.imwrite(location, cap)
    message = {'face': face_n, 'earring': earring_n}
    return render(request, 'index.html', message)