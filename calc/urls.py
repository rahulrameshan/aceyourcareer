from django.urls import path
from . import views
from . import jobs

urlpatterns = [
    # Homepage URLs
    path('', views.home, name='home'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('subscribe_store', views.subscribe_store, name='subscribe_store'),
    path('contact_us_store', views.contact_us_store, name='contact_us_store'),
    # register login urls
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('logout', views.logout, name='logout'),
    path('reset_password_request', views.reset_password_request, name='reset_password_request'),
    path('set_new_password/<uibd64>/<token>', views.set_new_password, name='set_new_password'),
    #tools
    path('resume_builder', views.resume_builder, name='resume_builder'),
    path('cover_letter', views.cover_letter, name='cover_letter'),
    path('resume_review', views.resume_review, name='resume_review'),
    #  job URLs
    path('browse_jobs', jobs.browse_jobs, name='browse_jobs'),
    path('job_details/<job_id>', jobs.job_details, name='job_details'),
    # Health check
    path('health_check',views.health_check, name='health_check'),
    #Storing sign ups
    path('sign_ups',views.sign_ups, name='sign_ups'),

]
