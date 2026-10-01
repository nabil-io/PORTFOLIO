# Portfolio Web Personnel — GOUNOU Mora Nabil (Vibe Codeur)

Portfolio web personnel complet, moderne et futuriste inspiré de l'esthétique spatiale (thème sombre `#06070d`, animations 3D Three.js/WebGL), doté d'un **espace administrateur sur-mesure** permettant une personnalisation totale sans toucher au code.

---

## 🚀 Fonctionnalités Clés

1. **Site Public Immersif & Futursiste** :
   - Design spatial/sombre avec effets de verre (*glassmorphism*), lueur (*glow*) et typographie moderne.
   - Animations 3D interactives en arrière-plan avec **Three.js** (particules spatiales, formes géométriques flottantes).
   - Navigation *one-page* fluide par ancres : Accueil, Parcours, Projets, Compétences, Contact.
   - Formulaire de contact fonctionnel avec stockage en base de données.
   - Entièrement responsive (mobile, tablette, desktop).

2. **Espace Administrateur sur-mesure (`/admin-panel/`)** :
   - Authentification sécurisée (login / logout).
   - **Personnalisation Totale du Design System** : couleurs primaires, secondaires, couleur de fond, police d'écriture (Google Fonts), activation/désactivation des animations 3D.
   - **Gestion de Contenu** : modification des textes de la section Hero, biographie, coordonnées, localisation.
   - **Gestion des Projets** : ajout, modification, suppression de projets avec technologies, liens GitHub/démo et upload d'images.
   - **Gestion des Compétences** : classement par catégories (Backend, Frontend, Bases de données, Outils) avec niveaux de maîtrise en pourcentages et icônes FontAwesome.
   - **Parcours Académique & Expériences Professionnelles** : gestion complète des diplômes (ex: Cours Sonou Parakou) et stages (ex: Asitech Solution).
   - **Messages de Contact** : consultation et gestion des messages reçus.

---

## 🛠️ Stack Technique

- **Backend** : Django 6.1+, Python 3.14+, SQLite (ou PostgreSQL).
- **Frontend** : Tailwind CSS, Alpine.js, FontAwesome, Three.js (WebGL).
- **Médias** : Pillow pour la gestion des uploads d'images.

---

## 📦 Installation et Lancement en Local

Suivez ces étapes pour lancer le projet sur votre machine :

### 1. Prérequis
Assurez-vous d'avoir **Python 3.10+** installé sur votre système.

### 2. Cloner ou ouvrir le projet
Ouvrez votre terminal dans le dossier du projet (`C:\PORTFOLIO`).

### 3. Installer les dépendances
```bash
python -m pip install django pillow
```

### 4. Appliquer les migrations de base de données
```bash
python manage.py makemigrations core portfolio dashboard
python manage.py migrate
```

### 5. Initialiser les données par défaut (et le superutilisateur)
Une commande de peuplement (*seed*) configure automatiquement le profil de **GOUNOU Mora Nabil**, ses compétences, ses projets initiaux et crée le compte administrateur :
```bash
python manage.py seed_portfolio
```
* **Identifiants Administrateur créés automatiquement** :
  * **Nom d'utilisateur** : `nabil`
  * **Mot de passe** : `nabil2026`

### 6. Lancer le serveur de développement
```bash
python manage.py runserver
```

Le site est désormais accessible :
* **Site Public** : `http://127.0.0.1:8000/`
* **Espace Admin sur-mesure** : `http://127.0.0.1:8000/admin-panel/`
* **Django Admin Standard** : `http://127.0.0.1:8000/admin/`

---

## 🎯 Utilisation de l'Espace Admin

1. Rendez-vous sur `http://127.0.0.1:8000/admin-panel/`.
2. Connectez-vous avec les identifiants `nabil` / `nabil2026`.
3. Depuis le tableau de bord, vous pouvez :
   - Modifier les couleurs et polices (les changements s'appliquent instantanément sur le site public).
   - Ajouter ou modifier des projets avec captures d'écran.
   - Mettre à jour vos compétences et expériences professionnelles (Asitech Solution, Cours Sonou, etc.).
   - Consulter les messages de contact reçus.
