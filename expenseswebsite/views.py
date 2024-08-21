import datetime
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from authentication.models import About, Profile
from barcode import Code128
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import cloudinary.uploader

@login_required(login_url='/login')
def index(request): 
    user = request.user
    barcode_io = BytesIO()
    barcode =Code128(user.username, writer=ImageWriter())
    barcode.default_writer_options['write_text'] =False
    barcode.write(barcode_io)
    
    barcode_path = f'barcodes/{user.username}.png'
    default_storage.save(barcode_path, ContentFile(barcode_io.getvalue()))
    
    about_us = About.objects.all()
    context={
        'about_company': about_us,
        'barcode_url': default_storage.url(barcode_path),
    }  
    return render (request, 'index.html', context)


# # Load image from Cloudinary
# @login_required(login_url='/login')
# def index(request): 
#     user = request.user
#     barcode_io = BytesIO()
#     barcode =Code128(user.username, writer=ImageWriter())
#     barcode.default_writer_options['write_text'] =False
#     barcode.write(barcode_io)
#     barcode_io.seek(0)
#     response = cloudinary.uploader.upload(barcode_io, public_id=f"barcodes/{user.username}", format="png")
#     barcode_url = response['secure_url']
#     about_us = About.objects.all()
#     context={
#         'about_company': about_us,
#         'barcode_url': barcode_url,
#     }  
#     return render (request, 'index.html', context)


@login_required(login_url='/login')
def current_year(request):
    year = datetime.now().year
    return render(request, 'index.html', {'current_year': current_year})


