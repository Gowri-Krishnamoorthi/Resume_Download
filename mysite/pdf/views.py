from django.shortcuts import get_object_or_404, render
from .models import Profile
import pdfkit
from django.http import HttpResponse
from django.template import loader
import io
# Create your views here.
def createprofile(request):
     
    if request.method =='POST':
       name = request.POST.get("name","")
       email = request.POST.get("email","")
       phone = request.POST.get("phone","")
       summary = request.POST.get("summary","")
       degree = request.POST.get("degree","")
       school = request.POST.get("school","")
       university = request.POST.get("university","")
       previous_work = request.POST.get("previous_work","")
       skills = request.POST.get("skills","")

       profile = Profile(name=name , email=email , phone=phone , summary=summary , degree=degree , school=school, university=university , previous_work=previous_work , skills=skills)
       profile.save()

    return render(request,'pdf/profile.html',)

def resume(request, id):
    user_profile = Profile.objects.get(pk=id)
    template = loader.get_template('pdf/resume.html')
    html = template.render({'user_profile': user_profile})
    
    path_to_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"  # Change this based on your OS
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

    options = {
        'page-size': 'Letter',
        'encoding': 'UTF-8',
    }

    pdf = pdfkit.from_string(html, False, options=options, configuration=config)
    
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
    return response

def list(request):
    profile = Profile.objects.all()
    return render(request , 'pdf/all_profile.html', {'profile':profile})

def download_profile(request, id):
    profile = get_object_or_404(Profile, id=id)
    
    # Example: Creating a text response as a sample "download"
    response = HttpResponse(f"Downloading profile for {profile.name}")
    response['Content-Disposition'] = f'attachment; filename="{profile.name}.txt"'
    return response