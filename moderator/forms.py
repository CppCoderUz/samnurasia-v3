
from django import forms


from moderator.models import User, Moderator
from articles.models import Post, Article, ArticleColumn, Journal
from ckeditor import fields
from ckeditor.widgets import CKEditorWidget

from pages.models import Team



class ModeratorUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'password', 'email', 
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].label = 'Ism'
        self.fields['last_name'].label = 'Familya'
        self.fields['email'].label = 'E-mail manzili'
        self.fields['username'].label = 'Username'
        self.fields['password'].label = 'Parol'

        

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'image']    
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].required = True


class JournalForm(forms.ModelForm):
    class Meta:
        model = Journal
        fields = ['name']
    def __init__(self, *args, **kwargs):
        super(JournalForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
    


class ArticleColumnForm(forms.ModelForm):
    class Meta:
        model = ArticleColumn
        fields = ['name']
    
    def __init__(self, *args, **kwargs):
        super(ArticleColumnForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})




class CKEditorForm(forms.Form):
    body = forms.CharField(widget = CKEditorWidget())


class BasicArticelForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['journal', 'column']
    
    def __init__(self, *args, **kwargs):
        super(BasicArticelForm, self).__init__(*args, **kwargs)
        self.fields['journal'].required = False
        self.fields['journal'].widget.attrs.update({'class': 'form-select', 'aria-label': 'Floating label select example'})
        self.fields['column'].widget.attrs.update({'class': 'form-select', 'aria-label': 'Floating label select example'})



class ArticleFullForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'journal', 'column', 'title',
            'first_name', 'last_name','description'
        ]
    def __init__(self, *args, **kwargs):
        super(ArticleFullForm, self).__init__(*args, **kwargs)
        self.fields['journal'].required = False
        self.fields['journal'].widget.attrs.update({'class': 'form-select'})
        self.fields['column'].widget.attrs.update({'class': 'form-select'})
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})

        self.fields['journal'].label = 'Jurnal'
        self.fields['column'].label = 'Maqola rukni'
        self.fields['title'].label = 'Maqola sarlavhasi'
        self.fields['first_name'].label = 'Muallif ismi'
        self.fields['last_name'].label = 'Muallif familyasi'
        self.fields['description'].label = 'Maqola haqida ma\'lumot'
        


class ArticleFullCreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'journal', 'column', 'title',
            'first_name', 'last_name',
            'description', 'file'
        ]
    def __init__(self, *args, **kwargs):
        super(ArticleFullCreateForm, self).__init__(*args, **kwargs)
        self.fields['journal'].required = False
        self.fields['journal'].widget.attrs.update({'class': 'form-select'})
        self.fields['column'].widget.attrs.update({'class': 'form-select'})
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['file'].widget.attrs.update({'class': 'form-control', 'accept': "application/pdf"})

        self.fields['journal'].label = 'Jurnal'
        self.fields['column'].label = 'Maqola rukni'
        self.fields['title'].label = 'Maqola sarlavhasi'
        self.fields['first_name'].label = 'Muallif ismi'
        self.fields['last_name'].label = 'Muallif familyasi'
        self.fields['description'].label = 'Maqola haqida ma\'lumot'
        self.fields['file'].label = 'Maqola fayli (pdf)'



class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super(TeamForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = 'Ismi'
        self.fields['role'].label = 'Vazifasi'
        self.fields['last_name'].label = 'Familyasi'
        self.fields['image'].label = 'Rasmi'
        self.fields['description'].label = 'Ma\'lumot'

        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['role'].widget.attrs.update({'class': 'form-control'})
        self.fields['image'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        


class ModeratorUpdateForm(forms.Form):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    role = forms.CharField(max_length=150)
    email = forms.EmailField(max_length=150)

    def __init__(self, *args, **kwargs):
        super(ModeratorUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['role'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})

        self.fields['first_name'].label = 'Ismi'
        self.fields['role'].label = 'Vazifasi'
        self.fields['last_name'].label = 'Familyasi'
        self.fields['email'].label = 'E-mail manzili'