from django.http import Http404


from moderator.models import AbstractUser, Moderator


def moderator_only(func):
    def wrapper_func(request, *args, **kwargs):
        if Moderator.get_moderator_or_None(request=request) is not None:
            return func(request, *args, **kwargs)
        else:
            raise Http404()
    return wrapper_func



def super_moderator_only(func):
    def wrapper_func(request, *args, **kwargs):
        moderator = Moderator.get_moderator_or_None(request=request)
        if moderator == None:
            raise Http404()
        if moderator.is_created == True:
            return func(request, *args, **kwargs)
        else:
            raise Http404()
    return wrapper_func