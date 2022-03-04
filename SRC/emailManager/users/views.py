import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponse
from .models import *
from django.views import View
from .forms import *
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from utils import *
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.contrib.auth.tokens import default_token_generator
from django.db.models.query_utils import Q
from django.core.mail import send_mail, BadHeaderError
from django.contrib.auth import authenticate, login, logout


# Create your views here.

class Index(View):
    def get(self, request):
        return render(request, 'home.html')


class UserRegister(View):
    form_class = UserRegisterForm()
    template_name = 'users/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'forms': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['recovery_email']:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)

                mail_subject = 'Activate your blog account.'
                message = render_to_string('users/acc_active_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('recovery_email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                messages.success(request, 'Please Confirm your email to complete registration.')
                return HttpResponse('Link sent to your email!')
            elif form.cleaned_data['phone_number']:
                random_code = random.randint(1000, 9999)
                send_otp_code(form.cleaned_data['phone_number'], random_code)
                OtpCode.objects.create(phone_number=form.cleaned_data['phone_number'], code=random_code)
                request.session['user_registration_info'] = {
                    'username': form.cleaned_data['username'],
                    'phone_number': form.cleaned_data['phone_number'],
                    'recovery_email': form.cleaned_data['recovery_email'],
                    'first_name': form.cleaned_data['first_name'],
                    'last_name': form.cleaned_data['last_name'],
                    'country': form.cleaned_data['country'],
                    'birthdate': form.cleaned_data['birthdate'].isoformat(),
                    'password': form.cleaned_data['password2'],
                    'gender': form.cleaned_data['gender'],
                }
                messages.success(request, 'we sent you a code', 'success')
                return redirect('verify_code')
            return render(request, self.template_name, {'forms': form})

        else:
            messages.error(request,
                           f"You must be enter email or phone number!!!!",
                           extra_tags='permanent error')
            storage = messages.get_messages(request)
            for message in storage:
                print(message)
            storage.used = False
            return render(request, 'users/register.html', {"forms": form})


def activate(request, uidb64, token, *args, **kwargs):
    try:
        uid = force_str(s=urlsafe_base64_decode(uidb64).decode(), strings_only=True)
        user = CustomUser.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.username += '@zyo.com'
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, 'users/verify.html', {'form': form})

    def post(self, request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            print('*******************************************************************')
            # print(user)
            print('*******************************************************************')
            if cd['code'] == code_instance.code:
                CustomUser.objects.create_user(user_session['password'],
                                               username=user_session['username'],
                                               phone_number=user_session['phone_number'],
                                               first_name=user_session['first_name'],
                                               last_name=user_session['last_name'],
                                               birthdate=user_session['birthdate'],
                                               gender=user_session['gender'],
                                               country=user_session['country'])
                print('*********************************************************')
                print(user_session['username'])
                # print(CustomUser.objects.get(user_session['username']))
                print('filter', CustomUser.objects.filter(username=user_session['username']))
                print('*********************************************************')
                user = CustomUser.objects.get(phone_number=user_session['phone_number'])
                user.is_active = True
                user.username += '@zyo.com'
                user.save()

                # CustomUser.save()

                code_instance.delete()
                messages.success(request, 'you registered.', 'success')
                return HttpResponse("you saved!")
            else:
                messages.error(request, 'this code is wrong', 'danger')
                return redirect('verify_code')


class UserLogin(View):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {"forms": form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user_login = CustomUser.objects.get(username=cd["username"])
            if user_login.check_password(cd['password']):
                login(request, user_login)
                messages.success(request, 'you logged successfully ', 'success')
                return redirect('email_view')
            # user = authenticate(request, username=cd["username"], password=cd['password'])
            # if user is not None:
            #     login(request, user)
            #     messages.success(request, 'you logged successfully ', 'success')
            #     return redirect('home')
            messages.error(request, "user name or password is wrong", 'error')
            return render(request, self.template_name, {"forms": form})


class ResetPassword(View):
    form_class = ResetPasswordForm
    template_name = 'users/reset_password.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'forms': form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            if form.cleaned_data['recovery_email']:
                # user = form.save(commit=False)
                user = CustomUser.objects.get(recovery_email=form.cleaned_data['recovery_email'])

                # user_pk = CustomUser.objects.get(recovery_email=form.cleaned_data['recovery_email']).pk
                print('**********************************************************************************')
                print(user.id)
                print('**********************************************************************************')
                current_site = get_current_site(request)

                mail_subject = "Reset your password's account."
                message = render_to_string('users/reset_password_account.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('recovery_email')
                email = EmailMessage(
                    mail_subject, message, to=[to_email]
                )
                email.send()
                messages.success(request, 'Please Confirm your email to reset password.')
                return HttpResponse('Link sent to your email!')
            if not form.cleaned_data['recovery_email']:
                messages.warning(request, 'This email does not exist!!')
            if form.cleaned_data['phone_number']:
                random_code = random.randint(1000, 9999)
                send_otp_code(form.cleaned_data['phone_number'], random_code)
                OtpCode.objects.create(phone_number=form.cleaned_data['phone_number'], code=random_code)
                request.session['user_reset_password'] = {
                    'phone_number': form.cleaned_data['phone_number']
                }
                messages.success(request, 'we sent you a code', 'success')
                return redirect('reset_password_confirm_phone')
            return render(request, self.template_name, {'forms': form})

        else:
            messages.error(request,
                           f"You must be enter email or phone number!!!!",
                           extra_tags='permanent error')
            storage = messages.get_messages(request)
            for message in storage:
                print(message)
            storage.used = False
            return render(request, 'users/register.html', {"forms": form})


def reset_password_confirm(request, uidb64, token, *args, **kwargs):
    try:
        uid = force_str(s=urlsafe_base64_decode(uidb64).decode(), strings_only=True)
        user = CustomUser.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        form_class = ResetPasswordConfirmForm
        if request.method == 'GET':
            return render(request, 'users/reset_password_form.html', {"forms": form_class})
        elif request.method == 'POST':
            form = form_class(request.POST)
            if form.is_valid():
                user_complete_new_password = form.cleaned_data['password1']
                user.set_password(user_complete_new_password)
                user.save()
                return HttpResponse('Your password is confirmed successfully!')
    else:
        return HttpResponse('Activation link is invalid!')


class UserResetPasswordVerifyCodeView(View):
    form_class = VerifyCodeForm

    def get(self, request):
        form = self.form_class
        return render(request, 'users/verify.html', {'form': form})

    def post(self, request):
        user_session = request.session['user_reset_password']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == code_instance.code:
                code_instance.delete()
                return redirect('reset_password_confirm_phone_complete')
            else:
                messages.error(request, 'this code is wrong', 'danger')
                return redirect('verify_code')


class ResetPasswordConfirmByPhone(View):
    form_class = ResetPasswordConfirmForm
    template_name = 'users/reset_password_form.html'

    def get(self, request):
        return render(request, 'users/reset_password_form.html', {"forms": self.form_class})

    def post(self, request):
        user_session = request.session['user_reset_password']
        user = CustomUser.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            user_complete_new_password = form.cleaned_data['password1']
            user.set_password(user_complete_new_password)
            user.save()
            messages.success(request, 'your password confirmed successfully.', 'success')
            return HttpResponse('Your password is confirmed successfully!')


class UserLogoutView(LoginRequiredMixin, View):
    # login_url = '/user/login/'
    def get(self, request):
        logout(request)
        messages.success(request, 'you logout successfully', 'success')
        return redirect('home')
