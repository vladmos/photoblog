from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

from utils import response
from forms import ArticleForm
from picasa.models import PicasaAlbum
from frontend.models import Article

@login_required
def index(request):
    return response(request, 'index.html', {
        'google_token_management_url': settings.GOOGLE_TOKEN_MANAGEMENT_URL,
    })

@login_required
def view_photoalbum(request, photoalbum_id):
    album = get_object_or_404(PicasaAlbum, id=photoalbum_id, user=request.user)

    return response(request, 'photoalbum.html', {
        'photoalbum': album,
    })

@login_required
def list_photoalbums(request):
    return response(request, 'photoalbums.html')

@login_required
def view_article(request, article_id=None):
    article=None
    if article_id:
        article = get_object_or_404(Article, id=article_id, user=request.user)
        form = ArticleForm(instance=article)
    else:
        form = ArticleForm()

    return response(request, 'article.html', {
        'article': article,
        'article_id': article_id,
        'article_form': form,
    })

@login_required
def save_article(request, article_id=None):
    article = None
    if article_id:
        article = get_object_or_404(Article, id=article_id, user=request.user)
        form = ArticleForm(request.POST, instance=article)
    else:
        form = ArticleForm(request.POST)

    if form.is_valid():
        if article_id:
            form.save()
        else:
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            article_id = article.id

        messages.add_message(request, messages.SUCCESS, 'The article is saved.')
        return redirect('management:article', article_id=article_id)

    return response(request, 'article.html', {
        'article': article,
        'article_form': form,
        'article_id': article_id,
    })

@login_required
def list_articles(request):
    return response(request, 'articles.html')

@login_required
def preview_photoalbum(request, photoalbum_id):
    album = get_object_or_404(PicasaAlbum, id=photoalbum_id, user=request.user)

    return response(request, 'photoalbum_preview.html', {
        'photoalbum': album,
    })
