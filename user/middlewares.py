from django.shortcuts import redirect
from django.http import HttpResponse
# ******* Authenticated *******
def allowed_user(allowed_roles=[]):
    def auth(view_function):    
        def wrapped_view(request,*args,**kwargs):
            if request.user.is_authenticated == False:
                return redirect('signin')
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            if group in allowed_roles or group == 'Admin': 
                return view_function(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorize to view this page')
        return wrapped_view
    return auth

# ******* Guest *******
def guest(view_function):
    def wrapped_view(request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return view_function(request, *args, **kwargs)
    return wrapped_view
