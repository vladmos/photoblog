from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from models import Article
from utils import response

def index(request):
    return HttpResponse('index!')

def blog(request, username):
    user = get_object_or_404(User, username=username)
    articles = user.articles.filter(is_published=True)

    return response(request, 'blog.html', {
        'user': user,
        'articles': articles,
    })

def view_article(request, username, article_slug):
    user = get_object_or_404(User, username=username)
    article = get_object_or_404(Article, user=user, slug=article_slug, is_published=True)

    return response(request, 'article.html', {
        'user': user,
        'article': article,
    })
