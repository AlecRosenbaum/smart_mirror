import uuid

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.urls import reverse

from accounts.models import UserProfile

from .forms import UserForm, ProfileForm
from .models import ShortMirror

@login_required
@transaction.atomic
def settings(request):
    """settings page"""

    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.userprofile)

        # check for errors and save

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('settings')
        else:
            messages.error(request, 'user_form ' + str(user_form.is_valid()))
            messages.error(request, 'profile_form ' + str(profile_form.is_valid()))
            messages.error(request, 'Please correct the error below.')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.userprofile)

    return render(request, 'display/settings.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'mirror_id': "12345",
    })

def app(request, account=0):
    # if mirror uuid isn't defined
    if 'mirror_uuid' not in request.COOKIES:
        return redirect('pair')

    # lookup display values
    mirror_uuid = request.COOKIES['mirror_uuid']
    userprofiles = UserProfile.objects.filter(mirror=uuid.UUID(mirror_uuid))

    # if none linked, redirect to pair
    if len(userprofiles) == 0:
        return redirect('pair')

    context = {
        'bus_stop': userprofiles[account].bus_stop,
        'ical_link': userprofiles[account].ical_link,
    }
    return render(request, 'display/app.html', context)

def pair(request, form_val=None):
    # if new mirror visits
    if 'mirror_uuid' not in request.COOKIES:
        response = render(request, 'display/pair.html')
        response.set_cookie('mirror_uuid', str(uuid.uuid4()))
        return response

    # setup maired mirror in database
    if request.method == 'POST':
        # basic validation
        if 'short_id' in request.POST:
            # link mirror to account
            try:
                sm_inst = ShortMirror.objects.get(short_id=request.POST['short_id'])
            except:
                return redirect(reverse('pair', kwargs={'form_val': request.POST['short_id']}))
            sm_inst.user.mirror = uuid.UUID(request.COOKIES['mirror_uuid'])
            sm_inst.user.save()
            return redirect('app')


    return render(request, 'display/pair.html', {"value": form_val})

def new(request):
    return HttpResponse('Nothing here yet.')
