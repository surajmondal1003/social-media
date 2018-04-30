from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from socialapp.forms import UserForm,PersonalInfoForm
from django.contrib.auth.models import User
from socialapp.models import User_Personal,Request,Friends,Post,Comment
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Q
from django.db.models import Count
from django.http import JsonResponse



# Create your views here.
def index(request):

        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('socialapp:newsfeed'))
        return render(request, 'socialapp/index.html')


def get_all_users(request):


    # user_list = User.objects.raw('SELECT s.profilepic,u.id,u.first_name from auth_user as u '
    #                             'LEFT JOIN socialapp_user_personal s on s.user_id=u.id '
    #                             'LEFT JOIN socialapp_request r ON r.request_user_id=u.id '
    #                             'WHERE u.id NOT IN(SELECT friend_id FROM socialapp_friends WHERE user_id='+str(request.session['id'])+') '
    #                             'AND u.id NOT IN(SELECT user_id FROM socialapp_request WHERE  request_status=0 AND request_user_id='+str(request.session['id'])+') '
    #                             'AND u.id NOT IN(SELECT request_user_id FROM socialapp_request WHERE  request_status=0 AND user_id='+str(request.session['id'])+') '
    #                             'AND u.id!='+str(request.session['id'])+'')

    user_list = User_Personal.objects.filter(~Q(user_id=request.user),~Q(user__friend_id__user_id=request.user))

    return user_list


def get_allpending_requests(request):
    user_list = Request.objects.filter(user_id=request.user,request_status=False)

    # user_list = User.objects.raw('SELECT r.id,s.profilepic,u.first_name,u.last_name,r.request_user_id  FROM socialapp_request as r'
		# ' LEFT JOIN auth_user u ON u.id=r.request_user_id'
    #     ' LEFT JOIN socialapp_user_personal s on s.id=r.request_user_id'
    #     ' WHERE  r.request_status=0 AND r.user_id='+str(request.session['id'])+'')


    return user_list



def request_notifications(request):

    # user_list = Request.objects.raw('SELECT r.id,s.profilepic,u.first_name,u.last_name,r.user_id FROM socialapp_request as r'
    #                              ' LEFT JOIN auth_user u ON u.id=r.user_id'
    #                              ' LEFT JOIN socialapp_user_personal s on s.id=r.user_id'
    #                              ' WHERE  r.request_status=0 AND r.request_user_id=' + str(request.session['id']) + '')

    user_list = Request.objects.filter(request_user_id=request.user, request_status=False)

    return render(request, 'fb_activites/newsfeed-accept-request.html',{'user_list':user_list,'media_url':settings.MEDIA_URL})



def get_userdetails(request):

    user_info=User_Personal.objects.filter(pk=str(request.session['id']))

    return user_info

def get_userdetails_byId(id_user):
    user_personal_list = User_Personal.objects.filter(pk=str(id_user))

    return user_personal_list



def register(request):
    registered=False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        personal_form = PersonalInfoForm(data=request.POST)

        if user_form.is_valid() and personal_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = personal_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
        else:
            messages.error(request,user_form.errors, personal_form.errors)
    else:
        user_form = UserForm()
        personal_form=PersonalInfoForm()

    return render(request, 'registrationandlogin/register.html',{'user_form': user_form,
                                                                 'personal_form':personal_form,
                                                                 'registered': registered})

def user_login(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)

                request.session['username']=user.username
                request.session['id']=request.user.id

                #print(request.session.items())
                return HttpResponseRedirect(reverse('socialapp:newsfeed'))
            else:
                return HttpResponse('Account Not Active')
        else:
            print("Someone tried to login and falied")
            print("Username:{} and password :{}".format(username, password))
            messages.error(request, 'username or password not correct')
            return render(request, 'registrationandlogin/login.html', {})
    else:

        return render(request, 'registrationandlogin/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('socialapp:index'))


def newsfeed(request):
    user_list=get_all_users(request)
    pending_requests_list=get_allpending_requests(request)

    post_list=get_allposts(request)
    user_info=get_userdetails(request)



    user_dict = {'user_info':user_info,'user_list': user_list,
                 'pending_requests_list':pending_requests_list,
                 'post_list':post_list,'media_url':settings.MEDIA_URL}

    return render(request, 'fb_activites/newsfeed.html',context=user_dict)

def newsfeed_friends(request):


    # #friends_list = Friends.objects.raw('SELECT * FROM socialapp_friends as f'
		#                                 ' LEFT JOIN auth_user u ON u.id=f.friend_id'
    #                                     ' LEFT JOIN socialapp_user_personal s on s.id=f.friend_id'
    #                                     ' WHERE  f.user_id='+str(request.session['id'])+'')

    friends_list=Friends.objects.filter(user=request.user)


    return render(request, 'fb_activites/newsfeed-friends.html',{
                                                                 'friends_list':friends_list,
                                                                 'media_url': settings.MEDIA_URL
                                                                 })


def newsfeed_messages(request):

    return render(request, 'fb_activites/newsfeed-messages.html')

def timeline_about(request):

    user_info=get_userdetails(request)

    return render(request, 'profile/timeline-about.html',{'user_info':user_info,'media_url':settings.MEDIA_URL})


def see_other_profile(request,id_user):

    user_info=get_userdetails_byId(id_user)

    return render(request, 'profile/timeline-about.html',{'user_info':user_info,'media_url':settings.MEDIA_URL})


def edit_profile_basic(request):
    user_info = get_userdetails(request)


    return render(request, 'profile/edit-profile-basic.html',{'user_info':user_info,'media_url':settings.MEDIA_URL})


def update_profile(request):
    updated = False
    user_info = User.objects.get(pk=request.session['id'])
    user_personal_info = User_Personal.objects.get(pk=request.session['id'])

    if request.method == 'POST':

        try:

            first_name=request.POST.get('first_name')
            last_name=request.POST.get('last_name')
            dob=request.POST.get('dob')
            gender=request.POST.get('gender')
            city=request.POST.get('city')
            country=request.POST.get('country')
            about_text=request.POST.get('about_text')

            user_info.first_name=first_name
            user_info.last_name=last_name
            user_main=user_info.save()

            user_personal_info.dob=dob
            user_personal_info.gender=gender
            user_personal_info.city=city
            user_personal_info.country=country
            user_personal_info.about_text=about_text
            user_personal_info.save()

            updated=True
        except:
            messages.error(request, 'Some problem occured.Please correct the form and submit again.')
            return edit_profile_basic(request)


    return HttpResponseRedirect(reverse('socialapp:timeline_about'))



def notfound404(request):
    return render(request, 'socialapp/404.html')


def add_friend(request,id_user):


    requests_get=Request()
    requests_get.user_id=request.session['id']
    requests_get.request_user_id=id_user
    requests_get.save()


    return HttpResponseRedirect(reverse('socialapp:newsfeed'))



def accept_friend(request,id_request,id_user):


    requests_get=Request.objects.get(pk=id_request)
    friend_user=User.objects.get(pk=id_user)

    requests_get.request_status=True
    requests_get.save()

    friend=Friends()
    friend.user=request.user
    friend.friend=friend_user
    friend.save()

    friend = Friends()
    friend.user=friend_user
    friend.friend=request.user
    friend.save()


    return HttpResponseRedirect(reverse('socialapp:newsfeed'))



def create_post(request):
    posted = False

    if request.method == 'POST':
        user=request.user
        post_info=Post()
        post_text = request.POST.get('post_text')
        post_info.user=user
        post_info.post_text=post_text
        post_info.save()

        #print(request.FILES)


        if 'post_pic' in request.FILES:
            post_info.post_pic = request.FILES['post_pic']

            post_info.save()

            posted=True


        return HttpResponseRedirect(reverse('socialapp:newsfeed'))



def get_allposts(request):



    post_list=Post.objects.raw('SELECT * FROM socialapp_post as p'
                                ' LEFT JOIN auth_user u ON u.id=p.user_id'
                                ' LEFT JOIN socialapp_user_personal s ON s.id=p.user_id'
                               ' WHERE p.user_id='+str(request.session['id'])+''
                               ' OR p.user_id IN(SELECT friend_id FROM socialapp_friends WHERE user_id='+str(request.session['id'])+') ORDER BY p.post_date DESC')


    #post_list = Post.objects.filter(Q(user_id=request.user)|Q(user__friend_id__user=request.user)).order_by('-post_date')


    return post_list




def like_post(request,post_id):
    get_post = Post.objects.get(pk=post_id)
    get_post.likes+=1

    get_post.save()


    return HttpResponseRedirect(reverse('socialapp:newsfeed'))


def get_all_comments():

    get_comments=Comment.objects.filter()



