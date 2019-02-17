from django.shortcuts import render
from django.http import HttpResponse
import os
from .models import ImagesForDraw
from django.conf import settings
# Create your views here.

def loadImage(request):

    return render(request, 'loadImage.html')

def upload_image(request):

    file_obj = request.FILES.get('imageFile01')
    obj = ImagesForDraw(image=file_obj)
    obj.save()
    mid = obj.image.url
    print(mid)
    context = {
        'images': mid
    }
    return render(request, 'draw.html', context)
