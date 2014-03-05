from django.shortcuts import render_to_response
from django.utils.html import escape
from django.template import RequestContext

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from carnique.profile.models import UserProfile
from carnique.utils import get_square_color, get_square_html

import re

def square_test(request):
    s = ""

    for i in range(150):
        c = get_square_color(i * 6 * 3600)
        s += "<tr><td>"
        s += get_square_html(c, 8)
        s += "</td><td>%2.2f days, color %s</td></tr>" % (float(i) / 4, c)

    return cnq_render_to_response('square_test.html', request, {
        'blokjes': s,
    })

def todo(request):
    return cnq_render_to_response('todo.html', request, {
        'is_done': [
            'inloggen',
            'uitloggen',
            'profiel bekijken',
            'eigen profiel wijzigen',
            'news bekijken',
            'news toevoegen (mits admin)',
            'oude quotes importeren',
            'quote toevoegen',
            'quote bekijken',
            'quotes max N per pagina weergeven',
            'carniqui op login-pagina',
            'wachtwoord wijzigen',
            'random quote bekijken',
        ],
        'todo': [
            'looks verbeteren',
            'carnimsg werkend krijgen',
            'add new user (plus profile) by admins',
            'voting op quotes',
            'password-velden gebruiken bij password edit',
            'birthday leeglaten geeft error',
            'maak usernames case insensitive bij inloggen',
            'sommige profielen nog omzetten naar bb-code',
            '... nog meer?',
        ],
    })

@login_required
def password_edit(request):
    u = request.user

    if not 'new_password' in request.POST:
        return cnq_render_to_response('password_edit.html', request, {
        })

    np  = request.POST['new_password']
    np2 = request.POST['new_password2']

    if (np or np2) and (np != np2):
        return cnq_render_to_response('password_edit.html', request, {
            'body_top_error': 'The two password fields must contain the same password.',
        })

    u.set_password(np)
    u.save()

    return cnq_render_to_response('index.html', request, {
        'body_top_message': 'Your password has been changed.',
    })

def cnq_render_to_response(page, request, args):
    return render_to_response(page, args, context_instance=RequestContext(request))

def get_carnique_user(username):
    u = None

    try:
        u = User.objects.get(username=username)
    except User.DoesNotExist:
        return None

    if not u.is_active:
        return None

    try:
        # This will raise an exception if there is no UserProfile
        # for this User at all.
        profile = u.get_profile()
        if profile.is_member:
            return u
    except UserProfile.DoesNotExist:
        pass

    return None

def convert_bb_to_html(text):
    """Converts a piece of text with bb-tags (like [b] and [img]) to
    html. Any 'real' HTML tags that were present in the original text
    are html-escaped."""

    # First escape the text to get rid of all HTML tags.
    text = escape(text)

    # Now we can safely replace the bb-tags and be sure that those will be
    # the only HTML tags in the text.
    replacements = [
        ('\[b\](.+?)\[/b\]',  '<b>\\1</b>'),
        ('\[i\](.+?)\[/i\]',  '<i>\\1</i>'),
        ('\[ul\](.+?)\[/ul\]',  '<ul>\\1<//ul>'),
        ('\[li\](.+?)\[/li\]',  '<li>\\1<//i>'),
        ('\[img\](.+?)\[/img\]', '<img src="\\1" />'),
        ('\[url\](.+?)\[/url\]', '<a href="\\1">\\1</a>'),
        ('\[url=(.+?)\](.+?)\[/url\]', '<a href="\\1">\\2</a>'),
        ("\n", '<br />'),
    ]

    for r in replacements:
        p = re.compile(r[0])
        text = p.sub(r[1], text)

    return text

