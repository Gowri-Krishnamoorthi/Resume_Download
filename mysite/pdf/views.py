from django.shortcuts import get_object_or_404, redirect, render
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

       return redirect('list')  # ✅ Redirect to list page after saving

       
    return render(request,'pdf/profile.html',)

# def resume(request, id):
#     user_profile = Profile.objects.get(pk=id)
#     template = loader.get_template('pdf/resume.html')
#     html = template.render({'user_profile': user_profile})
    
#     path_to_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"  # Change this based on your OS
#     config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

#     options = {
#         'page-size': 'Letter',
#         'encoding': 'UTF-8',
#     }

#     pdf = pdfkit.from_string(html, False, options=options, configuration=config)
    
#     response = HttpResponse(pdf, content_type='application/pdf')
#     response['Content-Disposition'] = 'attachment; filename="resume.pdf"'
#     return response

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import Profile

def resume(request, id):
    user_profile = get_object_or_404(Profile, pk=id)

    # Create response object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resume.pdf"'

    # Create PDF Canvas
    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setTitle(f"Resume - {user_profile.name}")

    # Set font and layout
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(100, 750, f"{user_profile.name}")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 730, f"Email: {user_profile.email}")
    pdf.drawString(100, 710, f"Phone: {user_profile.phone}")

    # Draw a line
    pdf.line(100, 700, 500, 700)

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(100, 680, "Summary:")
    pdf.setFont("Helvetica", 12)
    text = pdf.beginText(100, 660)
    text.setFont("Helvetica", 12)
    text.textLines(user_profile.summary)
    pdf.drawText(text)

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(100, 600, "Education:")
    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 580, f"Degree: {user_profile.degree}")
    pdf.drawString(100, 560, f"School: {user_profile.school}")
    pdf.drawString(100, 540, f"University: {user_profile.university}")

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(100, 500, "Previous Work Experience:")
    pdf.setFont("Helvetica", 12)
    work_text = pdf.beginText(100, 480)
    work_text.setFont("Helvetica", 12)
    work_text.textLines(user_profile.previous_work)
    pdf.drawText(work_text)

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(100, 430, "Skills:")
    pdf.setFont("Helvetica", 12)
    skills_text = pdf.beginText(100, 410)
    skills_text.setFont("Helvetica", 12)
    skills_text.textLines(user_profile.skills)
    pdf.drawText(skills_text)

    pdf.showPage()
    pdf.save()

    return response

def list(request):
    profile = Profile.objects.all()
    return render(request , 'pdf/all_profile.html', {'profile':profile})

