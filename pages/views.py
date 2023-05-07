from django.shortcuts import render, redirect, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse

from pages.models import (
    Eslatma,
    Icon,
    IjtimoiyTarmoqlar,
    Manzili,
    MaqolaJoylash,
    Narxlar,
    Team,
)

from moderator.models import Moderator

from articles.models import Post

from django.core.mail import send_mail
from django.conf import settings
from articles.models import Petition, ArticleColumn, Journal, Article
from moderator.models import Moderator


def index(request: WSGIRequest):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        email = request.POST.get('email', None)
        title = request.POST.get('title', None)
        message = request.POST.get('message', None)

        file = None
        try:
            file = request.FILES['file']
        except:
            pass
        if first_name and last_name and email and \
            message and title and file:
            object = Petition.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                description=message,
                file=file,
                title=title,
            )
            object.is_viewed = False
            object.status = Petition.STATUS[0][0]
            object.save()
            HTML_MESSAGE = f'''
            <div style="background:#eeeeee; border:1px solid #cccccc; padding:5px 10px">Hurmatli {last_name} {first_name}</div>
            <p>Maqola joylash bo&#39;yicha yuborgan arizangiz qabul qilindi. Tez fursatlarda arizangizni to&#39;liq ko&#39;rib chiqamiz. Hurmat bilan Samnurasia jamoasi.&nbsp;</p>
            '''
            send_mail(
                subject='Arizangiz qabul qilindi.',
                message='',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=False,
                html_message=HTML_MESSAGE,
            )   
            request.method = 'GET'
            request.POST = {}
            request.GET = {}
            return index(request=request)


    return render(request, 'pages/index.html', {
        'manzil': Manzili.object(),
        'about': Eslatma.object(),
        'article': MaqolaJoylash.object(),
        'price': Narxlar.object(),
        'icon': Icon.object(),
        'data': Team.objects.all()[:4]
    })



# DONE
def team_views(request: WSGIRequest):
    return render(request, 'pages/team.html', {
        'data': Team.objects.all(),
        'icon': Icon.object(),
    })


# 
from random import choice
def news(request: WSGIRequest, *args, **kwargs):
    pk = kwargs.get('pk', False)
    if pk:
        random_obj = get_object_or_404(Post, pk=pk)
    else:
        pks = Post.objects.values_list('pk', flat=True)
        random_pk = choice(pks)
        random_obj = Post.objects.get(pk=random_pk)
    return render(request, 'pages/news.html', {
        'object': random_obj,
        'object_list': Post.objects.all(),
        'icon': Icon.object(),
    })



def arxiv(request: WSGIRequest):
    journals = Journal.objects.all()
    cols = ArticleColumn.objects.all()
    return render(request, 'pages/arxiv.html', {
        'journals': journals,
        'cols': cols,
        'icon': Icon.object(),
    })



def detail_journal(request: WSGIRequest, pk):
    journal = get_object_or_404(Journal, pk=pk)
    data = Article.objects.filter(journal_id=journal.pk, is_active=True)
    return render(request, 'pages/filter.html', {
        'data': data,
        'icon': Icon.object(),
    })


def detail_col(request: WSGIRequest, pk):
    col = get_object_or_404(ArticleColumn, pk=pk)
    data = Article.objects.filter(column_id=col.pk, is_active=True)
    return render(request, 'pages/filter.html', {
        'data': data,
        'icon': Icon.object(),
    })



def page_not_found(request: WSGIRequest, exception, *args, **kwarg):
    md = Moderator.get_moderator_or_None(request)
    url = request.get_full_path().split('/')[1]
    if md and url == 'moderator':
        url_name = 'dashboard'
    else:
        url_name = 'index'
    return render(request, 'error/404.html', {
        'icon': Icon.object(),
        'url_name': url_name,
    }, status=404)

def bad_request(*args, **kwargs):
    return HttpResponse('Bad Request', status=500)