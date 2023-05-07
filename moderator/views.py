from django.shortcuts import render, redirect, get_object_or_404
from django.core.handlers.wsgi import WSGIRequest

from django.http import Http404

from django.contrib.auth import login, logout, hashers, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings


from django.core.mail import send_mail

from moderator.models import User,Moderator, Logins
from .decorator import moderator_only, super_moderator_only

from articles.models import (
    Article,
    ArticleColumn,
    Journal,
    Petition,
    Post,
)

from .forms import (
    PostForm,           # Post form
    JournalForm,        # Jurnal form
    ArticleColumnForm,  # Maqola rukni formi
    BasicArticelForm,   # Maqolani articlga o'tkazish formi
    CKEditorForm,       # CKEditor uchun sample form
    ModeratorUserForm,  # Moderator form
    ArticleFullForm,      # Articlni tahrirlash formi
    ArticleFullCreateForm, # Articlni yaratish formi
    TeamForm,               # Jamoa a'zosini formi
    ModeratorUpdateForm, # Moderator update
)

from pages.models import Team






# Dashboard
@login_required(login_url='login')
@moderator_only
def dashboard(request: WSGIRequest):
    data_not_viewed = Petition.objects.filter(is_viewed=False)

    data_sum_list = [
        len(Moderator.objects.all()),
        len(Article.objects.all()),
        len(Post.objects.all()),
        len(Journal.objects.all()),
        len(ArticleColumn.objects.all()),
        len(Petition.objects.all()),
        len(Team.objects.all())
    ]
    return render(request, 'moderator/index.html', {
        'data': data_not_viewed,
        'sums': data_sum_list,
    })




# Akkount viewslar
# ============================================================
# Profile View
@login_required(login_url='login')
@moderator_only
def profile_view(request: WSGIRequest):
    object = get_object_or_404(Moderator, user_id=request.user.id)
    data_filter = Petition.objects.filter(confirmed_id=object.pk)
    data_len = len(data_filter)
    return render(request, 'moderator/profile_view.html', {
        'object': object,
        'len_data': data_len,
        'data_filter': data_filter,
    })

# Profile update
@login_required(login_url='login')
@moderator_only
def profile_update(request: WSGIRequest):
    moderator = get_object_or_404(Moderator, user_id=request.user.pk)
    if request.method == 'POST':
        if request.POST.get('data_name') == 'other':
            first_name = request.POST.get('first_name', None)
            last_name = request.POST.get('last_name', None)
            email = request.POST.get('email', None)
            username = request.POST.get('username', None)
            dark_mode = request.POST.get('dark_mode', None)
            dark_mode = [True if dark_mode == 'on' else False][0]   
            description = request.POST.get('description', None)
            if not (first_name and last_name and email and username):
                messages.error(request, message='Barcha bandlarni to\'ldiring !', extra_tags='danger')
                return redirect('profile_update')
            
            db_user = True
            try:
                db_user = User.objects.get(username=username)
                if not (request.user.username ==  username):
                    db_user = False
            except:
                db_user = True

            if not db_user:
                messages.error(request, 'Ushbu taxallus avvalroq band qilingan. \n Iltimos boshqa taxallus kiriting.', extra_tags='danger')
            else:
                image = request.FILES.get('image', None)
                user = User.objects.get(pk=request.user.pk)
                user.first_name = first_name
                user.last_name = last_name
                user.username = username
                user.email = email
                user.dark_mode = dark_mode
                if image is not None:
                    user.image = image
                user.save()
                login(request=request, user=user)
                if description:
                    moderator.description = description
                    moderator.save()
                messages.success(request, "Sozlamalar saqlandi!")
                return redirect('profile_view')
        
        elif request.POST.get('data_name') == 'password':
            old_password = request.POST.get('old_password', None)
            new_password = request.POST.get('new_password', None)
            new_password_again = request.POST.get('new_password_again', None)

            if not (old_password and new_password and new_password_again) or not (new_password == new_password_again):
                messages.error(request, "Parolni tasdiqlashda xatolikka yo'l qo'ydingiz !", extra_tags='danger')
                return redirect('profile_update')
            
            user = User.objects.get(pk=request.user.pk)
            if not hashers.check_password(old_password ,user.password):
                messages.error(request, "Avvalgi parolni xato kiritdingiz !", extra_tags='danger')
                return redirect('profile_update')
            
            user.password = hashers.make_password(new_password)
            user.save()
            login(user=user, request=request)
            messages.success(request, "Parol muvaffaqiyatli o'zgartirildi !")
            return redirect('profile_view')
    return render(request, 'moderator/profile_update.html', {})




# Maqolalar viewslari
# ====================================================
# Barcha maqolalar
@login_required(login_url='login')
@moderator_only
def all_articles(request: WSGIRequest):
    data = Article.objects.all()
    return render(request, 'moderator/all_articles.html', {
        'data': data,
    })


@login_required(login_url='login')
@moderator_only
def article_read(request: WSGIRequest, pk):
    object = get_object_or_404(Article, pk=pk)
    return render(request, 'moderator/article_read.html', {
        'object': object,
    })


@login_required(login_url='login')
@moderator_only
def article_create(request: WSGIRequest):
    form = ArticleFullCreateForm()
    moderator = get_object_or_404(Moderator, user_id=request.user.id)
    if request.method == 'POST':
        form = ArticleFullCreateForm(request.POST)
        if form.is_valid:
            object = Article()
            object.journal = Journal.objects.get(pk=int(form['journal'].value()))
            object.column = ArticleColumn.objects.get(pk=int(form['column'].value()))
            object.title = form['title'].value()
            try:
                file = request.FILES['file']
            except:
                file = False
            object.description = form['description'].value()
            object.first_name = form['first_name'].value()
            object.last_name = form['last_name'].value()
            object.file = file
            object.confirmed = moderator

            if file:
                object.save()
                messages.success(request, 'Maqola muvaffaqiyatli qo\'shildi')
            else:
                messages.error(request, 'Xatolik yuz berdi', extra_tags='danger')
            return redirect('all_article')

    return render(request, 'moderator/article_create.html', {
        'form': form,
    })


@login_required(login_url='login')
@moderator_only
def article_archive(request: WSGIRequest, pk):
    object = get_object_or_404(Article, pk=pk)
    object.is_active = [False if object.is_active == True else True][0]
    object.save()
    return redirect('article_read', pk=object.pk)



@login_required(login_url='login')
@moderator_only
def article_delete(request: WSGIRequest, pk):
    object = get_object_or_404(Article, pk=pk)
    if request.method == 'POST':
        object.delete()
    return redirect('all_article')


@login_required(login_url='login')
@moderator_only
def article_change(request: WSGIRequest, pk):
    object = get_object_or_404(Article, pk=pk)
    form = ArticleFullForm(instance=object)

    if request.method == 'POST':
        form = ArticleFullForm(request.POST, instance=object)
        try:
            if form.is_valid:
                form.save()
                messages.success(request, 'Maqola muvaffaqiyatli o\'zgartirildi')
                return redirect('article_read', pk=object.pk)
            else:
                messages.error(request, 'Malumotlarni to\'dirishda xatolik yuz berdi.', extra_tags="danger") 
        except:
            messages.error(request, 'Nomalum xatolik yuz berdi. Joiz bo\'lsa sayt dasturchilariga xabar bering.', extra_tags='danger')
    return render(request, 'moderator/article_change.html', {
        'object': object,
        'form': form,
    })




# Maqolalar tugadi
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$4





# Postlar uchun viewslar 
# =====================================
# Barcha postlar
@login_required(login_url='login')
@moderator_only
def all_posts(request: WSGIRequest):
    data = Post.objects.all()
    return render(request, 'moderator/all_posts.html', {
        'data': data,
    })

# Yangi post qo'shish
@login_required(login_url='login')
@moderator_only
def post_create(request: WSGIRequest):
    form = PostForm()
    if request.method == 'POST':
        try:
            moderator = Moderator.objects.get(user_id=request.user.id)
        except:
            return redirect('login')
        data_form = PostForm(request.POST)
        
        try:
            if data_form.is_valid:
                title = data_form["title"].value()
                body = data_form["body"].value()
                image = request.FILES.get('image', None)

                if title and body and image:
                    object = Post()
                    object.author = moderator
                    object.title = title
                    object.body = body
                    object.image = image
                    object.save()
                messages.success(request, ''' Post saqlandi ''')
                return redirect('all_posts')
            else:
                messages.error(request, 'Barcha bandlar to\'ldirilmadi.', extra_tags='danger')
        except:
            messages.error(request, '''No\'malum xatolik yuz berdi. \n
                    Joiz bo\'lsa ishlab chiqaruvchilar bilan aloqaga chiqing''', extra_tags='danger')
    return render(request, 'moderator/post_create.html', {
        'form': form,
    })

# Mavjud postni yangilash
@login_required(login_url='login')
@moderator_only
def post_update(request: WSGIRequest, pk):
    object = get_object_or_404(Post, pk=pk)
    form = PostForm(instance=object)

    if request.method == 'POST':
        data_form = PostForm(data=request.POST, instance=object)
        try:
            if data_form.is_valid:
                object = data_form.save(commit=True)
                image = request.FILES.get('image', None)
                if image:
                    object.image = image
                    object.save()
                messages.success(request, 'Sozlamalar saqlandi !')
                return redirect('all_posts')   
            else:
                messages.error(request, 'Barcha bandlarni to\'ldiring.', extra_tags='danger')
        except:
            messages.error(request, 'Nomalum xatolik yuz berdi', extra_tags='danger')

    return render(request, 'moderator/post_update.html', {
        'form': form,
        'object': object,
    })

# Potni o'chirish
@login_required(login_url='login')
@moderator_only
def post_delete(request: WSGIRequest, pk):
    object = get_object_or_404(Post, pk=pk)
    try:
        object.delete()
        messages.success(request, 'Post muvaffaqiyatli o\'chirildi')
    except:
        messages.error(request, 'Postni o\'chirib bo\'lmadi. Ishlab chiqaruvchilarga xabar bering.', extra_tags="danger")
    return redirect('all_posts')

# Postlar bo'limi tugadi
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$44




# Jurnallar viewslari
# =========================================
# Barcha jurnallar
@login_required(login_url='login')
@moderator_only
def journal_all(request: WSGIRequest):
    data = Journal.objects.all()
    return render(request, 'moderator/journal_all.html', {
        'data': data,
    })

# Yangi jurnal qo'shish
@login_required(login_url='login')
@moderator_only
def journal_create(request: WSGIRequest):
    form = JournalForm()
    if request.method == 'POST':
        form = JournalForm(request.POST)
        try:
            if form.is_valid:
                form.save(commit=True)
                messages.success(request, 'Jurnal yaratildi. {obj.name}')
                return redirect('journal_all')
            else:
                messages.error(request, 'Jurnal yaratilmadi.', extra_tags='danger')
        except:
            messages.error(request, 'Xatolik yuz berdi. Ishlab chiqaruvchilarga xabar bering', extra_tags="danger")
    return render(request, 'moderator/journal_create.html', {
        'form': form,
    })

# Mavjud jurnalni yangilash
@login_required(login_url='login')
@moderator_only
def journal_update(request: WSGIRequest, pk):
    object = get_object_or_404(Journal, pk=pk)
    form = JournalForm(instance=object)

    if request.method == 'POST':
        form = JournalForm(data=request.POST, instance=object)
        if form.is_valid:
            form.save()
            messages.success(request, 'Sozlamalar saqlandi')
            return redirect('journal_all')

    return render(request, 'moderator/journal_update.html', {
        'form': form,
        'object': object,
    })

# Jurnalni o'chirish
@login_required(login_url='login')
@moderator_only
def journal_delete(request: WSGIRequest, pk):
    object = get_object_or_404(Journal, pk=pk)
    try:
        messages.success('Jurnal o\'chirildi {object.name}')
        object.delete()
    except:
        messages.error(request, 'Jurnalni o\'chirib bo\'lmadi. Xatolik haqida ishlab chiqaruvchiga murojaat qiling.', extra_tags="danger")
    return redirect('journal_all')

# Jurnallar bo'limi tugadi
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$4




# Maqola ruknlari
# ===============================================
# List view
@login_required(login_url='login')
@moderator_only
def article_col_all(request: WSGIRequest):
    data = ArticleColumn.objects.all()
    return render(request, 'moderator/article_col_all.html', {
        'data': data,
    })

# Rukn yaratish
@login_required(login_url='login')
@moderator_only
def article_col_create(request: WSGIRequest):
    form = ArticleColumnForm()

    if request.method == 'POST':
        form = ArticleColumnForm(data=request.POST)
        if form.is_valid:
            form.save()
            messages.success(request, 'Maqola rukni yaratildi.')
            return redirect('article_col_all')

    return render(request, 'moderator/article_col_create.html', {
        'form': form,
    })

# Ruknni yangilash
@login_required(login_url='login')
@moderator_only
def article_col_update(request: WSGIRequest, pk):
    object = get_object_or_404(ArticleColumn, pk=pk)
    form = ArticleColumnForm(instance=object)
    if request.method == 'POST':
        form = ArticleColumnForm(instance=object, data=request.POST)
        if form.is_valid:
            form.save()
            messages.success(request, 'Sozlamalar saqlandi.')
            return redirect('article_col_all')
    return render(request, 'moderator/article_col_update.html', {
        'object': object,   
        'form': form, 
    })


# Maqola ruknni o'chirish
@login_required(login_url='login')
@moderator_only
def article_col_delete(request: WSGIRequest, pk):
    if pk == 1:
        return redirect('article_col_all')
    object = get_object_or_404(ArticleColumn, pk=pk)
    object.delete()
    messages.success(request, 'Maqola rukni o\'chirildi.')
    return redirect('article_col_all')

# Ruknlar qismi tugadi
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$4




# Arizalar qismlari
# =========================================================
# Barcha arizalar
@login_required(login_url='login')
@moderator_only
def petition_all(request: WSGIRequest):
    data = Petition.objects.all().order_by('-pk')
    return render(request, 'moderator/petition_all.html', {
        'data': data,
    })



@login_required(login_url='login')
@moderator_only
def petition_detail(request: WSGIRequest, pk):
    object = get_object_or_404(Petition, pk=pk)
    
    return render(request, 'moderator/petition_detail.html', {
        'object': object,
    })


@login_required(login_url='login')
@moderator_only
def petition_access(request: WSGIRequest, pk):
    moderator = get_object_or_404(Moderator, user_id=request.user.id)
    object = get_object_or_404(Petition, pk=pk)
    form = BasicArticelForm()

    if request.method == 'POST':
        form = BasicArticelForm(request.POST)
        if form.is_valid:
            article = form.save(commit=False)
            article.confirmed = moderator
            article.title = object.title
            article.file = object.file
            article.description = object.description
            article.first_name = object.first_name
            article.last_name = object.last_name
            article.save()

            object.is_viewed = True
            object.status = Petition.STATUS[1][0]
            try:
                object.save()
                messages.success(request, ''' Ariza maqullandi va maqolalar safiga qo'shildi. ''')
                html_message = f'''
                    <p>Assalomu alaykum Xurmatli <strong>{object.last_name} {object.first_name}.</strong></p>
                    <p>SamNurAsia saytiga maqola joylash bo&#39;yicha berilgan arizangiz qabul qilindi va tasdiqlandi. Siz bilan hamkorlik qilganimizdan xursandmiz.&nbsp;</p>
                    <p>Arizangiz bo&#39;yicha e&#39;lon qilingan maqolani ushbu havolada topishingiz mumkin <u><em><a href="https://samnurasia.uz/article/{5}" target="_blank">havola</a>.</em></u>&nbsp;</p>
                    <p>Xurmat bilan <em>SamNurAsia</em> hamjamiyati.</p>
                    <p>&nbsp;</p>
                    <p>Arizangizni {moderator.user.last_name} {moderator.user.first_name} ko&#39;rib chiqdi.</p>'''
                try:
                    send_mail(
                        subject='Arizangiz Tasdiqlandi.',
                        message='',
                        from_email=settings.EMAIL_HOST_USER,
                        recipient_list=[object.email],
                        fail_silently=False,
                        html_message=html_message,
                    )
                    messages.success(request, 'Maqola muallifiga xabar yuborildi.')
                except:
                    messages.error(request, 'Maqola muallifiga xabar yuborishda xatolik yuz berdi.', extra_tags='danger')
                return redirect('all_article')
            except:
                messages.error(request, 'Nomalum xatolik yuz berdi. Iltimos ishlab chiqaruvchilarga xabar bering.', extra_tags='danger')
        else:
            messages.error(request, 'Iltimos barcha bandlarni to\'ldiring', extra_tags="danger")
    return render(request, 'moderator/petition_accesss.html', {
        'object': object,
        'form': form,
    })


@login_required(login_url='login')
@moderator_only
def petition_not_access(request: WSGIRequest, pk):
    moderator = get_object_or_404(Moderator, user_id=request.user.id)
    object = get_object_or_404(Petition, pk=pk)
    object.is_viewed = True
    object.confirmed = moderator
    object.status = Petition.STATUS[3][0]
    object.save()

    messages.success(request, 'Ariza rad etildi.')

    html_message = f'''
        <p><strong><em>Hurmatli {object.last_name} {object.first_name}</em></strong></p>
        <p>Maqola joylash bo&#39;yicha yuborgan erizangiz rad etildi. Savol, muammo va 
        takliflar bo&#39;lsa ushbu akkuntga xabar yuborishingiz mumkin.&nbsp;</p>
        <p>Maqolani: <strong>{moderator.user.last_name} {moderator.user.first_name}</strong> tekshirdi</p>
    '''

    try:
        send_mail(
            subject='Maqola joylash bo\'yicha yuborilgan arizangiz rad etildi. ',
            message='',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[object.email],
            fail_silently=True,
            html_message=html_message,
        )
        messages.success(request, 'Maqola muallifga xabar yuborildi')
    except:
        messages.error(request, 'Maqola muallifiga xabar yuborishda xatolik yuz berdi. Iltimos ishlab chiqaruvchilarga xabar bering!', extra_tags="danger")
    return redirect('petition_all')


@login_required(login_url='login')
@moderator_only
def petition_warning(request: WSGIRequest, pk):
    moderator = get_object_or_404(Moderator, user_id=request.user.id)
    object = get_object_or_404(Petition, pk=pk)
    form = CKEditorForm()

    if request.method == 'POST':
        form = CKEditorForm(request.POST)
        if form.is_valid:
            html_message = form['body'].value()
            html_message += f'<p>&nbsp;</p><p>Arizangizni <strong><em>{moderator.user.last_name} {moderator.user.first_name}</em></strong> tekshirdi.</p>'

            try:
                send_mail(
                    'Maqola joylash bo\'yicha bergan arizangizda kamchiliklar aniqlandi',
                    'Iltimos arizangizni qayta ko\'rib chiqing',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[object.email],
                    fail_silently=True,
                    html_message=html_message,
                )
                messages.success(request, 'Maqola muallifiga xabar yuborildi.')
            except:
                messages.error(request, 'Maqola muallifiga xabar yuborishda xatolik yuz berdi.', extra_tags='danger')
            object.is_viewed = True
            object.confirmed = moderator
            object.status = Petition.STATUS[2][0]
            object.save()
            messages.success(request, 'Ariza qayta ko\'rib chiqish uchun rad etildi .')
            return redirect('petition_all')

    return render(request, 'moderator/petition_warning.html', {
        'form': form,
    })


@login_required(login_url='login')
@moderator_only
def petition_delete(request: WSGIRequest, pk):
    object = get_object_or_404(Petition, pk=pk)
    object.delete()
    return redirect("petition_all")


# moderators 
# =========================================
# listview

@login_required(login_url='login')
@moderator_only
def moderator_all(request: WSGIRequest):
    data = Moderator.objects.all()
    moderator = get_object_or_404(Moderator, user_id=request.user.id)
    return render(request, 'moderator/moderator_all.html', {
        'data': data,
        'object': moderator
    })


@login_required(login_url='login')
@moderator_only
def moderator_detail(request: WSGIRequest, pk):
    object = get_object_or_404(Moderator, pk=pk)
    data_filter = Petition.objects.filter(confirmed_id=object.pk)
    len_data = len(data_filter)
    return render(request, 'moderator/moderator_detail.html', {
        'object': object,
        'data_filter': data_filter,
        'len_data': len_data,
        'moderator': Moderator.objects.get(user_id=request.user.id)
    })

@login_required(login_url='login')
@moderator_only
@super_moderator_only
def moderator_add(request: WSGIRequest):
    moderator = get_object_or_404(Moderator, user_id=request.user.pk)
    if moderator.is_created == False:
        raise Http404()
    form = ModeratorUserForm()

    if request.method == 'POST':
        form = ModeratorUserForm(request.POST)
        if form.is_valid:
            try:
                user = form.save(commit=False)
                user.dark_mode = False
                user.password = hashers.make_password(form['password'].value())
                user.save()
                new_moderator = Moderator()
                new_moderator.user = user
                new_moderator.role = request.POST.get('role', '')
                new_moderator.is_created = False
                new_moderator.save()
                messages.success(request, 'Yangi admin qo\'shildi. ')
                return redirect('moderator_all')
            except:
                messages.error(request, 'Iltimos boshqa username kiriting !', extra_tags='danger')

    return render(request, 'moderator/moderator_add.html', {
        'form': form,
    })


@login_required(login_url='login')
@moderator_only
@super_moderator_only
def moderator_delete(request: WSGIRequest, pk):
    object = get_object_or_404(Moderator, pk=pk)
    if object.user.pk == request.user.pk:
        return redirect('profile_update')    
    object.delete()
    return redirect("moderator_all")



@login_required(login_url='login')
@moderator_only
@super_moderator_only
def moderator_update(request: WSGIRequest, pk):
    object = get_object_or_404(Moderator, pk=pk)
    if object.user.pk == request.user.pk:
        return redirect('profile_update')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        email = request.POST.get('email', None)
        role = request.POST.get('role', None)
        active = request.POST.get('active', None)
        active = [True if active == 'on' else False][0]
        
        if first_name and last_name and email and role:
            object.user.first_name = first_name
            object.user.last_name = last_name
            object.user.email = email
            object.user.is_active = active
            print(object.user.is_active)
            object.user.save()
            object.role = role
            object.save()
            messages.success(request, "Sozlamalar saqlandi")
            return redirect('moderator_all')


    return render(request, 'moderator/moderator_update.html', {
        'object': object,
    })









# Jamoa
# ==================================================
# Barcha jamoadagilar
@login_required(login_url='login')
@moderator_only
def team_all(request: WSGIRequest):
    return render(request, 'moderator/team_all.html', {
        'data': Team.objects.all()
    })


@login_required(login_url='login')
@moderator_only
def team_create(request: WSGIRequest):
    form = TeamForm()
    if request.method == 'POST':
        form = TeamForm(data=request.POST)
        if form.is_valid:
            try:
                first_name = form["first_name"].value()
                last_name = form["last_name"].value()
                role = form["role"].value()
                description = form["description"].value()
                image = request.FILES.get('image', None)

                if first_name and last_name and role and description and image:
                    object = Team()
                    object.first_name = first_name
                    object.last_name = last_name
                    object.role = role
                    object.image = image
                    object.description = description
                    object.save()
                    messages.success(request, "Yangi jamoa a'zosi qo'shildi")
                    return redirect('team_all')
                else:
                    messages.error(request, "Formani to'ldirishda xatolik", extra_tags='danger')
            except:
                messages.error(request, "Nomalum xatolik yuz berdi", extra_tags="danger")
        else:
            messages.error(request, "Formani to'ldirishda xatolik yuz berdi", extra_tags='danger')
            return redirect("team_create")
    return render(request, 'moderator/team_form.html', {
        'title': "Yangi jamoa a'zosini kiritish",
        'form': form,
    })



@login_required(login_url='login')
@moderator_only
def team_update(request: WSGIRequest, pk):
    _team = get_object_or_404(Team, pk=pk)
    form = TeamForm(instance=_team)

    if request.method == 'POST':
        form = TeamForm(instance=_team, data=request.POST)
        if form.is_valid:
            try:
                form.save()
                messages.success(request, "Sozlamalar saqlandi")
                return redirect("team_all")
            except:
                messages.error(request, "Nomalum xatolik yuz berdi", extra_tags="danger")
        else:
            messages.error(request, "Formani to'ldirishda xatolik yuz berdi", extra_tags="danger")
            return redirect("team_update", pk=pk)

    return render(request, 'moderator/team_form.html', {
        'title': f'Jamoa a\'zosi {_team}',
        'form': form,
        'object': _team,
    })



@login_required(login_url='login')
@moderator_only
def team_delete(request: WSGIRequest, pk):
    object = get_object_or_404(Team, pk=pk)
    object.delete()
    messages.success(request, "Jamoa a'zosi olib tashlandi")
    return redirect("team_all")



















































































def login_view(request: WSGIRequest):
    error_msg = None
    next_page = request.GET.get('next', None)
    if request.method == 'POST':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        if username and password:
            check = None
            _user = None
            try:
                _user = User.objects.get(username=username)
                check = True
            except:
                check = False
            user = authenticate(request=request, username=username, password=password)
            if user is not None:
                login(request=request, user=user)
                Logins.objects.create(user = user, status=Logins.STATUS[0][0])
                if next_page:
                    return redirect(next_page)
                return redirect('dashboard')
            else:
                if check:
                    Logins.objects.create(user=_user, status=Logins.STATUS[1][0])
                error_msg = ''' Login yoki parol xato '''
        else:
            error_msg = ''' Barcha bandlar to'ldirilishi kerak ! '''

    return render(request, 'moderator/login.html', {
        'error_msg': error_msg,
    })


def logout_view(request):
    logout(request)
    return redirect('login')