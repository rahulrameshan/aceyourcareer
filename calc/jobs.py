from django.shortcuts import render
from .models import contact_us_model
from .models import subscribe_model
from django.contrib.auth.models import User, auth
from django.contrib import messages
import requests
from django.contrib.sites.shortcuts import get_current_site


def browse_jobs(request):
    current_site = get_current_site(request)
    if request.method == "POST":
        try:
            category = request.POST['job_category']
        except Exception as e:
            category = ""
        try:
            level = request.POST['exp_level']
        except Exception as e:
            level = ""
        try:
            location = request.POST['location']
        except Exception as e:
            location = ""
        try:
            current_page = request.POST['current_page']
            current_page = int(current_page)
        except Exception as e:
            current_page = 1
        
        URL = 'https://www.themuse.com/api/public/jobs'

        try:
            next_page = request.POST['next']
            current_page = current_page + 1
        except Exception as e:
            print(e)

        try:
            prev_page = request.POST['prev']
            current_page = current_page - 1
        except Exception as e:
            print(e)


        PARAMS = {'page': current_page, 'descending': 'true', 'category': category, 'level': level, 
                 'location': location, 'api_key': 'c4d0b40fb4452fe3dc0dfa0a885312df829c5828fee2d6e395ed122b49e5e5ef'}

        r = requests.get(url=URL, params=PARAMS)

        data = r.json()

        page_count = int(data['page_count'])

        context_dictionary = {'total_pages':page_count, 'current_page':current_page, 'category':category, 'level': level, 'location': location, 'domain':current_site.domain}
        
        if (len(data['results']) == 0):
            messages.info(request, 'No jobs for the search made. Please try another search')

        return render(request, 'job_display/jobs.html', {'data': data['results'],'context_dictionary':context_dictionary })

    else:
        URL = 'https://www.themuse.com/api/public/jobs'

        PARAMS = {'page': 1, 'descending': 'true', 'category': 'Design', 
                'level': 'internship', 'location': 'Bangalore, India', 'api_key': 'c4d0b40fb4452fe3dc0dfa0a885312df829c5828fee2d6e395ed122b49e5e5ef'}

        r = requests.get(url=URL, params=PARAMS)

        data = r.json()

        page_count = int(data['page_count'])

        context_dictionary = {'total_pages':page_count, 'current_page':1, 'category':'Design', 'level': 'internship', 'location': 'Bangalore, India','domain':current_site.domain}
        return render(request, 'job_display/jobs.html', {'data': data['results'], 'context_dictionary':context_dictionary})

def job_details(request, job_id):

    URL = 'https://www.themuse.com/api/public/jobs/'


    URL = URL + str(job_id)
    r = requests.get(url=URL)

    data = r.json()

    return render(request, 'job_display/job_details.html', {'data':data})