from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from carnique.news.models import News
from carnique.main.views import cnq_render_to_response

def news_list(request):
    news = News.objects.order_by('-id').all()

    can_add_news = False
    if request.user.is_authenticated:
        if request.user.has_perm('main.add_news'):
            can_add_news = True

    return cnq_render_to_response('news_list.html', request, {
        'news_list': news,
        'can_add_news': can_add_news,
    })

@login_required
def news_add(request):
    if not 'news.add_news' in request.user.get_all_permissions():
        return cnq_render_to_response('error.html', request, {
            'error_message': "You are not allowed to add news items.",
        })

    # Nothing was POSTed? Just display the form.
    if not 'news_title' in request.POST:
        return cnq_render_to_response('news_add.html', request, { })

    # News was POSTed. Try to add it.
    error_message = ""

    if len(request.POST['news_title']) == 0:
        error_message = "Please enter the news title."
    elif len(request.POST['news_text']) == 0:
        error_message = "Please enter the news text."

    if len(error_message) > 0:
        return cnq_render_to_response('news_add.html', request, {
            'body_top_error': error_message,
            'news_text': request.POST['news_text'],
            'news_title': request.POST['news_title'],
        })

    n = News()
    n.title = request.POST['news_title']
    n.text = request.POST['news_text']
    n.added_by = request.user
    n.save()

    # We should redirect to /news/<new_id>/ here, with possibly the
    # message "Quote added" at the top.
    return HttpResponseRedirect("/news/")
