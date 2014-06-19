from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from carnique.profile.models import UserProfile
from carnique.main.views import cnq_render_to_response, get_carnique_user
from carnique.utils import convert_bb_to_html

import datetime

def profile_view(request, username):
    u = get_carnique_user(username)

    if not u:
        raise Http404()

    profile_text = convert_bb_to_html(u.get_profile().text)

    return cnq_render_to_response('profile.html', request, {
        'puser': u,
        'profile_text': profile_text,
    })

def _can_edit_profile(username, user):
    if user.username == username:
        return True

    return False


@login_required
def profile_edit(request, username):
    u = get_carnique_user(username)

    if not u:
        raise Http404()

    editing_user = request.user
    profile_raw = u.get_profile().text
    profile_html = convert_bb_to_html(profile_raw)

    if not _can_edit_profile(username, editing_user):
        return cnq_render_to_response('profile.html', request, {
            'puser': u,
            'profile_text': profile_html,
            'body_top_error': 'You cannot edit this profile.',
        })

    if not 'profile_birthday' in request.POST:
        return cnq_render_to_response('profile_edit.html', request, {
            'puser': u,
            'profile': u.get_profile(),
            'profile_text': profile_raw,
        })

    # Verify and commit changes
    if u.get_profile().text != request.POST['profile_text']:
        u.get_profile().text = request.POST['profile_text']
        u.get_profile().last_updated = datetime.datetime.now()

    u.get_profile().realname         = request.POST['profile_realname']
    u.get_profile().location         = request.POST['profile_location']
    u.get_profile().twitter_username = request.POST['profile_twitter_username']
    u.get_profile().blog_url         = request.POST['profile_blog_url']
    u.get_profile().blog_name        = request.POST['profile_blog_name']

    if request.POST['profile_birthday']:
        u.get_profile().birthday = request.POST['profile_birthday']

    u.save()
    u.get_profile().save()

    profile_text = convert_bb_to_html(u.get_profile().text)

    return cnq_render_to_response('profile.html', request, {
        'puser': u,
        'profile_birthday': u.get_profile().birthday,
        'profile': u.get_profile(),
        'profile_text': profile_text,
        'body_top_message': 'The changes to your profile have been saved.',
    })
