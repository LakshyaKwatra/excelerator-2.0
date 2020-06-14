from django.shortcuts import render, redirect
from .forms import UploadForm
#from django.contrib import messages
#from django.http import HttpResponse
# Create your views here.


def upload_files(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid() and have_proper_formats(request.FILES['file1'], request.FILES['file2']):
            form.save()
            return redirect('compare:compare_files')
        else:
            alert_message = 'Unsupported File Format!'
            form = UploadForm()
            return render(request, 'upload/index.html', {'form': form, 'alert_message': alert_message})
    else:
        form = UploadForm()
        return render(request, 'upload/index.html', {'form': form})


def have_proper_formats(f1, f2):
    SUPPORTED_FORMATS = ['xls', 'xlsx', 'csv', 'tsv']
    file1_format = f1.name.split('.')[-1]
    file2_format = f2.name.split('.')[-1]
    if file1_format not in SUPPORTED_FORMATS or file2_format not in SUPPORTED_FORMATS:
        return False
    else:
        return True