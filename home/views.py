from email.message import EmailMessage
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count
from django.core.mail import EmailMessage
import json
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.urls import reverse
from .forms import *
from .models import *
from django.contrib.auth.decorators import login_required
from .tokens import account_activatin_token
import logging
# from django.contrib.auth import get_user_model

#User = get_user_model()

def is_admin(user):
    return user.is_admin

@login_required(login_url='/login/')
def home(request):
  
    places = Place.objects.all()
    places_data = []
    for place in places:
        place_images = place.images.all()
        image_urls = [image.image.url for image in place_images]
        
        events_ongoing = Event.objects.filter(place=place, end_date__gte=timezone.now())
        events_ongoing_data = []
        
        for event in events_ongoing:
            event_data = {
                'title': event.title,
                'detail': event.detail,
                'start_date': event.start_date.strftime('%m/%d/%Y, %H:%M:%S'),
                'end_date': event.end_date.strftime('%m/%d/%Y, %H:%M:%S'),
            }
            events_ongoing_data.append(event_data)
            
        place_data = {
            'name': place.name,
            'detail': place.detail,
            'id': place.id,
            'location': [place.latitude, place.longitude],
            'image_urls': image_urls,
            'events_ongoing': events_ongoing_data
        }
        places_data.append(place_data)  
    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        profile = None
     
    unread_notifications_count = Notification.objects.filter(user=request.user, is_read=False).count() if request.user.is_authenticated else 0
          
    return render(request, 'home/home.html', {
        'places_data': json.dumps(places_data), 
        'profile': profile,
        'unread_notifications_count': unread_notifications_count,
        'user': request.user,
    })
   
     
def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_admin:
                    messages.success(request, "คุณกำลังเข้าสู่ระบบในสถานะแอดมิน.")
                else:
                    messages.success(request, "ยินดีต้อนรับเข้าสู่หน้าหลัก!")
                return redirect('home')
            else:
                messages.error(request, "ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง กรุณาเข้าสู่ระบบใหม่อีกครั้ง")   
    else:
        form = LoginForm()
    return render(request, 'home/login.html', {'form': form})
        

def logout_user(request):
    logout(request)
    messages.success(request, "คุณได้ออกจากระบบแล้ว")
    return redirect('home')

@user_passes_test(is_admin)
def grant_admin_rights(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_admin = True
    user.save()
    return redirect('manage_accounts')

@user_passes_test(is_admin)
def manage_accounts(request):
    if not request.user.is_admin:
        return redirect('home')
    
    users = User.objects.all()
    profile = request.user.profile
    
    context = {
        'users': users,
        'profile': profile,
    }
    return render(request, 'home/manage_accounts.html', context)

@user_passes_test(is_admin)
def manage_posts(request):
    if not request.user.is_admin:
        return redirect('home')
    
    posts = Post.objects.all()
    profile = request.user.profile
    context = {
        'posts': posts,
        'profile': profile,
    }
    return render(request, 'home/manage_posts.html', context)

@user_passes_test(is_admin)
def delete_user_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('manage_posts')
    context = {
        'post': post,
        'referer_url': request.META.get('HTTP_REFERER')
    }
    return render(request, 'home/posts_delete.html', context)

@user_passes_test(is_admin)
def delete_user_account(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('manage_accounts')
    
    #  users = User.objects.all()
    context = {
        'user': user,
        'referer_url': request.META.get('HTTP_REFERER')
    }
    
    return render(request, 'home/accounts_delete.html', context)

@login_required
def password_change(request):
    user = request.user
    form = SetPasswordForm(user)
    return render(request, 'password_reset.html', {'form': form})

def activate(request, uidb64, token):
    user = get_user_model()
    try: 
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    
    if user is not None and account_activatin_token.check_token(user, token):
        user.is_active =True
        user.save()
        
        messages.success(request, "ขอบคุณสำหรับการยืนยันอีเมล. ตอนนี้คุณสามารถเข้าสู่ระบบบัญชีของคุณ.")
        return redirect('login_user')
    else: 
        messages.error(request, "Activation link is invalid!")
        return redirect('home')

def activateEmail(request, user, to_email):
    mail_subject = "เปิดใช้งานบัญชีผู้ใช้ของคุณ."
    message = render_to_string("home/template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activatin_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'ถึง <b>{user.username}</b>, กรุณาไปที่อีเมล <b>{to_email}</b> ตรวจสอบกล่องข้อความและคลิกลิงก์การเปิดใช้งานที่ได้รับ เพื่อยืนยันและดำเนินการสมัครให้เสร็จสมบูรณ์ <b>Note:</b> ตรวจสอบโฟลเดอร์สแปมของคุณ')
    else:
        messages.error(request, f'ส่งอีเมลไปยัง {to_email} ไม่สำเร็จ, ตรวจสอบว่าคุณพิมพ์ถูกต้องหรือไม่')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            user.save()
            
            try:
                activateEmail(request, user, form.cleaned_data.get('email'))
                #create profile
                Profile.objects.create(user=user)
                messages.success(request, "โปรดตรวจสอบอีเมลของคุณเพื่อยืนยันบัญชี")
                return redirect('home')
            except Exception as e:
                logging.error(f"Failed to send activation email: {e}")
                messages.error(request, "เกิดข้อผิดพลาดในการส่งอีเมลยืนยัน โปรดลองอีกครั้ง")
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = SignUpForm()          
    
    return render(request, 'home/signup.html', {'form':form})

def profile(request, username):
    profile = []
    if request.user.is_authenticated:
        profile = get_object_or_404(Profile, user__username=username)
        user_posts = Post.objects.filter(user=profile.user)
        
        if request.method == 'POST':
            current_user_profile = request.user.profile
            action = request.POST['follow']
            # follow or unfollow
            if action == 'unfollow':
                current_user_profile.follows.remove(profile)
            elif action == 'follow':
                current_user_profile.follows.add(profile)
                
                Notification.objects.create(
                    user=profile.user,
                    message=f"{request.user.username} ได้ติดตามคุณ"
                )
            current_user_profile.save()   
    else: 
        user_posts = []
        
    follower_count = profile.followed_by.count()
    following_count = profile.follows.count()
    context = {
        'profile': profile,
        'user_posts': user_posts, 
        'follower_count': follower_count,
        'following_count': following_count,
           
    }
    return render(request, 'home/profile.html', context)



            
            
    
#@login_required(login_url='/login/')
def profile_settings(request):
    if request.method == 'POST':
        form = ProfileSettingsForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            username = request.user.profile.user.username
            return redirect(reverse('profile', kwargs={'username': username}))
    else:
        form = ProfileSettingsForm(instance=request.user.profile)
        
    referer_url = request.META.get('HTTP_REFERER', '/')
    return render(request, 'home/profile_settings.html', {'form': form, 'referer_url': referer_url})

def add_new_place(request):
    lat = request.GET.get('lat')
    lng = request.GET.get('lng')
    
    if request.method == 'POST':
        form  = PlaceForm(request.POST, request.FILES)
        if form.is_valid():
            place = form.save(commit=False)
            place.user = request.user
            place.latitude = lat
            place.longitude = lng
            place.save()
            if 'image' in request.FILES:
                place_image = PlaceImage(place=place, image=request.FILES['image'])
                place_image.save()
            return redirect('home')
        else:
            print(form.errors)
    else:
        place_url = {'latitude': lat, 'longitude': lng}
        form = PlaceForm(initial=place_url)
    
    return render(request, 'home/add_new_place.html', {'form': form})


