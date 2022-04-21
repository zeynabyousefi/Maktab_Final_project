from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.db.models import Q
from django.contrib import messages


@login_required
def labels(request):
    form = SearchBox()
    admin = CustomUser.objects.get(username="1234")
    label = EmailPlaceHolders.objects.filter(Q(creator=request.user) | Q(creator=admin))
    inbox = EmailPlaceHolders.objects.get(place_holder="inbox")
    is_read = UserEmailMapped.objects.filter(is_read=False, place_holder=inbox
                                             , user=request.user).count()

    if is_read != 0:
        messages.success(request, 'you have new email.', 'success')

    return {'labels': label, "form": form, "read": is_read}
