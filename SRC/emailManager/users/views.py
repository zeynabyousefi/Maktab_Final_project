import csv
import random
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, HttpResponse, get_object_or_404
from .models import *
from django.views import View
from .forms import *
from django.contrib import messages
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
from emails.models import *
from django.contrib.auth import authenticate
from emails.forms import SearchBox

# Create your views here.

class Index(View):

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            inbox_view =  EmailPlaceHolders.objects.get(place_holder="inbox")
            user_is_read = UserEmailMapped.objects.filter(place_holder=inbox_view,is_read=False,user=request.user).count()
            print("M"*80)
            print(user_is_read)
            return redirect('email_view')
        else:
            return render(request, 'layout/_base.html')


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
                messages.success(request, 'we sent you email', 'success')
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
                    'birthdate': form.cleaned_data['birthdate'],
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
        user.username += '@email.com'
        user.save()
        # folders = ['inbox', 'sentbox', 'trash', 'draft']
        # for folder in folders:
        #     email_place_holder = EmailPlaceHolders()
        #     email_place_holder.place_holder = folder
        #     email_place_holder.save()
        login(request, user)
        # return redirect('home')
        return redirect('email_view')
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
                user.username += '@email.com'
                user.save()
                # folders = ['inbox', 'sentbox', 'trash', 'draft']
                # for folder in folders:
                #     email_place_holder = EmailPlaceHolders()
                #     email_place_holder.place_holder = folder
                #     email_place_holder.save()
                # CustomUser.save()

                code_instance.delete()
                messages.success(request, 'you registered.', 'success')
                login(request, user)
                return redirect("email_view")
            else:
                messages.error(request, 'this code is wrong', 'danger')
                return redirect('verify_code')


class UserLogin(View):
    form_class = UserLoginForm
    template_name = 'users/login.html'

    # def dispatch(self, request, *args, **kwargs):
    #     if request.user.is_authenticated:
    #         return redirect('home')
    #     return super().dispatch(request, *args, **kwargs)

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
                return redirect('user_login')
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
            return redirect('user_login')


class UserLogoutView(LoginRequiredMixin, View):
    # login_url = '/user/login/'
    def get(self, request):
        logout(request)
        messages.success(request, 'you logout successfully', 'success')
        return redirect('home')


class UserContactView(LoginRequiredMixin, View):
    form_class = AddContact
    template_name = 'users/add_contact.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'forms': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_contact = form.save(commit=False)
            new_contact.owner_contact = request.user
            new_contact.save()
            messages.success(request, f'You Add {cd["name"]} in your contact', 'success')
            return redirect('email_view')
        return HttpResponse(form.errors)


class ShowAllContact(LoginRequiredMixin, View):
    template = 'users/all_contact.html'

    def get(self, request):
        all_contact = Contact.objects.filter(owner_contact=request.user.id)
        return render(request, self.template, {"all_contact": all_contact})


class DetailContactView(LoginRequiredMixin, View):
    template = 'users/detail_contact.html'

    def setup(self, request, *args, **kwargs):
        self.email_instance = get_object_or_404(Contact, pk=kwargs['contact_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, contact_id):
        contact = Contact.objects.get(pk=contact_id)
        return render(request, self.template, {'contact': contact})


class Update(LoginRequiredMixin, View):
    form_class = AddContact
    template = 'users/update_contact.html'

    def setup(self, request, *args, **kwargs):
        self.contact_instance = Contact.objects.get(pk=kwargs["contact_id"])
        return super().setup(request, *args, **kwargs)

    # def dispatch(self, request, *args, **kwargs):
    #     conatct= self.contact_instance
    #     if not conatct.user.id == request.user.id:
    #         messages.error(request, 'you can not edit', 'danger')
    #         return redirect('home')
    #     return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        conatct = self.contact_instance
        form = self.form_class(instance=conatct)
        return render(request, self.template, {'forms': form})

    def post(self, request, *args, **kwargs):
        conatct = self.contact_instance
        form = self.form_class(request.POST, instance=conatct)
        if form.is_valid():
            update_conatct = form.save(commit=False)
            update_conatct.owner_contact = request.user
            update_conatct.save()
            messages.success(request, "updated post", 'success')
            return redirect('detail_contact', update_conatct.id)


class ContactDelete(LoginRequiredMixin, View):
    def get(self, request, contact_id):
        contact = Contact.objects.get(pk=contact_id)
        contact.delete()
        messages.success(request, "delete was successfully", 'success')
        return redirect('all_contacts')


def export_contact_csv(request):
    contacts = Contact.objects.filter(owner_contact=request.user)
    # return HttpResponse(contacts)
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=contacts.csv'
    writer = csv.writer(response)
    writer.writerow(['ID', 'owner_contact', 'phone', 'Name', 'Email', 'Birthdate'])
    studs = contacts.values_list('id', 'owner_contact', 'phone', 'name', 'email', 'birthdate')
    for std in studs:
        writer.writerow(std)
    return response


class SearchContacts(LoginRequiredMixin, View):

    def get(self, request):
        user_contacts = Contact.objects.filter(owner_contact=request.user)
        form = SearchBox()
        final_query = Q()
        if 'search' in request.GET:
            form = SearchBox(request.GET)
            if form.is_valid():
                cd = form.cleaned_data['search']
                for item in user_contacts:
                    final_query.add(
                        Q(
                            name__icontains=cd,

                        ) |
                        Q(email__icontains=cd) |
                        Q(phone__icontains=cd),
                        Q.OR
                    )
                search = Contact.objects.filter(final_query, owner_contact=request.user)
        return render(request, 'users/search_contact.html', {'search': search})


class AddSignature(LoginRequiredMixin, View):
    template_name = 'users/add_signature.html'
    form = AddSignatureForm

    def get(self, request):
        return render(request, self.template_name, {'forms': self.form})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            add_signature = form.save(commit=False)
            add_signature.owner = request.user
            add_signature.save()
            return redirect('setting')
