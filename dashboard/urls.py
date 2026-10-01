from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    path('', views.dashboard_home, name='home'),
    path('settings/', views.dashboard_settings, name='settings'),
    
    # Projects
    path('projects/', views.project_list, name='project_list'),
    path('projects/add/', views.project_add, name='project_add'),
    path('projects/<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('projects/<int:pk>/delete/', views.project_delete, name='project_delete'),
    
    # Skills
    path('skills/', views.skill_list, name='skill_list'),
    path('skills/add/', views.skill_add, name='skill_add'),
    path('skills/<int:pk>/edit/', views.skill_edit, name='skill_edit'),
    path('skills/<int:pk>/delete/', views.skill_delete, name='skill_delete'),
    
    # Experiences & Education
    path('experiences/', views.experience_list, name='experience_list'),
    path('experiences/add/', views.experience_add, name='experience_add'),
    path('experiences/<int:pk>/edit/', views.experience_edit, name='experience_edit'),
    path('experiences/<int:pk>/delete/', views.experience_delete, name='experience_delete'),
    
    path('education/', views.education_list, name='education_list'),
    path('education/add/', views.education_add, name='education_add'),
    path('education/<int:pk>/edit/', views.education_edit, name='education_edit'),
    path('education/<int:pk>/delete/', views.education_delete, name='education_delete'),
    
    # Services
    path('services/', views.service_list, name='service_list'),
    path('services/add/', views.service_add, name='service_add'),
    path('services/<int:pk>/edit/', views.service_edit, name='service_edit'),
    path('services/<int:pk>/delete/', views.service_delete, name='service_delete'),
    path('services/<int:service_pk>/examples/add/', views.service_example_add, name='service_example_add'),
    path('services/examples/<int:pk>/edit/', views.service_example_edit, name='service_example_edit'),
    path('services/examples/<int:pk>/delete/', views.service_example_delete, name='service_example_delete'),

    # Social Links
    path('socials/', views.social_list, name='social_list'),
    path('socials/add/', views.social_add, name='social_add'),
    path('socials/<int:pk>/edit/', views.social_edit, name='social_edit'),
    path('socials/<int:pk>/delete/', views.social_delete, name='social_delete'),

    # Messages
    path('messages/', views.message_list, name='message_list'),
    path('messages/<int:pk>/delete/', views.message_delete, name='message_delete'),
]
