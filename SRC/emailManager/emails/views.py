import email.errors
from django.contrib.postgres.search import SearchVector
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models.fields import json
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views import View
from django.contrib import messages
from django.views.generic import ListView
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required
from .forms import SearchBox
# Create your views here.
from emails.models import *
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest
from users.models import Signature

class AddNewEmail(LoginRequiredMixin, View):
    template_name = 'emails/compose.html'
    user_instance = ''

    def get(self, request):
        signature = Signature.objects.filter(owner=request.user)
        return render(request, self.template_name, {'signatures': signature})

    @staticmethod
    def get_user_is_exist(user):
        if CustomUser.objects.get(username=user):
            return True
        else:
            return False

    def post(self, request):
        # signature = Signature.objects.get(pk=self.signature_id).content
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

        def save_email():
            email = Email(subject=subject,
                          body=body,
                          attachment=attachment,
                          author=request.user,
                          )
            email.save()
            return email

        def create_receiver(receiver, email, is_to=False, is_cc=False, is_bcc=False):
            email_receiver = EmailReceiver(email=email)
            email_receiver.save()
            for receiver in receiver.split(','):
                receiver = receiver.strip()
                if CustomUser.objects.filter(username=receiver).exists():
                    receiver = CustomUser.objects.get(username=receiver)
                    if is_to:
                        email_receiver.to.add(receiver)
                    elif is_cc:
                        email_receiver.cc.add(receiver)
                    elif is_bcc:
                        email_receiver.bcc.add(receiver)
                    user_email_mapped_receiver = UserEmailMapped(email=email,
                                                                 place_holder=inbox,
                                                                 user=receiver)
                    user_email_mapped_receiver.save()
            user_email_mapped_sender = UserEmailMapped(email=email,
                                                       place_holder=sentbox,
                                                       user=request.user)
            user_email_mapped_sender.save()

        if to != '':
            if cc == '' and bcc == '':
                email = save_email()
                email_receiver = EmailReceiver(email=email)
                email_receiver.save()
                for to in to.split(','):
                    to = to.strip()
                    if CustomUser.objects.filter(username=to).exists():
                        to = CustomUser.objects.get(username=to)
                        email_receiver.to.add(to)
                        user_email_mapped_receiver = UserEmailMapped(email=email,
                                                                     place_holder=inbox,
                                                                     user=to)
                        user_email_mapped_receiver.save()
                user_email_mapped_sender = UserEmailMapped(email=email,
                                                           place_holder=sentbox,
                                                           user=request.user)
                user_email_mapped_sender.save()
                messages.success(request, 'Your email sent successfully!')
            if cc != '' and bcc == '':
                email = save_email()
                email_receiver = EmailReceiver(email=email)
                email_receiver.save()
                for to in to.split(','):
                    to = to.strip()
                    if CustomUser.objects.filter(username=to).exists():
                        to = CustomUser.objects.get(username=to)
                        email_receiver.to.add(to)
                        user_email_mapped_receiver = UserEmailMapped(email=email,
                                                                     place_holder=inbox,
                                                                     user=to)
                        user_email_mapped_receiver.save()

                for cc in cc.split(','):
                    cc = cc.strip()
                    if CustomUser.objects.filter(username=cc).exists():
                        cc = CustomUser.objects.get(username=cc)
                        email_receiver.cc.add(cc)
                        user_email_mapped_receiver = UserEmailMapped(email=email,
                                                                     place_holder=inbox,
                                                                     user=cc)
                        user_email_mapped_receiver.save()
                user_email_mapped_sender = UserEmailMapped(email=email,
                                                           place_holder=sentbox,
                                                           user=request.user)
                user_email_mapped_sender.save()
                messages.success(request, 'Your email sent successfully!')
            if cc == '' and bcc != '':
                email = save_email()
                email_receiver = EmailReceiver(email=email)
                email_receiver.save()
                for to in to.split(','):
                    to = to.strip()
                    if CustomUser.objects.filter(username=to).exists():
                        to = CustomUser.objects.get(username=to)
                        email_receiver.to.add(to)
                        user_email_mapped_receiver = UserEmailMapped(email=email,
                                                                     place_holder=inbox,
                                                                     user=to)
                        user_email_mapped_receiver.save()
                for bcc in bcc.split(','):
                    bcc = bcc.strip()
                    if CustomUser.objects.filter(username=bcc).exists():
                        bcc = CustomUser.objects.get(username=bcc)
                        email_receiver.bcc.add(bcc)
                        user_email_mapped_receiver = UserEmailMapped(email=email,
                                                                     place_holder=inbox,
                                                                     user=bcc)
                        user_email_mapped_receiver.save()
                user_email_mapped_sender = UserEmailMapped(email=email,
                                                           place_holder=sentbox,
                                                           user=request.user)
                user_email_mapped_sender.save()
                messages.success(request, 'Your email sent successfully!')
            if cc != '' and bcc != '':
                email = save_email()
                email_receiver = EmailReceiver(email=email)
                email_receiver.save()
                for to in to.split(','):
                    to = to.strip()
                    if CustomUser.objects.filter(username=to).exists():
                        to = CustomUser.objects.get(username=to)
                        email_receiver.to.add(to)
                        user_email_mapped_receiver = UserEmailMapped(email=email,
                                                                     place_holder=inbox,
                                                                     user=to)
                        user_email_mapped_receiver.save()
                for cc in cc.split(','):
                    cc = cc.strip()
                    if CustomUser.objects.filter(username=cc).exists():
                        cc = CustomUser.objects.get(username=cc)
                        email_receiver.cc.add(cc)
                        user_email_mapped_receiver = UserEmailMapped(email=email,
                                                                     place_holder=inbox,
                                                                     user=cc)
                        user_email_mapped_receiver.save()
                for bcc in bcc.split(','):
                    bcc = bcc.strip()
                    if CustomUser.objects.filter(username=bcc).exists():
                        bcc = CustomUser.objects.get(username=bcc)
                        email_receiver.bcc.add(bcc)
                        user_email_mapped_receiver = UserEmailMapped(email=email,
                                                                     place_holder=inbox,
                                                                     user=bcc)
                        user_email_mapped_receiver.save()
                user_email_mapped_sender = UserEmailMapped(email=email,
                                                           place_holder=sentbox,
                                                           user=request.user)
                user_email_mapped_sender.save()
                messages.success(request, 'Your email sent successfully!')
        elif to == '':
            if cc == '' and bcc == '':
                email = save_email()
                user_email_mapped_sender = UserEmailMapped(email=email,
                                                           place_holder=drafts,
                                                           user=request.user)
                user_email_mapped_sender.save()
                messages.success(request, 'Your email moved to drafts!!')
            if cc != '' and bcc == '':
                email = save_email()
                email_receiver = EmailReceiver(email=email)
                email_receiver.save()
                for cc in cc.split(','):
                    cc = cc.strip()
                    if CustomUser.objects.filter(username=cc).exists():
                        cc = CustomUser.objects.get(username=cc)
                        email_receiver.cc.add(cc)
                        user_email_mapped_receiver = UserEmailMapped(email=email,
                                                                     place_holder=inbox,
                                                                     user=cc)
                        user_email_mapped_receiver.save()
                user_email_mapped_sender = UserEmailMapped(email=email,
                                                           place_holder=sentbox,
                                                           user=request.user)
                user_email_mapped_sender.save()
                messages.success(request, 'Your email sent successfully!')
            if cc == '' and bcc != '':
                email = save_email()
                email_receiver = EmailReceiver(email=email)
                email_receiver.save()
                for bcc in bcc.split(','):
                    bcc = bcc.strip()
                    if CustomUser.objects.filter(username=bcc).exists():
                        bcc = CustomUser.objects.get(username=bcc)
                        email_receiver.bcc.add(bcc)
                        user_email_mapped_receiver = UserEmailMapped(email=email,
                                                                     place_holder=inbox,
                                                                     user=bcc)
                        user_email_mapped_receiver.save()
                user_email_mapped_sender = UserEmailMapped(email=email,
                                                           place_holder=sentbox,
                                                           user=request.user)
                user_email_mapped_sender.save()
                messages.success(request, 'Your email sent successfully!')
            if cc != '' and bcc != '':
                email = save_email()
                email_receiver = EmailReceiver(email=email)
                email_receiver.save()
                for cc in cc.split(','):
                    cc = cc.strip()
                    if CustomUser.objects.filter(username=cc).exists():
                        cc = CustomUser.objects.get(username=cc)
                        email_receiver.cc.add(cc)
                        user_email_mapped_receiver = UserEmailMapped(email=email,
                                                                     place_holder=inbox,
                                                                     user=cc)
                        user_email_mapped_receiver.save()

                for bcc in bcc.split(','):
                    bcc = bcc.strip()
                    if CustomUser.objects.filter(username=bcc).exists():
                        bcc = CustomUser.objects.get(username=bcc)
                        email_receiver.bcc.add(bcc)
                        user_email_mapped_receiver = UserEmailMapped(email=email,
                                                                     place_holder=inbox,
                                                                     user=bcc)
                        user_email_mapped_receiver.save()
                user_email_mapped_sender = UserEmailMapped(email=email,
                                                           place_holder=sentbox,
                                                           user=request.user)
                user_email_mapped_sender.save()
                messages.success(request, 'Your email sent successfully!')
        return redirect('email_view')


class EmailSentboxView(LoginRequiredMixin, View):
    model = UserEmailMapped
    template_name = 'emails/sentbox.html'

    def get(self, request):
        place_holder = EmailPlaceHolders.objects.get(place_holder='sentbox')
        print(place_holder)
        user_sentbox = UserEmailMapped.objects.filter(user=self.request.user, place_holder=place_holder)
        # email_user = Email.objects.filter(author=request.user)
        email_receiver = EmailReceiver
        return render(request, self.template_name, {"object_list": user_sentbox, "receiver": email_receiver})


class EmailInboxView(LoginRequiredMixin, View):
    model = UserEmailMapped
    template_name = 'emails/inbox.html'

    def get(self, request):
        place_holder = EmailPlaceHolders.objects.get(place_holder='inbox')
        user_inbox = UserEmailMapped.objects.filter(user=self.request.user, place_holder=place_holder)
        # label = EmailPlaceHolders.objects.filter(creator=request.user)
        return render(request, self.template_name, {'inbox': user_inbox})


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
        try:
            to = EmailReceiver.objects.get(email=email).to.exists()
        except:
            to = ''
        try:
            cc = EmailReceiver.objects.get(email=email).cc
        except:
            cc = ''
        has_bcc = False
        try:
            bcc = EmailReceiver.objects.get(email=email).bcc
            if bcc.exists():
                has_bcc = True
        except:
            bcc = ''

        return render(request, self.template, {'object': email, "to": to, "cc": cc, "bcc": bcc, "has_bcc": has_bcc})


class AddLabelView(LoginRequiredMixin, View):
    template_name = 'layout/_base.html'

    def get_queryset(self):
        labels = EmailPlaceHolders.objects.filter(creator=self.request.user)
        return EmailPlaceHolders.objects.filter(creator=self.request.user)

    def get(self, request):
        label = EmailPlaceHolders.objects.filter(creator=request.user)
        return render(request, 'emails/add_label.html')

    def post(self, request):
        place_holder = request.POST['place_holder']
        label = EmailPlaceHolders(place_holder=place_holder, creator=request.user)
        label.save()

        return redirect('email_view')


class AddLabelEmail(LoginRequiredMixin, View):
    def get(self, request, email_id, label_id):
        email = Email.objects.get(pk=email_id)
        label = EmailPlaceHolders.objects.get(pk=label_id)
        inbox = EmailPlaceHolders.objects.get(place_holder='inbox')
        # user_email_mapped = UserEmailMapped.objects.filter(place_holder=inbox, user=request.user, email=email)
        user_email_mapped_new = UserEmailMapped(place_holder=label,
                                                user=request.user,
                                                email=email)
        user_email_mapped_new.save()
        return redirect('label_view')


class EmailTrashView(LoginRequiredMixin, View):
    model = UserEmailMapped
    template_name = 'emails/trash.html'

    def get(self, request):
        place_holder = EmailPlaceHolders.objects.get(place_holder='trash')
        user_trash = UserEmailMapped.objects.filter(user=self.request.user, place_holder=place_holder)
        label = EmailPlaceHolders.objects.filter(creator=request.user)
        return render(request, self.template_name, {'trash': user_trash, "label": label})


class DeleteEmail(LoginRequiredMixin, View):

    def get(self, request, email_id):
        email = Email.objects.get(pk=email_id)
        trash = EmailPlaceHolders.objects.get(place_holder='trash')
        inbox = EmailPlaceHolders.objects.get(place_holder='inbox')
        user_email_mapped = UserEmailMapped.objects.filter(place_holder=inbox, user=request.user, email=email)
        user_email_mapped.update(place_holder=trash)
        return redirect('email_trash')


class LabelView(LoginRequiredMixin, View):
    template_name = 'emails/inbox.html'

    def get(self, request):
        label = EmailPlaceHolders.objects.filter(creator=request.user)
        print('3' * 90)
        print(label)
        print('3' * 90)
        return render(request, self.template_name, {"labels": label})


class DetailLabel(LoginRequiredMixin, View):
    template_name = 'emails/label_view.html'

    def get(self, request, label_id):
        email = UserEmailMapped.objects.filter(place_holder=label_id)
        return render(request, self.template_name, {"email": email, 'place_holder': label_id})


class DeleteLabel(LoginRequiredMixin, View):
    def get(self, request, label_id):
        label = EmailPlaceHolders.objects.get(pk=label_id)
        emails = UserEmailMapped.objects.filter(place_holder=label)
        inbox = EmailPlaceHolders.objects.get(place_holder='inbox')
        for email in emails:
            user_email_mapped = UserEmailMapped.objects.filter(place_holder=label, user=request.user, email=email.email)
            user_email_mapped.delete()
            label.delete()
        messages.success(request, "delete was successfully", 'success')
        return redirect('email_view')


class EmailArchiveAdd(LoginRequiredMixin, View):
    def get(self, request, email_id):
        email = Email.objects.get(pk=email_id)
        archive = EmailPlaceHolders.objects.get(place_holder="archive")
        inbox = EmailPlaceHolders.objects.get(place_holder='inbox')
        user_email_mapped = UserEmailMapped.objects.filter(place_holder=inbox, user=request.user, email=email)
        user_email_mapped.update(place_holder=archive)
        return redirect('email_archive')


class EmailArchiveView(LoginRequiredMixin, View):
    template_name = 'emails/archive.html'

    def get(self, request):
        place_holder = EmailPlaceHolders.objects.get(place_holder='archive')
        email = UserEmailMapped.objects.filter(place_holder=place_holder, user=request.user)
        return render(request, self.template_name, {"email": email})


class Search(LoginRequiredMixin, View):
    def get(self, request):
        user_email_mapped = UserEmailMapped.objects.filter(user=request.user)
        print('^' * 60)
        print(request.user)
        print('^' * 60)
        form = SearchBox()
        final_query = Q()
        if 'search' in request.GET:
            form = SearchBox(request.GET)
            if form.is_valid():
                cd = form.cleaned_data['search']
                for item in user_email_mapped:
                    final_query.add(
                        Q(
                            email__subject__icontains=cd,

                        ) |
                        Q(email__body__icontains=cd) |
                        Q(email__author__username__icontains=cd),
                        Q.OR
                    )
                    print('#' * 60)
                    print(final_query)
                    print(user_email_mapped)
                    print('#' * 60)
                search = UserEmailMapped.objects.filter(final_query, user=request.user)
        return render(request, 'emails/search.html', {'search': search})


class Setting(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'emails/setting.html')
