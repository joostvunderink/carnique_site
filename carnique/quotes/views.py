from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import django.utils.timezone
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt

from carnique.quotes.models import Quote, QuoteVote
from carnique.main.views import cnq_render_to_response, convert_bb_to_html

from random import randint
import datetime

quote_vote_expiry_time = datetime.timedelta(1, 0)

def quote_view(request, quote_id):
    q = get_object_or_404(Quote, pk=quote_id)

    return cnq_render_to_response('quote.html', request, {
        'quote': q,
        'quote_text': convert_bb_to_html(q.text),
    })

def quote_view_random(request):
    num_quotes = Quote.objects.count()
    q = Quote.objects.all()[randint(0, num_quotes-1)]

    return cnq_render_to_response('quote.html', request, {
        'quote': q,
        'quote_text': convert_bb_to_html(q.text),
    })

def quote_list(request):
    quotes = Quote.objects.order_by('id').all()

    return cnq_render_to_response('quote_list.html', request, {
        'quote_list': quotes,
    })

def _get_page_of_quotes(quotes, page_number):
    quotes_per_page = 10

    num_quotes = len(quotes)
    num_pages = int(num_quotes / quotes_per_page)
    if num_quotes % quotes_per_page != 0:
        num_pages += 1

    if (page_number - 1) * quotes_per_page > num_quotes:
        raise Http404()

    begin = (page_number - 1) * quotes_per_page
    end   = page_number * quotes_per_page
    if end > num_quotes:
        end = num_quotes

    previous_page = page_number - 1
    if previous_page < 1:
        previous_page = 1

    next_page = page_number + 1
    if next_page > num_pages:
        next_page = num_pages

    return {
        'paged_quotes': quotes[begin:end],
        'next_page': next_page,
        'previous_page': previous_page,
        'num_pages': num_pages,
        'close_nav': _get_close_nav_pages(page_number, 1, num_pages),
    }

def _get_close_nav_pages(current_page, first_page, last_page):
    page_list = [
        current_page - 10,
        current_page - 2,
        current_page - 1,
        current_page,
        current_page + 1,
        current_page + 2,
        current_page + 10,
    ]

    while page_list[0] < first_page:
        page_list.pop(0)

    while page_list[-1] > last_page:
        page_list.pop(-1)

    return page_list

def quote_view_top_page(request, page_number=1):
    page_number = int(page_number)

    quotes = Quote.objects.order_by('-score', '-id').all()
    result = _get_page_of_quotes(quotes, page_number)

    return cnq_render_to_response('quote_page.html', request, {
        'quote_list': result['paged_quotes'],
        'num_pages': result['num_pages'],
        'page_list': range(1, result['num_pages'] + 1),
        'current_page': page_number,
        'first_page': 1,
        'last_page': result['num_pages'],
        'previous_page': result['previous_page'],
        'next_page': result['next_page'],
        'type': 'top',
        'close_nav': result['close_nav'],
    })

def quote_view_page(request, page_number=1):
    page_number = int(page_number)

    quotes = Quote.objects.order_by('-id').all()
    result = _get_page_of_quotes(quotes, page_number)

    return cnq_render_to_response('quote_page.html', request, {
        'quote_list': result['paged_quotes'],
        'num_pages': result['num_pages'],
        'page_list': range(1, result['num_pages'] + 1),
        'current_page': page_number,
        'first_page': 1,
        'last_page': result['num_pages'],
        'previous_page': result['previous_page'],
        'next_page': result['next_page'],
        'type': 'page',
        'close_nav': result['close_nav'],
    })

@login_required
def quote_add(request):
    # Nothing was POSTed? Just display the form.
    if not 'quote_title' in request.POST:
        return cnq_render_to_response('quote_add.html', request, {})

    # A quote was POSTed. Try to add it.
    error_message = ""

    if len(request.POST['quote_title']) == 0:
        error_message = "Please enter the quote's title."
    elif len(request.POST['quote_text']) == 0:
        error_message = "Please enter the quote's text."

    if len(error_message) > 0:
        return cnq_render_to_response('quote_add.html', request, {
            'body_top_error': error_message,
            'quote_text': request.POST['quote_text'],
            'quote_title': request.POST['quote_title'],
        })

    q = Quote()
    q.title = request.POST['quote_title']
    q.text = request.POST['quote_text']
    q.added_by = request.user
    q.save()

    # We should redirect to /quotes/<new_id>/ here, with possibly the
    # message "Quote added" at the top.
    return HttpResponseRedirect("/quotes/%d/" % q.id)

@csrf_exempt
def quote_vote(request):
    if 'quote_id' not in request.POST:
        return json_to_http({
            'success': False,
            'error': 'no quote id given',
        })

    quote_id = int(request.POST['quote_id'])
    direction = request.POST['direction']

    q = get_object_or_404(Quote, pk=quote_id)

    if _already_voted(q, request):
        return json_to_http({
            'success': False,
            'error': "you have already voted on this quote",
        })

    print "qv3 '%s'" % direction;
    if direction == 'up':
        _vote(q, request, 1)
    else:
        _vote(q, request, -1)

    data = {
        'success': True,
        'new_score': q.score,
        'quote_id': q.id,
    }

    return json_to_http(data)

def json_to_http(data):
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')

def _already_voted(quote, request):
    qvs = QuoteVote.objects.all().filter(quote=quote)
    now = django.utils.timezone.now()

    for qv in qvs:
        if now - qv.ts < quote_vote_expiry_time:
            return True

    return False

def _vote(quote, request, amount):
    quote.score += amount
    quote.save()

    qv = QuoteVote()
    qv.quote = quote
    qv.ts = datetime.datetime.now()
    qv.ip = request.META['REMOTE_ADDR']
    qv.save()

def quote_vote_up(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)

    if not _already_voted(quote, request):
        _vote(quote, request, 1)

    return cnq_render_to_response('quote.html', request, {
        'quote': quote,
        'quote_text': convert_bb_to_html(quote.text),
    })

def quote_vote_down(request, quote_id):
    quote = get_object_or_404(Quote, pk=quote_id)

    if not _already_voted(quote, request):
        _vote(quote, request, -1)

    return cnq_render_to_response('quote.html', request, {
        'quote': quote,
        'quote_text': convert_bb_to_html(quote.text),
    })


