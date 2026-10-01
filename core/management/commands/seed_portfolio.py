from django.core.management.base import BaseCommand
from core.models import SiteSettings, SkillCategory, Skill, Project, Experience, Education, SocialLink

class Command(BaseCommand):
    help = 'Initialise le portfolio avec les données par défaut de GOUNOU Mora Nabil'

    def handle(self, *args, **options):
        self.stdout.write("Création des paramètres du site...")
        settings, created = SiteSettings.objects.get_or_create(pk=1, defaults={
            'site_title': "GOUNOU Mora Nabil | Vibe Codeur & Fullstack",
            'primary_color': "#00f0ff",
            'secondary_color': "#8a2be2",
            'bg_color': "#06070d",
            'font_family': "Space Grotesk",
            'enable_3d': True,
            'hero_greeting': "Bonjour, je suis",
            'hero_title': "GOUNOU Mora Nabil",
            'hero_subtitle': "Développeur Fullstack — Vibe Codeur",
            'hero_description': "Développeur fullstack passionné, je transforme des idées en applications robustes, élégantes et intuitives — avec Django et une bonne dose de créativité.",
            'about_text': "Étudiant en 1ère année de Licence en Systèmes d'Information et Logiciels à l'Institut Universitaire Les Cours Sonou de Parakou (Bénin). Passionné par le code, l'architecture logicielle et les interfaces immersives. Je conçois des solutions web performantes, élégantes et évolutives.",
            'location': "Parakou, Bénin",
            'email': "nabil.gounou@example.com",
            'phone': "+229 01 00 00 00 00",
            'availability': "Disponible pour stage, freelance & projets innovants",
        })
        if not created:
            self.stdout.write("Paramètres du site déjà existants.")

        self.stdout.write("Création des catégories et compétences...")
        cat_backend, _ = SkillCategory.objects.get_or_create(name="Backend", defaults={'order': 1})
        cat_frontend, _ = SkillCategory.objects.get_or_create(name="Frontend", defaults={'order': 2})
        cat_database, _ = SkillCategory.objects.get_or_create(name="Bases de données", defaults={'order': 3})
        cat_tools, _ = SkillCategory.objects.get_or_create(name="Outils & DevOps", defaults={'order': 4})

        skills_data = [
            (cat_backend, "Django / DRF", 90, "fab fa-python", 1),
            (cat_backend, "Python", 92, "fab fa-python", 2),
            (cat_backend, "Node.js", 75, "fab fa-node-js", 3),
            (cat_frontend, "HTML5 / CSS3", 95, "fab fa-html5", 1),
            (cat_frontend, "Tailwind CSS", 90, "fab fa-css3-alt", 2),
            (cat_frontend, "JavaScript (ES6+)", 85, "fab fa-js", 3),
            (cat_frontend, "Alpine.js / HTMX", 80, "fas fa-bolt", 4),
            (cat_database, "PostgreSQL", 85, "fas fa-database", 1),
            (cat_database, "MySQL / SQLite", 85, "fas fa-server", 2),
            (cat_tools, "Git & GitHub", 90, "fab fa-git-alt", 1),
            (cat_tools, "Docker", 70, "fab fa-docker", 2),
            (cat_tools, "VS Code / Linux", 90, "fas fa-terminal", 3),
        ]
        for cat, name, prof, icon, ord in skills_data:
            Skill.objects.get_or_create(category=cat, name=name, defaults={'proficiency': prof, 'icon': icon, 'order': ord})

        self.stdout.write("Création des expériences...")
        Experience.objects.get_or_create(
            title="Stagiaire Développeur Fullstack",
            company="Asitech Solution",
            defaults={
                'location': "Parakou, Bénin",
                'start_date': "2025",
                'end_date': "Présent",
                'is_current': True,
                'description': "Participation au développement d'applications web robustes, intégration d'API avec Django, optimisation des interfaces utilisateurs et collaboration sur des projets clients innovants.",
                'order': 1
            }
        )

        self.stdout.write("Création du parcours académique...")
        Education.objects.get_or_create(
            degree="1ère année de Licence en Systèmes d'Information et Logiciels (SIL)",
            institution="Institut Universitaire Les Cours Sonou",
            defaults={
                'location': "Parakou, Bénin",
                'start_year': "2025",
                'end_year': "En cours",
                'description': "Formation approfondie en algorithmique, structures de données, bases de données relationnelles, programmation orientée objet et génie logiciel.",
                'order': 1
            }
        )

        self.stdout.write("Création des services...")
        from core.models import Service
        services_data = [
            ("Développement Web Fullstack", "Conception d'applications web robustes, performantes et sécurisées avec Django et un écosystème moderne.", "fas fa-laptop-code", 1),
            ("Intégration UI/UX & Responsive", "Création d'interfaces utilisateur futuristes, fluides et élégantes avec Tailwind CSS et des micro-interactions.", "fas fa-paint-brush", 2),
            ("Création d'API & Backends", "Développement d'APIs REST puissantes, gestion des bases de données PostgreSQL et authentification sécurisée.", "fas fa-server", 3),
            ("Conseil & Vibe Coding", "Accompagnement sur vos projets innovants, résolution de bugs et architecture logicielle sur-mesure.", "fas fa-bolt", 4),
        ]
        for title, desc, icon, ord in services_data:
            Service.objects.get_or_create(title=title, defaults={'description': desc, 'icon': icon, 'order': ord})

        self.stdout.write("Création des réseaux sociaux...")
        socials = [
            ("GitHub", "https://github.com", "fab fa-github", 1),
            ("LinkedIn", "https://linkedin.com", "fab fa-linkedin", 2),
            ("Email", "mailto:nabil.gounou@example.com", "fas fa-envelope", 3),
            ("WhatsApp", "https://wa.me/2290100000000", "fab fa-whatsapp", 4),
        ]
        for plat, url, icon, ord in socials:
            SocialLink.objects.get_or_create(platform=plat, defaults={'url': url, 'icon_class': icon, 'order': ord})

        self.stdout.write("Création de projets par défaut...")
        Project.objects.get_or_create(
            slug="futuristic-portfolio",
            defaults={
                'title': "Portfolio Immersif & Futursitic",
                'short_description': "Portfolio web hautement personnalisé avec animations 3D Three.js, mode sombre spatial et panneau d'administration total.",
                'full_description': "Un chef-d'œuvre de design et de code développé avec Django, Tailwind CSS et Three.js. L'espace administrateur permet de modifier absolument tous les aspects du site en temps réel.",
                'technologies': "Django, Tailwind CSS, Three.js, JavaScript, SQLite",
                'github_url': "https://github.com",
                'demo_url': "#",
                'status': "completed",
                'featured': True,
                'order': 1
            }
        )
        Project.objects.get_or_create(
            slug="asitech-gestion",
            defaults={
                'title': "Application de Gestion Asitech",
                'short_description': "Plateforme web de gestion et de suivi de projets professionnels développée lors du stage chez Asitech Solution.",
                'full_description': "Solution complète pour le suivi des tâches, la gestion des clients et le reporting interne avec authentification sécurisée et tableaux de bord dynamiques.",
                'technologies': "Django, Python, Bootstrap, PostgreSQL",
                'github_url': "https://github.com",
                'demo_url': "#",
                'status': "completed",
                'featured': True,
                'order': 2
            }
        )

        self.stdout.write(self.style.SUCCESS("Base de données initialisée avec succès !"))

        from django.contrib.auth.models import User
        if not User.objects.filter(username='nabil').exists():
            User.objects.create_superuser('nabil', 'nabil@example.com', 'nabil2026')
            self.stdout.write(self.style.SUCCESS("Superutilisateur 'nabil' créé (mot de passe: nabil2026)"))
