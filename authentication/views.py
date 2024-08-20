from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage
from django.urls import reverse
from django.contrib import auth
from .utils import account_activation_token
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ObjectDoesNotExist
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
import threading
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import  ProfileUpdateForm
from .models import Profile



class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email=email
        threading.Thread.__init__(self)
    
    def run(self):
        self.email.send(fail_silently=False)
    

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
            if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }

                link = reverse('activate', kwargs={
                               'uidb64': email_body['uid'], 'token': email_body['token']})

                email_subject = 'Activate your account'

                activate_url = 'http://'+current_site.domain+link

                email = EmailMessage(
                    email_subject,
                    'Hi '+user.username + ', Please the link below to activate your account \n'+activate_url,
                    'noreply@semycolon.com',
                    [email],
                )
                EmailThread(email).start()
                messages.success(request, 'Activation link was sent to your email successfully..')
                return render(request, 'authentication/register.html')
        return render(request, 'authentication/register.html')
    

                
        

class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)
            
            if not account_activation_token.check_token(user, token):
                return redirect('login' + '?message'+'User already activate')
            
            if user.is_active:
                return redirect('login')
            user.is_active = True
            user.save()
            messages.success(request, "Account activated successfully...")
            return redirect ('login')
        
        except Exception as ex:
            pass
        return redirect ('login')
    

class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']

        if username and password:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    # Ensure profile is created if it does not exist
                    try:
                        profile = user.profile
                    except Profile.DoesNotExist:
                        profile = Profile.objects.create(user=user)
                    
                    auth.login(request, user)
                    messages.success(request, 'Welcome, ' + user.username + ' you are now logged in')
                    return redirect('index')
                messages.error(request, 'Account is not active, please check your email')
                return render(request, 'authentication/login.html')
            messages.error(request, 'Invalid credentials, try again')
            return render(request, 'authentication/login.html')

        messages.error(request, 'Please fill all fields')
        return render(request, 'authentication/login.html')
   
  

class LogoutView(View):
    def post(self, request):
        auth.logout(request)
        messages.success(request, 'You have logged out')
        return redirect('login')


def logout(request):
   auth.logout(request)
   return redirect('login')



class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request, 'authentication/reset_password.html')
    
    def post(self, request):
        email = request.POST.get('email')
        
        context = {
            'values': request.POST,
        }
        
        if not validate_email(email):
            messages.error(request, 'Please enter a valid email address.')
            return render(request, 'authentication/reset_password.html', context)
        
        current_site = get_current_site(request)
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            messages.error(request, 'No user is associated with this email address.')
            return render(request, 'authentication/reset_password.html', context)
        
        email_contents = {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': PasswordResetTokenGenerator().make_token(user),
        }
        
        link = reverse('reset-user-password', kwargs={
            'uidb64': email_contents['uid'], 
            'token': email_contents['token']
        })
        
        email_subject = "Password Reset Instructions"
        reset_url = f"http://{current_site.domain}{link}"
        email_body = f'Hi {user.username},\n\nPlease click the link below to reset your password:\n{reset_url}'
        
        email = EmailMessage(
            email_subject,
            email_body,
            'no-reply@yourdomain.com',
            [email],
        )
        
        try:
            # email_message.send(fail_silently=False)
            EmailThread(email).start()
            messages.success(request, 'We have sent you an email to reset your password.')
        except Exception as e:
            messages.error(request, 'There was an error sending the email. Please try again later.')
        
        return render(request, 'authentication/reset_password.html')



class CompletePasswordReset(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
        }
        try:
            user_id = force_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            
            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, 'Password link invalid, please request a new one')
                return render(request, 'authentication/reset_password.html', context)
        
        except Exception as identifier:
            pass
        
        return render(request, 'authentication/set_newpassword.html', context)
    
    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token,
        }
        password = request.POST['password']
        password2 = request.POST['password2']
        
        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'authentication/set_newpassword.html', context)
        
        if len(password) < 6:
            messages.error(request, 'Password is too short.')
            return render(request, 'authentication/set_newpassword.html', context)
        
        try:
            user_id = force_bytes(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            if PasswordResetTokenGenerator().check_token(user, token):
                user.set_password(password)  # Properly set the password
                user.save()
                messages.success(request, 'Password reset successfully. You are now logged in.')
                login(request, user)  # Log the user in
                return redirect('index')  # Redirect to the homepage or another appropriate page
            else:
                messages.error(request, 'The reset link is no longer valid.')
                return render(request, 'authentication/set_newpassword.html', context)
        except Exception as identifier:
            messages.info(request, 'Something went wrong, please try again.')
            return render(request, 'authentication/set_newpassword.html', context)



class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data ['email']
        if not validate_email(email):
            return JsonResponse({'email_error': ' Email is invalid'}, status=400)
        
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': ' Sorry email is already exists'}, status=409)
        
        return JsonResponse({'email_valid': True})

class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data ['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': ' Username should only countain alphabet'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': ' Sorry username is already exists'}, status=409)
        
        return JsonResponse({'username_valid': True})
        




@login_required
def profile(request):
    # Ensure the user has a profile
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = Profile(user=request.user)
        profile.profile_image = 'default/default-user.png'
        profile.save()

    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('index')
    else:
        p_form = ProfileUpdateForm(instance=profile)

    return render(request, 'userpreferences/profile.html', {'p_form': p_form, 'profile': profile})
