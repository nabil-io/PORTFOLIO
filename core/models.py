from django.db import models

class SiteSettings(models.Model):
    site_title = models.CharField(max_length=200, default="GOUNOU Mora Nabil | Portfolio Futursitic")
    primary_color = models.CharField(max_length=50, default="#00f0ff") # Neon Cyan
    secondary_color = models.CharField(max_length=50, default="#8a2be2") # Neon Purple
    bg_color = models.CharField(max_length=50, default="#06070d") # Deep Space Dark
    font_family = models.CharField(max_length=100, default="Space Grotesk")
    enable_3d = models.BooleanField(default=True)
    
    hero_greeting = models.CharField(max_length=100, default="Bonjour, je suis")
    hero_title = models.CharField(max_length=150, default="GOUNOU Mora Nabil")
    hero_subtitle = models.CharField(max_length=200, default="Développeur Fullstack — Vibe Codeur")
    hero_description = models.TextField(default="Développeur fullstack passionné, je transforme des idées en applications robustes, élégantes et intuitives — avec Django et une bonne dose de créativité.")
    
    about_text = models.TextField(default="Étudiant en 1ère année de Licence en Systèmes d'Information et Logiciels à l'Institut Universitaire Les Cours Sonou de Parakou (Bénin). Passionné par le code, l'architecture logicielle et les interfaces immersives. Je conçois des solutions web performantes et évolutives.")
    location = models.CharField(max_length=100, default="Parakou, Bénin")
    email = models.EmailField(default="contact@gounounabil.tech")
    phone = models.CharField(max_length=50, default="+229 01 00 00 00 00")
    availability = models.CharField(max_length=150, default="Disponible pour stage, freelance & projets innovants")
    
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    resume_file = models.FileField(upload_to='resume/', blank=True, null=True)
    
    class Meta:
        verbose_name = "Paramètre du Site"
        verbose_name_plural = "Paramètres du Site"

    def __str__(self):
        return "Configuration du Site"

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class SkillCategory(models.Model):
    name = models.CharField(max_length=100) # Frontend, Backend, Mobile, DevOps, etc.
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Catégorie de Compétence"
        verbose_name_plural = "Catégories de Compétences"
        ordering = ['order']

    def __str__(self):
        return self.name


class Skill(models.Model):
    category = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    proficiency = models.IntegerField(default=80) # 0-100
    icon = models.CharField(max_length=100, default="fas fa-code", help_text="FontAwesome class (e.g. fab fa-python, fas fa-database)")
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Compétence"
        verbose_name_plural = "Compétences"
        ordering = ['category__order', 'order']

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class Project(models.Model):
    STATUS_CHOICES = [
        ('completed', 'Terminé'),
        ('in_progress', 'En cours'),
        ('archived', 'Archivé'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.TextField()
    full_description = models.TextField(blank=True)
    technologies = models.CharField(max_length=300, help_text="Séparées par des virgules (ex: Django, Tailwind, PostgreSQL)")
    github_url = models.URLField(blank=True, null=True)
    demo_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Projet"
        verbose_name_plural = "Projets"
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def get_tech_list(self):
        if not self.technologies:
            return []
        return [t.strip() for t in self.technologies.split(',')]


class Experience(models.Model):
    title = models.CharField(max_length=200) # e.g. Stagiaire Développeur
    company = models.CharField(max_length=200) # e.g. Asitech Solution
    location = models.CharField(max_length=100, default="Parakou, Bénin")
    start_date = models.CharField(max_length=50) # e.g. Janvier 2025
    end_date = models.CharField(max_length=50, default="Présent") # e.g. Présent
    is_current = models.BooleanField(default=False)
    description = models.TextField()
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Expérience Professionnelle"
        verbose_name_plural = "Expériences Professionnelles"
        ordering = ['order']

    def __str__(self):
        return f"{self.title} chez {self.company}"


class Education(models.Model):
    degree = models.CharField(max_length=250) # e.g. 1ère année Licence en Systèmes d'Information et Logiciels
    institution = models.CharField(max_length=250) # e.g. Institut Universitaire Les Cours Sonou
    location = models.CharField(max_length=100, default="Parakou, Bénin")
    start_year = models.CharField(max_length=50) # e.g. 2025
    end_year = models.CharField(max_length=50, default="En cours")
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Parcours Académique"
        verbose_name_plural = "Parcours Académiques"
        ordering = ['order']

    def __str__(self):
        return f"{self.degree} - {self.institution}"


class SocialLink(models.Model):
    platform = models.CharField(max_length=100) # GitHub, LinkedIn, etc.
    url = models.CharField(max_length=500) # URLField or CharField to support WhatsApp URI / mailto / tel
    icon_class = models.CharField(max_length=100, default="fab fa-github")
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Réseau Social"
        verbose_name_plural = "Réseaux Sociaux"
        ordering = ['order']

    def __str__(self):
        return self.platform

    def get_formatted_url(self):
        if not self.url:
            return "#"
        url = self.url.strip()
        if '@' in url and not url.startswith('mailto:') and not url.startswith('http'):
            return f"mailto:{url}"
        if (url.startswith('+') or url.isdigit()) and not url.startswith('tel:'):
            return f"tel:{url}"
        return url


class Service(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    icon = models.CharField(max_length=100, default="fas fa-code", help_text="FontAwesome class (e.g. fas fa-laptop-code, fas fa-server, fab fa-python)")
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"
        ordering = ['order']

    def __str__(self):
        return self.title


class ServiceExample(models.Model):
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='examples')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='services/examples/', blank=True, null=True)
    project_link = models.URLField(blank=True, null=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Exemple de réalisation"
        verbose_name_plural = "Exemples de réalisations"
        ordering = ['order']

    def __str__(self):
        return f"{self.title} ({self.service.title})"


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Message de Contact"
        verbose_name_plural = "Messages de Contact"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"
