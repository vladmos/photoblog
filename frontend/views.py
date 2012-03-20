from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from models import Article
from utils import response

def index(request):
    return response(request, 'frontend.html')

def blog(request, username):
    user = get_object_or_404(User, username=username)
    articles = user.articles.filter(is_published=True)
    years = str(a.event_end.year for a in articles)
    years = list(reversed(sorted(years)))

    return response(request, 'blog.html', {
        'user': user,
        'articles': articles,
        'years': years,
    })

def view_article(request, username, article_slug):
    user = get_object_or_404(User, username=username)
    article = get_object_or_404(Article, user=user, slug=article_slug, is_published=True)
    articles = user.articles.filter(is_published=True)

    return response(request, 'article.html', {
        'user': user,
        'articles': articles,
        'article': article,
    })

def rss(request, username):
    user = get_object_or_404(User, username=username)
    articles = user.articles.filter(is_published=True)[:20]

    return response(request, 'rss.xml', {
        'user': user,
        'articles': articles,
        'last_update': max(a.updated for a in articles) if articles else None,
    }, mimetype='text/xml')
