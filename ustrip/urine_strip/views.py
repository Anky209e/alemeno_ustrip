from django.shortcuts import render
from django.http import HttpResponse
import json
import cv2
from .models import UStrip
import numpy as np
from rest_framework import viewsets,views,generics
from .serializers import UStripSerializer

def analyze_colors(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    analyzed_colors = {}

    if len(contours) >= 10:
        sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
        sorted_contours = sorted(sorted_contours, key=lambda c: cv2.boundingRect(c)[0])

        for i, contour in enumerate(sorted_contours):
            x, y, w, h = cv2.boundingRect(contour)
            color_roi = image[y:y + h, x:x + w]
            pixel_color = color_roi[0, 0]

            color_name = ['Urobilinogen', 'Bilirubin', 'Ketones', 'Blood', 'Protein', 'Nitrite', 'Leukocytes', 'Glucose', 'Specific Gravity', 'pH'][i]
            rgb_values = [int(pixel_color[2]), int(pixel_color[1]), int(pixel_color[0])]

            analyzed_colors[color_name] = rgb_values

    return analyzed_colors

def index(request):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        
        img = cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        
        analyzed_colors = analyze_colors(img)
        urine_strip = UStrip(image=image, colors=analyzed_colors)
        urine_strip.save()
        return render(request, 'index.html', {'analyzed_colors': analyzed_colors})
    return render(request, 'index.html')

class UStripViewSet(generics.ListAPIView):
    queryset = UStrip.objects.all()
    serializer_class = UStripSerializer

    def post(self,request,*args,**kwargs):
        file = request.data['file']
        img = cv2.imdecode(np.fromstring(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        analyzed_colors = analyze_colors(img)
        urine_strip = UStrip(image=file, colors=analyzed_colors)
        urine_strip.save()
        return HttpResponse(json.dumps(analyzed_colors),status=200)