from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.utils.timezone import now
from .models import Scan
from .forms import ScanForm
import sys
from os import path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from record.models import ImageList
import math

# Create your views here.
def index(request):
    scan = Scan.objects.filter(id=16)[0]
    points = scan.points
    data = []
    angle = -45
    for count, point in enumerate(points):
        x = point * math.cos(math.radians(angle))
        y = point * math.sin(math.radians(angle))
        angle += 0.25
        if abs(x) < 10000 and abs(y) < 10000:
            data.append({'x': x, 'y': y})

    return render(request, 'lidar/lidar.html', {'scan': scan, 'data': data})

@csrf_exempt
def scan(request):
    if request.method == 'POST':
        form = ScanForm(request.POST, request.FILES)
        if form.is_valid():
            # name = form.cleaned_data['name']
            # date = form.cleaned_data['date']
            left_section = form.cleaned_data['left_section']
            right_section = form.cleaned_data['right_section']
            points = [float(point) for point in dict(request.POST)['points']]
            # print(points)

            left_image = ImageList.objects.filter(section__name=left_section).latest()
            right_image = ImageList.objects.filter(section__name=right_section).latest()
            scan = Scan(left_image=left_image, right_image=right_image, points=points)
            scan.save()
        else:
            print(form.errors)
            
    else:
        form = ScanForm()
        
    return render(request, 'lidar/lidar.html', {'form': ScanForm})