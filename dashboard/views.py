from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import SiteSettings, SkillCategory, Skill, Project, Experience, Education, SocialLink, Service, ServiceExample, ContactMessage

def admin_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Connexion réussie au panneau d'administration !")
            return redirect('dashboard:home')
        else:
            messages.error(request, "Identifiants invalides.")
            
    return render(request, 'dashboard/login.html')

@login_required(login_url='dashboard:login')
def admin_logout(request):
    logout(request)
    messages.info(request, "Vous avez été déconnecté.")
    return redirect('dashboard:login')

@login_required(login_url='dashboard:login')
def dashboard_home(request):
    projects_count = Project.objects.count()
    skills_count = Skill.objects.count()
    messages_count = ContactMessage.objects.count()
    unread_messages = ContactMessage.objects.filter(is_read=False).count()
    recent_messages = ContactMessage.objects.all()[:5]
    
    context = {
        'projects_count': projects_count,
        'skills_count': skills_count,
        'messages_count': messages_count,
        'unread_messages': unread_messages,
        'recent_messages': recent_messages,
    }
    return render(request, 'dashboard/home.html', context)

@login_required(login_url='dashboard:login')
def dashboard_settings(request):
    site_settings = SiteSettings.load()
    if request.method == 'POST':
        site_settings.site_title = request.POST.get('site_title', site_settings.site_title)
        site_settings.primary_color = request.POST.get('primary_color', site_settings.primary_color)
        site_settings.secondary_color = request.POST.get('secondary_color', site_settings.secondary_color)
        site_settings.bg_color = request.POST.get('bg_color', site_settings.bg_color)
        site_settings.font_family = request.POST.get('font_family', site_settings.font_family)
        site_settings.enable_3d = True if request.POST.get('enable_3d') == 'on' else False
        
        site_settings.hero_greeting = request.POST.get('hero_greeting', site_settings.hero_greeting)
        site_settings.hero_title = request.POST.get('hero_title', site_settings.hero_title)
        site_settings.hero_subtitle = request.POST.get('hero_subtitle', site_settings.hero_subtitle)
        site_settings.hero_description = request.POST.get('hero_description', site_settings.hero_description)
        site_settings.about_text = request.POST.get('about_text', site_settings.about_text)
        site_settings.location = request.POST.get('location', site_settings.location)
        site_settings.email = request.POST.get('email', site_settings.email)
        site_settings.phone = request.POST.get('phone', site_settings.phone)
        site_settings.availability = request.POST.get('availability', site_settings.availability)
        
        if 'profile_image' in request.FILES:
            site_settings.profile_image = request.FILES['profile_image']
        if 'resume_file' in request.FILES:
            site_settings.resume_file = request.FILES['resume_file']
            
        site_settings.save()
        messages.success(request, "Paramètres mis à jour avec succès !")
        return redirect('dashboard:settings')
        
    return render(request, 'dashboard/settings.html', {'settings': site_settings})

# Projects CRUD
@login_required(login_url='dashboard:login')
def project_list(request):
    projects = Project.objects.all()
    return render(request, 'dashboard/project_list.html', {'projects': projects})

@login_required(login_url='dashboard:login')
def project_add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        slug = request.POST.get('slug') or title.lower().replace(' ', '-')
        short_description = request.POST.get('short_description')
        full_description = request.POST.get('full_description')
        technologies = request.POST.get('technologies')
        github_url = request.POST.get('github_url')
        demo_url = request.POST.get('demo_url')
        status = request.POST.get('status', 'completed')
        featured = True if request.POST.get('featured') == 'on' else False
        order = int(request.POST.get('order', 0))
        image = request.FILES.get('image')
        
        Project.objects.create(
            title=title,
            slug=slug,
            short_description=short_description,
            full_description=full_description,
            technologies=technologies,
            github_url=github_url,
            demo_url=demo_url,
            status=status,
            featured=featured,
            order=order,
            image=image
        )
        messages.success(request, "Projet ajouté avec succès !")
        return redirect('dashboard:project_list')
        
    return render(request, 'dashboard/project_form.html', {'action': 'Ajouter'})

@login_required(login_url='dashboard:login')
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.title = request.POST.get('title')
        project.slug = request.POST.get('slug') or project.title.lower().replace(' ', '-')
        project.short_description = request.POST.get('short_description')
        project.full_description = request.POST.get('full_description')
        project.technologies = request.POST.get('technologies')
        project.github_url = request.POST.get('github_url')
        project.demo_url = request.POST.get('demo_url')
        project.status = request.POST.get('status', 'completed')
        project.featured = True if request.POST.get('featured') == 'on' else False
        project.order = int(request.POST.get('order', 0))
        if 'image' in request.FILES:
            project.image = request.FILES['image']
        project.save()
        messages.success(request, "Projet modifié avec succès !")
        return redirect('dashboard:project_list')
        
    return render(request, 'dashboard/project_form.html', {'project': project, 'action': 'Modifier'})

@login_required(login_url='dashboard:login')
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    project.delete()
    messages.success(request, "Projet supprimé.")
    return redirect('dashboard:project_list')

# Skills CRUD
@login_required(login_url='dashboard:login')
def skill_list(request):
    categories = SkillCategory.objects.prefetch_related('skills').all()
    return render(request, 'dashboard/skill_list.html', {'categories': categories})

@login_required(login_url='dashboard:login')
def skill_add(request):
    categories = SkillCategory.objects.all()
    if request.method == 'POST':
        category_id = request.POST.get('category')
        category = get_object_or_404(SkillCategory, pk=category_id)
        name = request.POST.get('name')
        proficiency = int(request.POST.get('proficiency', 80))
        icon = request.POST.get('icon', 'fas fa-code')
        order = int(request.POST.get('order', 0))
        
        Skill.objects.create(
            category=category,
            name=name,
            proficiency=proficiency,
            icon=icon,
            order=order
        )
        messages.success(request, "Compétence ajoutée !")
        return redirect('dashboard:skill_list')
        
    return render(request, 'dashboard/skill_form.html', {'categories': categories, 'action': 'Ajouter'})

@login_required(login_url='dashboard:login')
def skill_edit(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    categories = SkillCategory.objects.all()
    if request.method == 'POST':
        skill.category = get_object_or_404(SkillCategory, pk=request.POST.get('category'))
        skill.name = request.POST.get('name')
        skill.proficiency = int(request.POST.get('proficiency', 80))
        skill.icon = request.POST.get('icon')
        skill.order = int(request.POST.get('order', 0))
        skill.save()
        messages.success(request, "Compétence modifiée !")
        return redirect('dashboard:skill_list')
        
    return render(request, 'dashboard/skill_form.html', {'skill': skill, 'categories': categories, 'action': 'Modifier'})

@login_required(login_url='dashboard:login')
def skill_delete(request, pk):
    skill = get_object_or_404(Skill, pk=pk)
    skill.delete()
    messages.success(request, "Compétence supprimée.")
    return redirect('dashboard:skill_list')

# Experiences CRUD
@login_required(login_url='dashboard:login')
def experience_list(request):
    experiences = Experience.objects.all()
    return render(request, 'dashboard/experience_list.html', {'experiences': experiences})

@login_required(login_url='dashboard:login')
def experience_add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        company = request.POST.get('company')
        location = request.POST.get('location')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        is_current = True if request.POST.get('is_current') == 'on' else False
        description = request.POST.get('description')
        order = int(request.POST.get('order', 0))
        
        Experience.objects.create(
            title=title, company=company, location=location,
            start_date=start_date, end_date=end_date, is_current=is_current,
            description=description, order=order
        )
        messages.success(request, "Expérience ajoutée !")
        return redirect('dashboard:experience_list')
    return render(request, 'dashboard/experience_form.html', {'action': 'Ajouter'})

@login_required(login_url='dashboard:login')
def experience_edit(request, pk):
    exp = get_object_or_404(Experience, pk=pk)
    if request.method == 'POST':
        exp.title = request.POST.get('title')
        exp.company = request.POST.get('company')
        exp.location = request.POST.get('location')
        exp.start_date = request.POST.get('start_date')
        exp.end_date = request.POST.get('end_date')
        exp.is_current = True if request.POST.get('is_current') == 'on' else False
        exp.description = request.POST.get('description')
        exp.order = int(request.POST.get('order', 0))
        exp.save()
        messages.success(request, "Expérience modifiée !")
        return redirect('dashboard:experience_list')
    return render(request, 'dashboard/experience_form.html', {'experience': exp, 'action': 'Modifier'})

@login_required(login_url='dashboard:login')
def experience_delete(request, pk):
    get_object_or_404(Experience, pk=pk).delete()
    messages.success(request, "Expérience supprimée.")
    return redirect('dashboard:experience_list')

# Education CRUD
@login_required(login_url='dashboard:login')
def education_list(request):
    educations = Education.objects.all()
    return render(request, 'dashboard/education_list.html', {'educations': educations})

@login_required(login_url='dashboard:login')
def education_add(request):
    if request.method == 'POST':
        degree = request.POST.get('degree')
        institution = request.POST.get('institution')
        location = request.POST.get('location')
        start_year = request.POST.get('start_year')
        end_year = request.POST.get('end_year')
        description = request.POST.get('description')
        order = int(request.POST.get('order', 0))
        
        Education.objects.create(
            degree=degree, institution=institution, location=location,
            start_year=start_year, end_year=end_year, description=description, order=order
        )
        messages.success(request, "Parcours académique ajouté !")
        return redirect('dashboard:education_list')
    return render(request, 'dashboard/education_form.html', {'action': 'Ajouter'})

@login_required(login_url='dashboard:login')
def education_edit(request, pk):
    edu = get_object_or_404(Education, pk=pk)
    if request.method == 'POST':
        edu.degree = request.POST.get('degree')
        edu.institution = request.POST.get('institution')
        edu.location = request.POST.get('location')
        edu.start_year = request.POST.get('start_year')
        edu.end_year = request.POST.get('end_year')
        edu.description = request.POST.get('description')
        edu.order = int(request.POST.get('order', 0))
        edu.save()
        messages.success(request, "Parcours modifié !")
        return redirect('dashboard:education_list')
    return render(request, 'dashboard/education_form.html', {'education': edu, 'action': 'Modifier'})

@login_required(login_url='dashboard:login')
def education_delete(request, pk):
    get_object_or_404(Education, pk=pk).delete()
    messages.success(request, "Parcours supprimé.")
    return redirect('dashboard:education_list')

# Messages
@login_required(login_url='dashboard:login')
def message_list(request):
    msgs = ContactMessage.objects.all()
    msgs.update(is_read=True) # mark all as read when viewed
    return render(request, 'dashboard/message_list.html', {'messages_list': msgs})

@login_required(login_url='dashboard:login')
def message_delete(request, pk):
    get_object_or_404(ContactMessage, pk=pk).delete()
    messages.success(request, "Message supprimé.")
    return redirect('dashboard:message_list')

# Services CRUD
@login_required(login_url='dashboard:login')
def service_list(request):
    services = Service.objects.all()
    return render(request, 'dashboard/service_list.html', {'services': services})

@login_required(login_url='dashboard:login')
def service_add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        icon = request.POST.get('icon', 'fas fa-code')
        order = int(request.POST.get('order', 0))
        image = request.FILES.get('image')
        Service.objects.create(title=title, description=description, icon=icon, order=order, image=image)
        messages.success(request, "Service ajouté avec succès !")
        return redirect('dashboard:service_list')
    return render(request, 'dashboard/service_form.html', {'action': 'Ajouter'})

@login_required(login_url='dashboard:login')
def service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.title = request.POST.get('title')
        service.description = request.POST.get('description')
        service.icon = request.POST.get('icon')
        service.order = int(request.POST.get('order', 0))
        if 'image' in request.FILES:
            service.image = request.FILES['image']
        service.save()
        messages.success(request, "Service modifié avec succès !")
        return redirect('dashboard:service_list')
    return render(request, 'dashboard/service_form.html', {'service': service, 'action': 'Modifier'})

@login_required(login_url='dashboard:login')
def service_delete(request, pk):
    get_object_or_404(Service, pk=pk).delete()
    messages.success(request, "Service supprimé.")
    return redirect('dashboard:service_list')

@login_required(login_url='dashboard:login')
def service_example_add(request, service_pk):
    service = get_object_or_404(Service, pk=service_pk)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        project_link = request.POST.get('project_link')
        order = int(request.POST.get('order', 0))
        image = request.FILES.get('image')
        ServiceExample.objects.create(
            service=service, title=title, description=description,
            project_link=project_link, order=order, image=image
        )
        messages.success(request, "Exemple de réalisation ajouté avec succès !")
        return redirect('dashboard:service_edit', pk=service.pk)
    return render(request, 'dashboard/service_example_form.html', {'service': service, 'action': 'Ajouter'})

@login_required(login_url='dashboard:login')
def service_example_edit(request, pk):
    example = get_object_or_404(ServiceExample, pk=pk)
    if request.method == 'POST':
        example.title = request.POST.get('title')
        example.description = request.POST.get('description')
        example.project_link = request.POST.get('project_link')
        example.order = int(request.POST.get('order', 0))
        if 'image' in request.FILES:
            example.image = request.FILES['image']
        example.save()
        messages.success(request, "Exemple modifié avec succès !")
        return redirect('dashboard:service_edit', pk=example.service.pk)
    return render(request, 'dashboard/service_example_form.html', {'example': example, 'service': example.service, 'action': 'Modifier'})

@login_required(login_url='dashboard:login')
def service_example_delete(request, pk):
    example = get_object_or_404(ServiceExample, pk=pk)
    service_pk = example.service.pk
    example.delete()
    messages.success(request, "Exemple supprimé.")
    return redirect('dashboard:service_edit', pk=service_pk)

# Social Links CRUD
@login_required(login_url='dashboard:login')
def social_list(request):
    socials = SocialLink.objects.all()
    return render(request, 'dashboard/social_list.html', {'socials': socials})

@login_required(login_url='dashboard:login')
def social_add(request):
    if request.method == 'POST':
        platform = request.POST.get('platform')
        url = request.POST.get('url')
        icon_class = request.POST.get('icon_class', 'fab fa-github')
        order = int(request.POST.get('order', 0))
        SocialLink.objects.create(platform=platform, url=url, icon_class=icon_class, order=order)
        messages.success(request, "Lien social ajouté avec succès !")
        return redirect('dashboard:social_list')
    return render(request, 'dashboard/social_form.html', {'action': 'Ajouter'})

@login_required(login_url='dashboard:login')
def social_edit(request, pk):
    social = get_object_or_404(SocialLink, pk=pk)
    if request.method == 'POST':
        social.platform = request.POST.get('platform')
        social.url = request.POST.get('url')
        social.icon_class = request.POST.get('icon_class')
        social.order = int(request.POST.get('order', 0))
        social.save()
        messages.success(request, "Lien social modifié avec succès !")
        return redirect('dashboard:social_list')
    return render(request, 'dashboard/social_form.html', {'social': social, 'action': 'Modifier'})

@login_required(login_url='dashboard:login')
def social_delete(request, pk):
    get_object_or_404(SocialLink, pk=pk).delete()
    messages.success(request, "Lien social supprimé.")
    return redirect('dashboard:social_list')
