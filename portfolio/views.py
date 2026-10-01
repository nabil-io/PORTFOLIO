from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from core.models import SiteSettings, SkillCategory, Project, Experience, Education, SocialLink, Service, ContactMessage

def home(request):
    site_settings = SiteSettings.load()
    skill_categories = SkillCategory.objects.prefetch_related('skills').all()
    projects = Project.objects.all()
    experiences = Experience.objects.all()
    educations = Education.objects.all()
    social_links = SocialLink.objects.all()
    services = Service.objects.all()
    
    context = {
        'settings': site_settings,
        'skill_categories': skill_categories,
        'projects': projects,
        'experiences': experiences,
        'educations': educations,
        'social_links': social_links,
        'services': services,
    }
    return render(request, 'portfolio/home.html', context)

def contact_send(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject', 'Message depuis le portfolio')
        message = request.POST.get('message')
        
        if name and email and message:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            
            site_settings = SiteSettings.load()
            admin_email = site_settings.email
            full_message = f"Nouveau message de contact de : {name} ({email})\n\nSujet : {subject}\n\nMessage :\n{message}"
            
            try:
                send_mail(
                    subject=f"[Portfolio] {subject}",
                    message=full_message,
                    from_email=email,
                    recipient_list=[admin_email],
                    fail_silently=True,
                )
            except Exception:
                pass
                
            messages.success(request, "Votre message a été envoyé avec succès ! Merci de m'avoir contacté.")
        else:
            messages.error(request, "Veuillez remplir tous les champs requis.")
            
    return redirect('portfolio:home')
