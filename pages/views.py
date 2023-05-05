from django.shortcuts import render, redirect, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest

from pages.models import (
    Eslatma,
    Icon,
    IjtimoiyTarmoqlar,
    Manzili,
    MaqolaJoylash,
    Narxlar,
    Team,
)

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
    })



# DONE
def team_views(request: WSGIRequest):
    return render(request, 'pages/team.html', {
        'data': Team.objects.all()
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
        'object_list': Post.objects.all()
    })



def arxiv(request: WSGIRequest):
    journals = Journal.objects.all()
    cols = ArticleColumn.objects.all()
    return render(request, 'pages/arxiv.html', {
        'journals': journals,
        'cols': cols,
    })



def detail_journal(request: WSGIRequest, pk):
    journal = get_object_or_404(Journal, pk=pk)
    data = Article.objects.filter(journal_id=journal.pk)
    return render(request, 'pages/filter.html', {
        'data': data,
    })


def detail_col(request: WSGIRequest, pk):
    col = get_object_or_404(ArticleColumn, pk=pk)
    data = Article.objects.filter(column_id=col.pk)
    return render(request, 'pages/filter.html', {
        'data': data,
    })