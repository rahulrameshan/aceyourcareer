from django.shortcuts import render
from .models import contact_us_model
from .models import subscribe_model
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse
import smtplib
from email.mime.text import MIMEText
from gingerit.gingerit import GingerIt
from django.http import HttpResponse, HttpResponseNotFound, Http404,  HttpResponseRedirect


# Create your views here.


def home(request): 	
    return render(request, 'index.html')


def contact(request):
    return render(request, 'contact.html')


def about(request):
    return render(request, 'about.html')


def contact_us_store(request):
    try:
        contact_email = request.POST['contact_email']
    except Exception as e:
        contact_email = ""

    try:
        contact_name = request.POST['contact_name']
    except Exception as e:
        contact_name = ""

    try:
        contact_subject = request.POST['contact_subject']
    except Exception as e:
        contact_subject = ""

    try:
        contact_message = request.POST['contact_message']
    except Exception as e:
        contact_message = ""

    try:
        contact_us_data = contact_us_model(contact_email=contact_email, contact_name=contact_name,
                                           contact_subject=contact_subject, contact_message=contact_message)

        contact_us_data.save()
    except Exception as e:
        pass

    return render(request, 'index.html')


def subscribe_store(request):
    try:
        subscribe_email = request.POST['subscribe_email']
        subscription_data = subscribe_model(subscribe_email=subscribe_email)
        subscription_data.save()

    except Exception as e:
        subscribe_email = ""

    return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        try:
            login_email = request.POST['login_email']
            login_user_name = login_email
        except Exception as e:
            pass
        try:
            login_password = request.POST['login_password']
        except Exception as e:
            pass

        try:
            user = auth.authenticate(
                username=login_user_name, password=login_password)
        except Exception as e:
            user = None

        if user is not None:
            try:
                auth.login(request, user)
                return render(request, 'index.html')
            except Exception as e:
                messages.info(request, e)
                return render(request, 'login.html')

        else:
            messages.info(request, 'Username or Password is wrong')
            return render(request, 'login.html')

    else:
        return render(request, 'login.html')


def register(request):

    if request.method == 'POST':
        try:
            reg_first_name = request.POST['reg_first_name']
        except Exception as e:
            pass
        try:
            reg_last_name = request.POST['reg_last_name']
        except Exception as e:
            pass
        try:
            reg_email = request.POST['reg_email']
            reg_user_name = reg_email
        except Exception as e:
            pass
        try:
            reg_password1 = request.POST['reg_password1']
        except Exception as e:
            pass
        try:
            reg_password2 = request.POST['reg_password2']
        except Exception as e:
            pass

        try:
            if reg_password1 == reg_password2:
                if User.objects.filter(username=reg_user_name).exists():

                    messages.info(request, 'Email taken')

                    return render(request, 'register.html')
                else:

                    user = User.objects.create_user(username=reg_user_name, password=reg_password1,
                                                    email=reg_email, first_name=reg_first_name, last_name=reg_last_name)
                    user.save()
                    return render(request, 'login.html')
            else:
                messages.info(request, 'Password does not match')

                return render(request, 'register.html')
        except Exception as e:
            messages.info(request, 'Error, User Cannot be registered')
            print(e)
            return render(request, 'register.html')

    else:
        return render(request, 'register.html')


def logout(request):
    auth.logout(request)
    return render(request, 'index.html')


def resume_builder(request):
    if request.user.is_authenticated:
        return render(request, 'resume_builder.html')

    else:
        messages.info(request, 'To use Resume Builder, login first')
        return render(request, 'login.html')


def reset_password_request(request):

    if request.method == 'POST':
        reset_email = request.POST['reset_email']

        if User.objects.filter(email=reset_email).exists():

            user = User.objects.filter(email=reset_email)
            current_site = get_current_site(request)

            email_contents = {'user':user[0], 'domain':current_site.domain, 'uid':urlsafe_base64_encode(force_bytes(user[0].pk)), 'token': PasswordResetTokenGenerator().make_token(user[0])}

            #link = reverse('set_new_password', kwargs = {'uidb64': email_contents['uid'], 'token': email_contents['token']})
            link = '/set_new_password' + '/' + str(email_contents['uid']) + '/' + str(email_contents['token'])
            email_subject = 'Reset Your Password'

            reset_url = 'http://' + current_site.domain + link
            """
            email = EmailMessage(email_subject, 'Hi, '  + 'Go to the link below to reset your password \n' + reset_url , settings.EMAIL_HOST_USER, [reset_email])

            email.send(fail_silently=False)
            """
            sender = settings.EMAIL_HOST_USER
            recipient = reset_email # Create message
            msg = MIMEText('Hi, '  + 'Go to the link below to reset your password \n' + reset_url)
            msg['Subject'] = "Ace Your Carrer - Reset Your Password"
            msg['From'] = sender
            msg['To'] = recipient # Create server object with SSL option
            server = smtplib.SMTP_SSL('smtp.zoho.in', 465) # Perform operations via server
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(sender, [recipient], msg.as_string())
            server.quit()
            messages.success(request, 'Please check your email for password reset link')
            return render(request, 'reset_password_request.html')
        
        else:
            messages.info(request, 'This Email is not registered')
            return render(request, 'reset_password_request.html')

    else:
        return render(request, 'reset_password_request.html')

def set_new_password(request, uibd64, token):
    if request.method == "POST":
        context={'uibd64':uibd64, 'token':token}
        uidb64_ok = uibd64
        
        password1 = request.POST['reset_password1']
        password2 = request.POST['reset_password2']

        if password1 != password2:
            messages.info(request, 'Password does not match')
            return render(request, 'set_new_password.html', context)

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64_ok))

            user = User.objects.get(pk=user_id)
            user.set_password(password1)
            user.save()
            messages.info(request, 'Password reset succesful')

            return redirect(login)
        except Exception as e:
            messages.info(request, 'Please try again')
            print(e)
            return render(request, 'set_new_password.html', context)

    else:
        context={'uibd64':uibd64, 'token':token}
        print(context)
        print('printing context')
        return render(request, 'set_new_password.html', context)

def health_check(request):
    return HttpResponse(status=200)

def error_404(request, exception):
    return render(request, 'error_pages/error_404.html')

def error_500(request):
    return render(request, 'error_pages/error_500.html')

def cover_letter(request):
    if request.user.is_authenticated:
        return render(request, 'cover_letter.html')

    else:
        messages.info(request, 'To use Cover Letter Generator, login first')
        return render(request, 'login.html')

def resume_review(request):
    if request.method == "POST":
        try:
            output_string = request.POST["output"]
            output_string = str(output_string)
            output_list = output_string.split("<br>")
            final_output_list = [x for x in output_list if len(x)>3]
            parser = GingerIt()
            output_dictionary_list = []
            message = "There are no suggested changes"
            for i in range(len(final_output_list)):
                text = final_output_list[i]
                temp_result_dict =parser.parse(text)
                
                if(temp_result_dict['text'] != temp_result_dict['result']):
                    temp_output_dict = {}
                    temp_output_dict['original'] = temp_result_dict['text']
                    temp_output_dict['corrected'] = temp_result_dict['result']
                    temp_output_dict['details'] = temp_result_dict['corrections']

                    output_dictionary_list.append(temp_output_dict)
                    message = "These are the suggested changes"
            
            context = {'Message':message, 'output_list':output_dictionary_list}
            return render(request, 'resume_review.html', context)
        except Exception as e:
            output_dictionary_list = []
            context = {'Message':'Something went wrong', 'output_list':output_dictionary_list}
            return render(request, 'resume_review.html', context)

    else:
        if request.user.is_authenticated:
            output_dictionary_list = []
            context = {'Message':'Upload your resume', 'output_list':output_dictionary_list}
            return render(request, 'resume_review.html', context)

        else:
            messages.info(request, 'To use Resume Review tool, login first')
            return render(request, 'login.html')

def sign_ups(request):
    try:
        subscribe_email = request.POST['sign_up_email']
        subscription_data = subscribe_model(subscribe_email=subscribe_email)
        subscription_data.save()

    except Exception as e:
        subscribe_email = ""   

    return HttpResponseRedirect("https://airtable.com/shrnw0kckmhoVn61e")
