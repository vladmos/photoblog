from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import Http404

from models import Article
from utils import response

def _get_user(request):
    if request.owner:
        return request.owner
    raise Http404

def blog(request):
    try:
        user = _get_user(request)
    except Http404:
        return response(request, 'frontend.html')

    articles = user.articles.filter(is_published=True)
    years = set(a.event_end.year for a in articles)
    years = list(reversed(sorted(years)))

    return response(request, 'blog.html', {
        'user': user,
        'articles': articles,
        'years': years,
    })

def article(request, article_slug):
    user = _get_user(request)
    article = get_object_or_404(Article, user=user, slug=article_slug, is_published=True)
    articles = user.articles.filter(is_published=True)

    return response(request, 'article.html', {
        'user': user,
        'articles': articles,
        'article': article,
    })

def rss(request):
    user = _get_user(request)
    articles = user.articles.filter(is_published=True)[:20]

    return response(request, 'rss.xml', {
        'user': user,
        'articles': articles,
        'last_update': max(a.updated for a in articles) if articles else None,
    }, mimetype='text/xml')
