from django.contrib.auth.models import User
from carnique.profile.models import UserProfile
from carnique.quotes.models import Quote

def test_cp(request):
    return {'huk': 'tilde'}

def get_carniqui(request):
    carniqui = [ ]

    for u in User.objects.all().order_by('username'):
        if not u.is_active:
            continue

        try:
            # This will raise an exception if there is no UserProfile
            # for this User at all.
            profile = u.get_profile()
            if profile.is_member:
                carniqui.append(u)
        except UserProfile.DoesNotExist:
            pass


    return {'carniqui': carniqui}

def get_blogs(request):
    result = get_carniqui(request)

    blogs = [ ]

    for c in result['carniqui']:
        p = c.get_profile()
        if p.blog_url and p.blog_name:
            blogs.append({
                'name': p.blog_name,
                'url': p.blog_url,
            })

    return {'blogs': blogs}

def get_latest_quote(request):
    num_quotes = Quote.objects.count()
    q = Quote.objects.order_by('id').all()[num_quotes - 1]

    return { 'latest_quote': q }

