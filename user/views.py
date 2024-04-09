from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from new import settings
from django.contrib.auth.models import Group
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from .tokens import generate_token
from .middlewares import guest, allowed_user
from .models import *

User = get_user_model()
# Create your views here.
@guest
def index(request):
    user = request.user
    is_default_user = user.groups.filter(name="default").exists()
    return render(request, "index.html",{'is_default_user': is_default_user})

@allowed_user(allowed_roles=['default','Salers'])
def home(request):
    user = request.user
    is_default_user = user.groups.filter(name="default").exists()
    return render(request, "index.html",{'is_default_user': is_default_user})

@allowed_user(allowed_roles=['Salers'])
def salers(request):
    return render(request , 'salers.html')

@allowed_user(allowed_roles=['default','Salers'])
def change_role(request):
    user = request.user
    current_group = user.groups.first()  # Get the user's current group

    if request.method == "POST":
        # Authenticate the user
        email = user.email
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        
        if user is not None:
            new_group_id = request.POST.get('new_group_id')
            new_group = Group.objects.get(id=new_group_id)
            
            # Check if the user is trying to change to the current group
            if new_group != current_group:
                # Remove user from existing group and add to the new group
                user.groups.clear()
                user.groups.add(new_group)
                messages.success(request, "User group updated successfully.")
            else:
                messages.warning(request, "You are already in this group.")
            
            # If the new group is "Saler," handle Saler creation
            if new_group.name == 'Salers':
                hotel_name = request.POST.get('hotel')
                address = request.POST.get('address')
                contact = request.POST.get('contact')
                saler = Saler.objects.create(name=user, hotel=hotel_name, addresh=address, contact=contact)
                saler.save()
                
                messages.success(request, "Saler details added successfully.")
            
            return redirect('home')  # Redirect to user's profile page or any other appropriate page
        
        else:
            messages.error(request, "Authentication failed. Please check your password.")
            return redirect('change_role')  # Redirect back to the change_role page if authentication fails

    available_groups = Group.objects.exclude(id=current_group.id)
    
    return render(request, 'change_role.html', {'current_group': current_group, 'available_groups': available_groups})

@guest
def signup(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        tc = request.POST.get('tc')
        
        if User.objects.filter(name=name).exists():
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('signup')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('signup')
        
        if len(name)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('signup')
        
        if password != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('signup')
        
        myuser = User.objects.create_user(email=email, name=name ,tc=tc , password= password)
        myuser.is_active = False
        myuser.save()
        
        default_group = Group.objects.get(name='default')
        myuser.groups.add(default_group)
        messages.success(request, "Please check your email to confirm your email address in order to activate your account.")
        
        # Welcome Email
        subject = "Welcome to Trend !!"
        message = "Hello " + myuser.name + "!! \n" + "Welcome to  Trend  \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\n Trend "        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @  Trend !!"
        message2 = render_to_string('email_confirmation.html',{
            
            'name': myuser.name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()
        
        return redirect('signin')
        
        
    return render(request, "signup.html")

@guest
def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin')
    else:
        return render(request,'activation_failed.html')
      
@guest
def signin(request):
    if request.method == 'POST':
        username_or_email = request.POST['username']
        pass1 = request.POST['password']
        
        # Check if username_or_email is an email
        if '@' in username_or_email:
            # Authenticate using email
            user = authenticate(email=username_or_email, password=pass1)
        else:
            # Authenticate using username
            user = authenticate(username=username_or_email, password=pass1)
        
        if user is not None:
            login(request, user)
            user_groups = user.groups.values_list('name', flat=True)
            if 'default' in user_groups:
                return redirect('home')
            elif 'Salers' in user_groups:
                return redirect('salers')
            elif 'Admin' in user_groups:
                return redirect('home')
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect(request.path)
    
    return render(request, "signin.html")

@allowed_user(allowed_roles=['default','Salers', 'Admin'])
def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')