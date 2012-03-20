# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from utils import response
from forms import ArticleForm, UserForm, UserProfileForm, CustomPasswordChangeForm
from picasa.models import PicasaAlbum
from frontend.models import Article
from frontend.utils import compile_article

from picasa.async import async_fetch_albums

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
        'page_type': 'photoalbum',
    })

@login_required
def list_photoalbums(request):
    return response(request, 'photoalbums.html', {
        'page_type': 'photoalbum',
    })

@login_required
def view_article(request, article_id=None):
    article=None
    if article_id:
        article = get_object_or_404(Article, id=article_id, user=request.user)
        form = ArticleForm(instance=article)
    else:
        form = ArticleForm()

    return response(request, 'edit_article.html', {
        'article': article,
        'article_id': article_id,
        'article_form': form,
        'page_type': 'article',
    })

@login_required
def save_article(request, article_id=None):
    article = None
    if article_id:
        article = get_object_or_404(Article, id=article_id, user=request.user)
        form = ArticleForm(request.POST, instance=article)

        if 'delete' in request.POST:
            article.delete()
            messages.add_message(request, messages.INFO, u'The article “%s” has been deleted.' % article.name)
            return redirect('management:index')

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

    return response(request, 'edit_article.html', {
        'article': article,
        'article_form': form,
        'article_id': article_id,
        'page_type': 'article',
    })

@login_required
def list_articles(request):
    return response(request, 'articles.html', {
        'page_type': 'article',
    })

@login_required
def preview_photoalbum(request, photoalbum_id):
    album = get_object_or_404(PicasaAlbum, id=photoalbum_id, user=request.user)

    return response(request, 'photoalbum_preview.html', {
        'photoalbum': album,
    })

@login_required
def user_settings(request):
    return response(request, 'settings.html', {
        'password_change_form': CustomPasswordChangeForm(request.user),
        'user_form': UserForm(instance=request.user),
        'user_profile_form': UserProfileForm(instance=request.user.profile),
        'google_token_management_url': settings.GOOGLE_TOKEN_MANAGEMENT_URL,
        'page_type': 'settings',
    })

@login_required
def change_password(request):
    password_change_form = CustomPasswordChangeForm(request.user, request.POST)
    if password_change_form.is_valid():
        password_change_form.save()
        messages.add_message(request, messages.SUCCESS, 'You password has been changed.')
        return redirect('management:settings')

    return response(request, 'settings.html', {
        'password_change_form': password_change_form,
        'user_form': UserForm(instance=request.user),
        'user_profile_form': UserProfileForm(instance=request.user.profile),
        'google_token_management_url': settings.GOOGLE_TOKEN_MANAGEMENT_URL,
        'page_type': 'settings',
    })

@login_required
def change_settings(request):
    user_form = UserForm(request.POST, instance=request.user)
    user_profile_form = UserProfileForm(request.POST, instance=request.user.profile)

    if user_form.is_valid() and user_profile_form.is_valid():
        user_form.save()
        user_profile_form.save()
        messages.add_message(request, messages.SUCCESS, 'Your settings have been changed.')
        return redirect('management:settings')

    return response(request, 'settings.html', {
        'password_change_form': CustomPasswordChangeForm(request.user),
        'user_form': user_form,
        'user_profile_form': user_profile_form,
        'google_token_management_url': settings.GOOGLE_TOKEN_MANAGEMENT_URL,
        'page_type': 'settings',
    })

@login_required
def update_albums(request):
    async_fetch_albums.delay()
    messages.add_message(request, messages.INFO, 'Your photoalbums have been scheduled to be imported soon.')
    return redirect('management:index')

@csrf_exempt
@login_required
def preview_article(request):
    article_text = request.POST['text']
    compiled_text = compile_article(request.user, article_text)

    return HttpResponse(compiled_text)
