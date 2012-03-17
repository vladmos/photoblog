from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

from models import Article
from utils import response

def index(request):
    return HttpResponse('index!')

def user_articles(request, username):
    user = get_object_or_404(User, username=username)

    return response(request, 'blog.html', {
        'user': user,
    })

def view_article(request, username, article_slug):
    user = get_object_or_404(User, username=username)
    article = get_object_or_404(Article, user=user, slug=article_slug)

    return response(request, 'article.html', {
        'user': user,
        'article': article,
    })
