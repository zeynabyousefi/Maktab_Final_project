import email.errors

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views import View
from django.contrib import messages
from django.views.generic import ListView
from django.core.files.storage import FileSystemStorage

# Create your views here.
from emails.models import *


class AddNewEmail(LoginRequiredMixin, View):
    template_name = 'emails/compose.html'
    user_instance = ''

    def get(self, request):
        return render(request, self.template_name)

    @staticmethod
    def get_user_is_exist(user):
        if CustomUser.objects.get(username=user):
            return True
        else:
            return False

    def post(self, request):
        to = request.POST['to']
        cc = request.POST['cc']
        bcc = request.POST['bcc']
        subject = request.POST['subject']
        body = request.POST['body']
        inbox = EmailPlaceHolders.objects.get(place_holder='inbox')
        sentbox = EmailPlaceHolders.objects.get(place_holder='sentbox')
        drafts = EmailPlaceHolders.objects.get(place_holder='drafts')

        try:
            attachment = request.FILES['file']

        except:
            attachment = False
        try:
            subject = request.POST['subject']
        except:
            subject = False

        if request.POST['to'] != '':
            user_to = request.POST['to']
            to = CustomUser.objects.get(username=to)
            try:
                if self.get_user_is_exist(user=user_to):
                    to = CustomUser.objects.get(username=user_to)
                    if (cc == '') and (bcc == ''):
                        email = Email(subject=subject,
                                      body=body,
                                      author=request.user,
                                      attachment=attachment,
                                      to=to,
                                      cc='',
                                      bcc='',
                                      )
                        email.save()
                        user_email_mapped_sender = UserEmailMapped(email=email,
                                                                   place_holder=sentbox,
                                                                   user=request.user)
                        user_email_mapped_sender.save()
                        user_email_mapped_receiver = UserEmailMapped(email=email,
                                                                     place_holder=inbox,
                                                                     user=to)
                        user_email_mapped_receiver.save()
                        messages.success(request, "Email sent successfully", 'success')
                    elif (cc != '') and (bcc != ''):
                        cc = CustomUser.objects.get(username=cc)
                        bcc = CustomUser.objects.get(username=bcc)
                        email = Email(subject=subject,
                                      body=body,
                                      author=request.user,
                                      attachment=attachment,
                                      to=user_to,
                                      cc=cc,
                                      bcc=bcc,
                                      )
                        email.save()
                        user_email_mapped_sender = UserEmailMapped(email=email,
                                                                   place_holder=sentbox,
                                                                   user=request.user)
                        user_email_mapped_sender.save()
                        receivers = [to, cc, bcc]
                        for receiver in receivers:
                            user_email_mapped_receiver = UserEmailMapped(email=email,
                                                                         place_holder=inbox,
                                                                         user=receiver)
                            user_email_mapped_receiver.save()
                        messages.success(request, "Email sent successfully", 'success')
                    elif (cc != '') and (bcc == ''):
                        cc = CustomUser.objects.get(username=cc)
                        email = Email(subject=subject,
                                      body=body,
                                      author=request.user,
                                      attachment=attachment,
                                      to=user_to,
                                      cc=cc,
                                      bcc='',
                                      )
                        email.save()
                        user_email_mapped_sender = UserEmailMapped(email=email,
                                                                   place_holder=sentbox,
                                                                   user=request.user)
                        user_email_mapped_sender.save()
                        receivers = [to, cc]
                        for receiver in receivers:
                            user_email_mapped_receiver = UserEmailMapped(email=email,
                                                                         place_holder=inbox,
                                                                         user=receiver)
                            user_email_mapped_receiver.save()
                        messages.success(request, "Email sent successfully", 'success')
                    elif (bcc != '') and (cc == ''):
                        # cc = CustomUser.objects.get(username=cc)
                        bcc = CustomUser.objects.get(username=bcc)
                        email = Email(subject=subject,
                                      body=body,
                                      author=request.user,
                                      attachment=attachment,
                                      to=user_to,
                                      cc='',
                                      bcc=bcc,
                                      )
                        email.save()
                        user_email_mapped_sender = UserEmailMapped(email=email,
                                                                   place_holder=sentbox,
                                                                   user=request.user)
                        user_email_mapped_sender.save()
                        receivers = [to, bcc]
                        for receiver in receivers:
                            user_email_mapped_receiver = UserEmailMapped(email=email,
                                                                         place_holder=inbox,
                                                                         user=receiver)
                            user_email_mapped_receiver.save()
                        messages.success(request, "Email sent successfully", 'success')
            except CustomUser.DoesNotExist:
                messages.error(request, "email is not correct", 'danger')

            return redirect('email_view')

        elif to == '':
            if (cc == '') and (bcc == ''):
                drafts = EmailPlaceHolders.objects.get(place_holder='drafts')
                email = Email(subject=subject,
                              body=body,
                              author=request.user,
                              attachment=attachment,
                              to='',
                              cc='',
                              bcc='',
                              )
                email.save()
                user_email_mapped = UserEmailMapped(email=email,
                                                    place_holder=drafts,
                                                    user=request.user)
                user_email_mapped.save()
            elif (cc != '') and (bcc != ''):
                cc = CustomUser.objects.get(username=cc)
                bcc = CustomUser.objects.get(username=bcc)
                email = Email(subject=subject,
                              body=body,
                              author=request.user,
                              attachment=attachment,
                              to='',
                              cc=cc,
                              bcc=bcc,
                              )
                email.save()
                user_email_mapped_sender = UserEmailMapped(email=email,
                                                           place_holder=sentbox,
                                                           user=request.user)
                user_email_mapped_sender.save()
                receivers = [cc, bcc]
                for receiver in receivers:
                    user_email_mapped_receiver = UserEmailMapped(email=email,
                                                                 place_holder=inbox,
                                                                 user=receiver)
                    user_email_mapped_receiver.save()
                messages.success(request, "Email sent successfully", 'success')
            elif (cc != '') and (bcc == ''):
                cc = CustomUser.objects.get(username=cc)
                # bcc = CustomUser.objects.get(username=bcc)
                email = Email(subject=subject,
                              body=body,
                              author=request.user,
                              attachment=attachment,
                              to='',
                              cc=cc,
                              bcc='',
                              )
                email.save()
                user_email_mapped_sender = UserEmailMapped(email=email,
                                                           place_holder=sentbox,
                                                           user=request.user)
                user_email_mapped_sender.save()
                receivers = [cc]
                for receiver in receivers:
                    user_email_mapped_receiver = UserEmailMapped(email=email,
                                                                 place_holder=inbox,
                                                                 user=receiver)
                    user_email_mapped_receiver.save()
                messages.success(request, "Email sent successfully", 'success')
            elif (bcc != '') and (cc == ''):
                # cc = CustomUser.objects.get(username=cc)
                user_bcc = CustomUser.objects.get(username=bcc)
                email = Email(subject=subject,
                              body=body,
                              author=request.user,
                              attachment=attachment,
                              to='',
                              cc='',
                              bcc=user_bcc,
                              )
                email.save()
                user_email_mapped_sender = UserEmailMapped(email=email,
                                                           place_holder=sentbox,
                                                           user=request.user)
                user_email_mapped_sender.save()
                receivers = [user_bcc]
                for receiver in receivers:
                    user_email_mapped_receiver = UserEmailMapped(email=email,
                                                                 place_holder=inbox,
                                                                 user=receiver)
                    user_email_mapped_receiver.save()
                messages.success(request, "Email sent successfully", 'success')

            return redirect('email_view')


class EmailSentboxView(LoginRequiredMixin, ListView):
    model = UserEmailMapped
    template_name = 'emails/sentbox.html'

    def get_queryset(self):
        place_holder = EmailPlaceHolders.objects.get(place_holder='sentbox')
        print(place_holder)
        user_sentbox = UserEmailMapped.objects.filter(user=self.request.user, place_holder=place_holder)
        return UserEmailMapped.objects.filter(user=self.request.user, place_holder=place_holder)


class EmailInboxView(LoginRequiredMixin, ListView):
    model = UserEmailMapped
    template_name = 'emails/inbox.html'

    def get_queryset(self):
        print('*************************************************************')
        print(self.request.user)
        print('*************************************************************')
        place_holder = EmailPlaceHolders.objects.get(place_holder='inbox')
        print(place_holder)
        user_inbox = UserEmailMapped.objects.filter(user=self.request.user, place_holder=place_holder)
        print('*************************************************************')
        print(user_inbox)
        print('*************************************************************')
        return UserEmailMapped.objects.filter(user=self.request.user, place_holder=place_holder)


class EmailDraftsView(LoginRequiredMixin, ListView):
    model = UserEmailMapped
    template_name = 'emails/drafts.html'

    def get_queryset(self):
        place_holder = EmailPlaceHolders.objects.get(place_holder='drafts')
        print(place_holder)
        return UserEmailMapped.objects.filter(user=self.request.user, place_holder=place_holder)


class DetailEmailView(LoginRequiredMixin, View):
    template = 'emails/detail.html'

    def setup(self, request, *args, **kwargs):
        self.email_instance = get_object_or_404(Email, pk=kwargs['email_id'])
        return super().setup(request, *args, **kwargs)

    def get(self, request, email_id):
        email = Email.objects.get(pk=email_id)
        return render(request, self.template, {'object': email})


class AddLabelView(LoginRequiredMixin, View):
    template_name = 'layout/_base.html'

    def get_queryset(self):
        labels = EmailPlaceHolders.objects.filter(creator=self.request.user)
        return EmailPlaceHolders.objects.filter(creator=self.request.user)

    def get(self, request):
        return render(request, 'emails/add_label.html')

    def post(self, request):
        place_holder = request.POST['place_holder']
        label = EmailPlaceHolders(place_holder=place_holder, creator=request.user)
        label.save()

        return redirect('email_view')
