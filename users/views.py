from django.db.models import Q
from django.shortcuts import render, redirect
from MGN.models import MessageOrder, NotificationFollower, NotificationComment, Activity, Settings
from posts.models import Posts, Comments
from .forms import LoginForm, RegisterForm, UpdateForm
from .models import (
    Profile,
    Order,
    OrderDetail,
    OrderDetailFollowing,
    OrderFollowing,
    Latest_Search,
)
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json


def login_page(request):
    if request.user.is_authenticated:
        return redirect(f'/profile/')
    login_form = LoginForm(request.POST or None)
    context = {
        'login_form': login_form,
    }
    if login_form.is_valid():
        user_name = login_form.cleaned_data.get('user_name')
        password = login_form.cleaned_data.get('password')
        user = authenticate(request, username=user_name, password=password)
        print(user)
        if user is not None:
            login(request, user)
            profile = Profile.objects.filter(user_id=user.id).first()
            profile.is_active = True
            profile.save()
            return redirect(f'/profile/')
    else:
        print("Error")
    return render(request, 'account/home_page.html', context)


def register_page(request):
    form = RegisterForm()
    context = {
        'form': form
    }
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('/profile/')
        else:
            print("Error")
    return render(request, 'account/register_form.html', context)


def header(request):
    context = {
        'total_notifications': 0,
        'total_message': 0
    }
    # get_main_user = Profile.objects.filter(user_id=request.user.id).first()
    # context['user'] = get_main_user
    get_notifications = NotificationFollower.objects.filter(user_id=request.user.profile_set.first().id,
                                                            is_read=False).order_by(
        '-time')
    context['notifications'] = get_notifications
    for n in get_notifications:
        context['total_notifications'] += 1
    get_notifications2 = NotificationComment.objects.filter(user_id=request.user.profile_set.first().id,
                                                            is_read=False).order_by(
        '-time')
    context['notifications2'] = get_notifications2
    for n in get_notifications2:
        context['total_notifications'] += 1
    messages_order = MessageOrder.objects.filter(owner_id=request.user.profile_set.first().id).first()
    if messages_order is not None:
        context['messages'] = messages_order.messages_set.order_by('-time').all()
        context['message_order'] = messages
        detail_messages = messages_order.messages_set.filter(is_read=False)
        for s in detail_messages:
            context['total_message'] += 1
    else:
        return redirect('home')
    return render(request, 'shared/Header.html', context)


@login_required(login_url='/')
def profile_following(request, *args, **kwargs):
    context = {
        'total_message': 0,
        'total_notifications': 0
    }
    get_profile = Profile.objects.filter(user_id=request.user.id).first()
    context['user'] = get_profile
    open_order: Order = Order.objects.filter(owner_id=request.user.profile_set.first().id).first()
    open_order_following: OrderFollowing = OrderFollowing.objects.filter(
        owner_id=request.user.profile_set.first().id).first()
    open_order_main: Order = Order.objects.filter(owner_id=request.user.profile_set.first().id).first()
    if open_order_following is not None and open_order is not None:
        context['order'] = open_order
        context['order_following'] = open_order_following
        context['user_followers'] = open_order.orderdetail_set.all()
        context['user_following'] = open_order_following.orderdetailfollowing_set.all()
        context['right_following'] = open_order_following.orderdetailfollowing_set.all()
        get_fg_search = request.GET.get('fg_search')
        if get_fg_search is not None:
            lookup = (
                    Q(user__user_name__istartswith=get_fg_search) |
                    Q(user__last_name__istartswith=get_fg_search)
            )
            follower = open_order_following.orderdetailfollowing_set.filter(lookup)
            context['user_following'] = follower
    elif open_order is None:
        open_order = Order.objects.create(owner_id=request.user.profile_set.first().id)

    return render(request, 'account/Following.html', context)


@login_required(login_url='/')
def profile_followers(request, *args, **kwargs):
    context = {
        'total_message': 0,
        'total_notifications': 0
    }
    get_profile = Profile.objects.filter(user_id=request.user.id).first()
    context['user'] = get_profile
    open_order_main: Order = Order.objects.filter(owner_id=request.user.profile_set.first().id).first()
    open_order_main_following: OrderFollowing = OrderFollowing.objects.filter(
        owner_id=request.user.profile_set.first().id).first()
    if open_order_main is not None and open_order_main_following:
        context['order'] = open_order_main
        context['order_following'] = open_order_main_following
        context['user_following'] = open_order_main_following.orderdetailfollowing_set.all()
        context['right_following'] = open_order_main_following.orderdetailfollowing_set.all()
        context['user_followers'] = open_order_main.orderdetail_set.all()
        get_fr_search = request.GET.get('fr_search')
        if get_fr_search is not None:
            lookup = (
                    Q(user__user_name__istartswith=get_fr_search) |
                    Q(user__last_name__istartswith=get_fr_search)
            )
            follower = open_order_main.orderdetail_set.filter(lookup)
            context['user_followers'] = follower

    return render(request, 'account/Followers.html', context)


@login_required(login_url='/')
def profile_page(request, *args, **kwargs):
    context = {
        'total_message': 0,
        'total_notifications': 0,
        'total_comments': 0
    }
    activity = Activity.objects.filter(user_id=request.user.profile_set.first().id).order_by('-time')[:6]
    context['activites'] = activity

    posts = Posts.objects.filter(user_id=request.user.profile_set.first().id).order_by('-id').all()
    context['posts'] = posts
    for s in posts:
        get_comments = Comments.objects.filter(post_id=s.id)
        context['comments'] = get_comments
        for s in get_comments:
            context['total_comments'] += 1
    get_notifications = NotificationFollower.objects.filter(user_id=request.user.profile_set.first().id,
                                                            is_read=False).order_by('-time')
    context['notifications'] = get_notifications
    for n in get_notifications:
        context['total_notifications'] += 1
    get_notifications2 = NotificationComment.objects.filter(user_id=request.user.profile_set.first().id,
                                                            is_read=False).order_by('-time')
    context['notifications2'] = get_notifications2
    for n in get_notifications2:
        context['total_notifications'] += 1
    posts = Posts.objects.filter(user_id=request.user.profile_set.first().id).order_by('-id').all()
    context['posts'] = posts
    for s in posts:
        get_comments = Comments.objects.filter(post_id=s.id)
        context['comments'] = get_comments
        for s in get_comments:
            context['total_comments'] += 1
    open_order: Order = Order.objects.filter(owner_id=request.user.profile_set.first().id).first()
    open_order_following: OrderFollowing = OrderFollowing.objects.filter(
        owner_id=request.user.profile_set.first().id).first()
    if open_order is not None:
        context['order'] = open_order
        context['order_following'] = open_order_following
        context['user_following'] = open_order_following.orderdetailfollowing_set.all()
        context['right_following'] = open_order_following.orderdetailfollowing_set.all()
        context['followers'] = open_order.orderdetail_set.all()
    messages_order = MessageOrder.objects.filter(owner_id=request.user.profile_set.first().id).first()
    if messages_order is not None:
        context['messages'] = messages_order.messages_set.order_by('-time').all()
        context['message_order'] = messages
        detail_messages = messages_order.messages_set.filter(is_read=False)
        for s in detail_messages:
            context['total_message'] += 1
    if open_order_following is not None:
        context['user_following'] = open_order_following.orderdetailfollowing_set.all()

    else:
        return redirect('home')

    return render(request, 'account/Profile.html', context)


def add_user_order(main_user_id, user_id, *args, **kwargs):
    order = Order.objects.filter(owner_id=user_id).first()
    order_following = OrderFollowing.objects.filter(owner_id=main_user_id).first()
    if order is None and order_following is None:
        order = Order.objects.create(owner_id=user_id)
        order_following = OrderFollowing.objects.create(owner_id=main_user_id)
    user = Profile.objects.filter(id=main_user_id).first()
    order.orderdetail_set.create(user_id=user.id)
    order.total_follower += 1
    order.save()
    user_view = Profile.objects.filter(id=user_id).first()
    order_following.orderdetailfollowing_set.create(user_id=user_view.id)
    order_following.total_follower += 1
    order_following.save()
    get_user = Profile.objects.filter(id=user_id).first()
    Activity.objects.create(user_id=main_user_id,
                            activity_text=f"Followed The {get_user.user_name} {get_user.last_name}")


def delete_user_order(main_user_id, user_id, *args, **kwargs):
    order = Order.objects.filter(owner_id=user_id).first()
    order_following = OrderFollowing.objects.filter(owner_id=main_user_id).first()
    if order is not None and order_following is not None:
        order.orderdetail_set.filter(user_id=main_user_id).first().delete()
        order.total_follower -= 1
        order.save()
        order_following.orderdetailfollowing_set.filter(user_id=user_id).first().delete()
        order_following.total_follower -= 1
        order_following.save()


@login_required(login_url='/')
def view_profile(request, *args, **kwargs):
    user_id = kwargs.get('user_id')
    user_name = kwargs.get('user_name')
    context = {
        'total_message': 0,
        'total_notifications': 0,
        'message_use': None
    }
    get_profile = Profile.objects.filter(user_id=request.user.id).first()
    print(get_profile.user_name == user_name)
    if user_id is not None and user_name is not None and get_profile.user_name == user_name:
        return redirect(f'/profile/')
    elif user_id is not None and user_name is not None:
        get_user = Profile.objects.filter(id=user_id, user_name=user_name).first()
        get_main_user = Profile.objects.filter(user_id=request.user.id).first()
        if get_user is not None and get_main_user is not None:
            context['user_view'] = get_user
            context['user'] = get_main_user
            get_notifications = NotificationFollower.objects.filter(user_id=get_main_user.id, is_read=False).order_by(
                '-time')
            context['notifications'] = get_notifications
            for n in get_notifications:
                context['total_notifications'] += 1
            get_notifications2 = NotificationComment.objects.filter(user_id=get_main_user.id, is_read=False).order_by(
                '-time')
            context['notifications2'] = get_notifications2
            for n in get_notifications2:
                context['total_notifications'] += 1
            context['posts'] = Posts.objects.filter(user_id=get_user.id)
            open_order: Order = Order.objects.filter(owner_id=get_user.id).first()
            open_order_following: OrderFollowing = OrderFollowing.objects.filter(owner_id=get_user.id).first()
            open_order_main: Order = Order.objects.filter(owner_id=get_main_user.id).first()
            open_order_main_following: OrderFollowing = OrderFollowing.objects.filter(owner_id=get_main_user.id).first()
            if open_order is not None and open_order_following is not None:
                context['order'] = open_order
                context['order_following'] = open_order_following
                context['user_followers'] = open_order.orderdetail_set.all()
                context['user_following'] = open_order_following.orderdetailfollowing_set.all()
                context['following'] = open_order_main_following.orderdetailfollowing_set.all()
                context['right_following'] = open_order_main_following.orderdetailfollowing_set.all()
                detail = open_order.orderdetail_set.filter(user_id=get_main_user.id).first()
                context['detail'] = detail
                if detail is not None:
                    context['btn_name'] = 'Unfollow'
                else:
                    context['btn_name'] = "Follow"
            get_message_detail = open_order.orderdetail_set.filter(user_id=get_user.id).first()
            if get_message_detail is not None:
                context['message_use'] = "yes"
            messages_order = MessageOrder.objects.filter(owner_id=get_main_user.id).first()
            if messages_order is not None:
                context['messages'] = messages_order.messages_set.order_by('-time').all()
                context['message_order'] = messages
                detail_messages = messages_order.messages_set.filter(is_read=False)
                for s in detail_messages:
                    context['total_message'] += 1
            elif open_order is None and open_order_following is not None:
                open_order = Order.objects.create(owner_id=get_user.id)
                open_order_following = OrderFollowing.objects.create(owner_id=get_main_user.id)
            if open_order_main is not None:
                context['followers'] = open_order_main.orderdetail_set.all()
        else:
            return redirect('home')
        # ================================== Followers =======================

    if context['btn_name'] == "Unfollow" and request.method == "POST":
        delete_user_order(main_user_id=get_main_user.id, user_id=get_user.id)
        return redirect(f'/view_profile/{get_user.id}/{get_user.user_name}/view/')
    elif context['btn_name'] == "Follow" and request.method == "POST":
        add_user_order(main_user_id=get_main_user.id, user_id=get_user.id)
        messages.success(request, 'Successfully Follow!!!!')
        get_order = Order.objects.filter(owner_id=user_id).first()
        user = Profile.objects.filter(id=user_id).first()
        user2 = Profile.objects.filter(user_id=request.user.id).first()
        NotificationFollower.objects.create(user_id=user.id, user_following_id=user2.id,
                                            description=f'start following you', order_follower_id=get_order.id)
        return redirect(f'/view_profile/{get_user.id}/{get_user.user_name}/view/')

    return render(request, 'account/Profile_View.html', context)


@login_required(login_url='/')
def followers(request, *args, **kwargs):
    user_id = kwargs.get('user_id')
    user_name = kwargs.get('user_name')
    context = {
        'total_message': 0,
        'total_notifications': 0
    }
    get_profile = Profile.objects.filter(user_id=request.user.id).first()
    if user_id is not None and user_name is not None and get_profile.user_name == user_name:
        return redirect('/profile/')
    elif user_id is not None and user_name is not None:
        get_user = Profile.objects.filter(id=user_id, user_name=user_name).first()
        get_main_user = Profile.objects.filter(user_id=request.user.id).first()
        # if user_id == main_user_id:
        #     return redirect(f'/own_profile/followers/{get_main_user.id}/')
        if get_user is not None:
            context['user'] = get_user
            context['main_user'] = get_main_user
            get_notifications = NotificationFollower.objects.filter(user_id=get_main_user.id, is_read=False).order_by(
                '-time')
            context['notifications'] = get_notifications
            for n in get_notifications:
                context['total_notifications'] += 1
            get_notifications2 = NotificationComment.objects.filter(user_id=get_main_user.id, is_read=False).order_by(
                '-time')
            context['notifications2'] = get_notifications2
            for n in get_notifications2:
                context['total_notifications'] += 1
            open_order: Order = Order.objects.filter(owner_id=get_user.id).first()
            open_order_following: OrderFollowing = OrderFollowing.objects.filter(owner_id=get_user.id).first()
            open_order_main: Order = Order.objects.filter(owner_id=get_main_user.id).first()
            if open_order is not None:
                context['order'] = open_order
                context['order_following'] = open_order_following
                context['user_followers'] = open_order.orderdetail_set.all()
                context['user_following'] = open_order_following.orderdetailfollowing_set.all()
                messages_order = MessageOrder.objects.filter(owner_id=get_main_user.id).first()
                if messages_order is not None:
                    context['messages'] = messages_order.messages_set.order_by('-time').all()
                    context['message_order'] = messages
                    detail_messages = messages_order.messages_set.filter(is_read=False)
                    for s in detail_messages:
                        context['total_message'] += 1
                detail = open_order.orderdetail_set.filter(user_id=get_main_user.id).first()
                context['detail'] = detail
                if detail is not None:
                    context['btn_name'] = 'Unfollow'
                else:
                    context['btn_name'] = "Follow"
                get_fr_search = request.GET.get('fr_search')
                if get_fr_search is not None:
                    lookup = (
                            Q(user__user_name__istartswith=get_fr_search) |
                            Q(user__last_name__istartswith=get_fr_search)
                    )
                    follower = open_order.orderdetail_set.filter(lookup)
                    context['user_followers'] = follower

            elif open_order is None:
                open_order = Order.objects.create(owner_id=get_user.id)
            if open_order_main is not None:
                context['followers'] = open_order_main.orderdetail_set.all()
        else:
            return redirect('home')

    # =========================== Followers ======================

    if context['btn_name'] == "Unfollow" and request.method == "POST":
        delete_user_order(main_user_id=get_main_user.id, user_id=get_user.id)
        return redirect(f'/view_profile/{get_user.id}/{get_user.user_name}/view/')
    elif context['btn_name'] == "Follow" and request.method == "POST":
        add_user_order(main_user_id=get_main_user.id, user_id=get_user.id)
        messages.success(request, 'Successfully Follow!!!!')
        get_order = Order.objects.filter(owner_id=user_id).first()
        user = Profile.objects.filter(id=user_id).first()
        user2 = Profile.objects.filter(user_id=request.user.id).first()
        NotificationFollower.objects.create(user_id=user.id, user_following_id=user2.id,
                                            description=f'start following you', order_follower_id=get_order.id)
        return redirect(f'/view_profile/{get_user.id}/{get_user.user_name}/view/')
    return render(request, 'account/Followers.html', context)


@login_required(login_url='/')
def following(request, *args, **kwargs):
    user_id = kwargs.get('user_id')
    user_name = kwargs.get('user_name')
    context = {
        'total_message': 0,
        'total_notifications': 0
    }
    get_profile = Profile.objects.filter(user_id=request.user.id).first()
    if user_id is not None and user_name is not None and get_profile.user_name == user_name:
        return redirect('/profile/')
    if user_id is not None and user_name is not None:
        get_user = Profile.objects.filter(id=user_id, user_name=user_name).first()
        get_main_user = Profile.objects.filter(user_id=request.user.id).first()
        # if user_id == main_user_id:
        #     return redirect(f'/own_profile/following/{get_main_user.id}/')
        if get_user is not None and get_main_user is not None:
            context['user'] = get_user
            context['main_user'] = get_main_user
            get_notifications = NotificationFollower.objects.filter(user_id=get_main_user.id, is_read=False).order_by(
                '-time')
            context['notifications'] = get_notifications
            for n in get_notifications:
                context['total_notifications'] += 1
            get_notifications2 = NotificationComment.objects.filter(user_id=get_main_user.id, is_read=False).order_by(
                '-time')
            context['notifications2'] = get_notifications2
            for n in get_notifications2:
                context['total_notifications'] += 1
            open_order: Order = Order.objects.filter(owner_id=get_user.id).first()
            open_order_following: OrderFollowing = OrderFollowing.objects.filter(owner_id=get_user.id).first()
            open_order_main: Order = Order.objects.filter(owner_id=get_main_user.id).first()
            if open_order_following is not None and open_order is not None:
                context['order'] = open_order
                context['order_following'] = open_order_following
                context['user_followers'] = open_order.orderdetail_set.all()
                context['user_following'] = open_order_following.orderdetailfollowing_set.all()

                detail = open_order.orderdetail_set.filter(user_id=get_main_user.id).first()
                context['detail'] = detail
                if detail is not None:
                    context['btn_name'] = 'Unfollow'
                else:
                    context['btn_name'] = "Follow"
                get_fg_search = request.GET.get('fg_search')
                if get_fg_search is not None:
                    lookup = (
                            Q(user__user_name__istartswith=get_fg_search) |
                            Q(user__last_name__istartswith=get_fg_search)
                    )
                    following = open_order_following.orderdetailfollowing_set.filter(lookup)
                    context['user_following'] = following
            messages_order = MessageOrder.objects.filter(owner_id=get_main_user.id).first()
            if messages_order is not None:
                context['messages'] = messages_order.messages_set.order_by('-time').all()
                context['message_order'] = messages
                detail_messages = messages_order.messages_set.filter(is_read=False)
                for s in detail_messages:
                    context['total_message'] += 1
            elif open_order is None:
                open_order = Order.objects.create(owner_id=get_user.id)
            if open_order_main is not None:
                context['followers'] = open_order_main.orderdetail_set.all()
        else:
            return redirect('home')
    # =========================== Followers ======================

    if context['btn_name'] == "Unfollow" and request.method == "POST":
        delete_user_order(main_user_id=get_main_user.id, user_id=get_user.id)
        return redirect(f'/view_profile/{get_user.id}/{get_user.user_name}/view/followers')
    elif context['btn_name'] == "Follow" and request.method == "POST":
        add_user_order(main_user_id=get_main_user.id, user_id=get_user.id)
        get_order = Order.objects.filter(owner_id=user_id).first()
        user = Profile.objects.filter(id=user_id).first()
        user2 = Profile.objects.filter(id=request.user.id).first()
        NotificationFollower.objects.create(user_id=user.id, user_following_id=user2.id,
                                            description='start following you', order_follower_id=get_order.id)
        return redirect(f'/view_profile/{get_user.id}/{get_user.user_name}/view/followers')
    return render(request, 'account/Following.html', context)


@login_required(login_url='/')
def logoutUser(request, *args, **kwargs):
    logout(request)
    return redirect('home')


@login_required(login_url='/')
def updateProfile(request, *args, **kwargs):
    user = Profile.objects.filter(user_id=request.user.id).first()
    form = UpdateForm(instance=user)
    context = {
        'form': form,
        'total_message': 0,
        'total_notifications': 0
    }
    if user is not None:
        context['user'] = user
        get_notifications = NotificationFollower.objects.filter(user_id=user.id, is_read=False).order_by('-time')
        context['notifications'] = get_notifications
        for n in get_notifications:
            context['total_notifications'] += 1
        get_notifications2 = NotificationComment.objects.filter(user_id=user.id, is_read=False).order_by('-time')
        context['notifications2'] = get_notifications2
        for n in get_notifications2:
            context['total_notifications'] += 1
        if request.method == 'POST':
            form = UpdateForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                return redirect(f'/profile/')
        open_order: Order = Order.objects.filter(owner_id=user.id).first()
        if open_order is not None:
            context['order'] = open_order
            context['followers'] = open_order.orderdetail_set.all()
        messages_order = MessageOrder.objects.filter(owner_id=user.id).first()
        if messages_order is not None:
            context['messages'] = messages_order.messages_set.order_by('-time').all()
            context['message_order'] = messages
            detail_messages = messages_order.messages_set.filter(is_read=False)
            for s in detail_messages:
                context['total_message'] += 1
    return render(request, 'account/update_profile.html', context)


@login_required(login_url='/')
def about_page(request, *args, **kwargs):
    user = Profile.objects.filter(user_id=request.user.id).first()
    context = {
        'user': user,
        'total_message': 0,
        'total_notifications': 0
    }
    user = Profile.objects.filter(user_id=request.user.id).first()
    if user is None:
        return redirect('home')
    get_notifications = NotificationFollower.objects.filter(user_id=user.id, is_read=False).order_by('-time')
    context['notifications'] = get_notifications
    for n in get_notifications:
        context['total_notifications'] += 1
    get_notifications2 = NotificationComment.objects.filter(user_id=user.id, is_read=False).order_by('-time')
    context['notifications2'] = get_notifications2
    for n in get_notifications2:
        context['total_notifications'] += 1
    open_order: Order = Order.objects.filter(owner_id=user.id).first()
    if open_order is not None:
        context['order'] = open_order
        context['followers'] = open_order.orderdetail_set.all()
    messages_order = MessageOrder.objects.filter(owner_id=user.id).first()
    if messages_order is not None:
        context['messages'] = messages_order.messages_set.order_by('-time').all()
        context['message_order'] = messages
        detail_messages = messages_order.messages_set.filter(is_read=False)
        for s in detail_messages:
            context['total_message'] += 1
    return render(request, 'account/About_page.html', context)


@login_required(login_url='/')
def search(request, *args, **kwargs):
    context = {
        'total_comment': 0,
        'total_message': 0,
        'total_notifications': 0,
        'total_search': 0
    }
    user = Profile.objects.filter(user_id=request.user.id).first()
    if user is not None:
        context['user'] = user
        activity = Activity.objects.filter(user_id=user.id).order_by('-time')[:6]
        context['activities'] = activity
        get_notifications = NotificationFollower.objects.filter(user_id=user.id, is_read=False).order_by('-time')
        context['notifications'] = get_notifications
        for n in get_notifications:
            context['total_notifications'] += 1
        get_notifications2 = NotificationComment.objects.filter(user_id=user.id, is_read=False).order_by('-time')
        context['notifications2'] = get_notifications2
        for n in get_notifications2:
            context['total_notifications'] += 1
        get_search = request.GET.get('search')
        if get_search is not None:
            search_user = Profile.objects.filter(
                Q(user_name__istartswith=get_search) |
                Q(last_name__istartswith=get_search)
            )
            if search_user.exists():
                context['show_user'] = search_user

            lookup_posts = (
                    Q(title__icontains=get_search) |
                    Q(user__user_name__istartswith=get_search) |
                    Q(user__last_name__istartswith=get_search)
            )
            posts = Posts.objects.filter(lookup_posts)
            if posts is not None:
                context['posts'] = posts
                for post in posts:
                    for s in post.comments_set.all():
                        context['total_comment'] += 1
        else:
            get_latest_search = Latest_Search.objects.filter(owner_id=user.id)
            context['show_user'] = get_latest_search
            context['true_latest'] = "no"
            context['posts'] = Posts.objects.all()

        open_order_main: Order = Order.objects.filter(owner_id=user.id).first()
        if open_order_main is not None:
            context['followers'] = open_order_main.orderdetail_set.all()
        messages_order = MessageOrder.objects.filter(owner_id=user.id).first()
        if messages_order is not None:
            context['messages'] = messages_order.messages_set.order_by('-time').all()
            context['message_order'] = messages
            detail_messages = messages_order.messages_set.filter(is_read=False)
            for s in detail_messages:
                context['total_message'] += 1
        best_people_list = []
        best_order = Order.objects.exclude(owner_id=user.id).order_by('-total_follower')
        for order_best in best_order:
            best_people_list.append(order_best)
        context['best_User'] = best_people_list
        # ======================
        # ==================================== Following =============
        followers_list = []
        followers_order = Order.objects.filter(owner_id=user.id)
        for order_follower in followers_order:
            followers_list.append(order_follower.orderdetail_set.all())
        context['followers_user'] = followers_list
    return render(request, 'account/Search_Result.html', context)


@login_required(login_url='/')
def add_latest_search(request, *args, **kwargs):
    user_view_id = kwargs.get('user_view_id')
    context = {}
    if user_view_id is not None:
        get_user_view: Profile = Profile.objects.filter(id=user_view_id).first()
        get_main_user: Profile = Profile.objects.filter(user_id=request.user.id).first()
        if get_main_user is not None and get_user_view is not None:
            context['user'] = get_main_user
            get_user = Latest_Search.objects.filter(owner_id=get_main_user.id, user_id=get_user_view.id).first()
            if get_user is None:
                Latest_Search.objects.create(owner_id=get_main_user.id, user_id=get_user_view.id)
                return redirect(f'/view_profile/{get_user_view.id}/{get_user_view.user_name}/view/')
            else:
                return redirect(f'/view_profile/{get_user_view.id}/{get_user_view.user_name}/view/')


def left_bar(request):
    context = {}
    context['settings'] = Settings.objects.last()
    return render(request, 'shared/left_bar.html', context)


def right_bar(request):
    context = {}
    if request.user.is_authenticated:
        get_user = Profile.objects.filter(user_id=request.user.id).first()
        open_order: Order = Order.objects.filter(owner_id=get_user.id).first()
        open_order_following: OrderFollowing = OrderFollowing.objects.filter(owner_id=get_user.id).first()
        if open_order is not None:
            context['right_following'] = open_order_following.orderdetailfollowing_set.all()
            context['followers'] = open_order.orderdetail_set.all()
    else:
        return redirect('home')
    return render(request, 'shared/right_bar.html', context)
