from django.shortcuts import render, redirect
from .forms import CreateMessageForm
from .models import MessageOrder, Messages, NotificationFollower, NotificationComment
from users import models
from django.contrib import messages
from users.models import Order, OrderDetail
from users import views
from django.contrib.auth.decorators import login_required
import json
from posts.models import Posts

@login_required(login_url='/')
def message(request, *args, **kwargs):
    context = {
        'total_message': 0,
        'total_notifications' : 0
    }
    user = models.Profile.objects.filter(user_id=request.user.id).first()
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
        messages_order = MessageOrder.objects.filter(owner_id=user.id).first()
        if messages_order is not None:
            context['messages'] = messages_order.messages_set.order_by('is_read').all()
            context['message_order'] = messages
            detail_messages = messages_order.messages_set.filter(is_read=False)
            for s in detail_messages:
                context['total_message'] += 1
        open_order_main: Order = Order.objects.filter(owner_id=user.id).first()
        if open_order_main is not None:
            context['followers'] = open_order_main.orderdetail_set.all()
    return render(request, 'MNG/messages.html', context)

@login_required(login_url='/')
def message_detail(request, *args, **kwargs):
    message_id = kwargs.get('message_id')
    context = {
        'total_message': 0,
        'total_notifications' : 0
    }
    user = models.Profile.objects.filter(user_id=request.user.id).first()
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
        get_order = MessageOrder.objects.filter(owner_id=user.id).first()
        if get_order is not None:
            get_message = get_order.messages_set.filter(id=message_id).first()
            context['message'] = get_message
            get_message.is_read = True
            get_message.save()
            messages_order = MessageOrder.objects.filter(owner_id=user.id).first()
            detail_messages = get_order.messages_set.filter(is_read=False)
            for s in detail_messages:
                context['total_message'] += 1
            context['messages'] = detail_messages
        open_order_main: Order = Order.objects.filter(owner_id=user.id).first()
        if open_order_main is not None:
            context['followers'] = open_order_main.orderdetail_set.all()

    return render(request, 'MNG/message_detail.html', context)

@login_required(login_url='/')
def create_message(request, *args, **kwargs):
    profile = models.Profile.objects.filter(user_id=request.user.id).first()
    send_user_id = kwargs.get('send_user_id')
    get_order = MessageOrder.objects.filter(owner_id=send_user_id).first()
    message_form = CreateMessageForm(initial={'order': get_order.id, 'user': profile.id})
    context = {
        'message_form': message_form,
        'total_message': 0,
        'total_notifications' : 0
    }
    if send_user_id is not None:
        user_send = models.Profile.objects.filter(id=send_user_id).first()
        user = models.Profile.objects.filter(user_id=request.user.id).first()
        if user is not None and user_send is not None:
            context['user'] = user
            context['user_send'] = user_send
            get_notifications = NotificationFollower.objects.filter(user_id=user.id, is_read=False).order_by('-time')
            context['notifications'] = get_notifications
            for n in get_notifications:
                context['total_notifications'] += 1
            get_notifications2 = NotificationComment.objects.filter(user_id=user.id, is_read=False).order_by('-time')
            context['notifications2'] = get_notifications2 
            for n in get_notifications2:
                context['total_notifications'] += 1
            get_order = MessageOrder.objects.filter(owner_id=user_send.id).first()
            if request.method == 'POST' and get_order is not None:
                messages.success(request, 'Successfully message sent!!!')
                message_form = CreateMessageForm(request.POST, initial={'order.id': get_order.id, 'user.id': user.id})
                if message_form.is_valid():
                    message_form.save()
                    return redirect(f'/select_followers')
            if get_order is not None:
                context['messages'] = get_order.messages_set.order_by('-time').all()
                context['message_order'] = messages
                detail_messages = get_order.messages_set.filter(is_read=False)
                for s in detail_messages:
                    context['total_message'] += 1
        open_order_main: Order = Order.objects.filter(owner_id=user.id).first()
        if open_order_main is not None:
            context['followers'] = open_order_main.orderdetail_set.all()
    return render(request, 'MNG/Send_message.html', context)

@login_required(login_url='/')
def select_follower(request, *args, **kwargs):
    context = {
        'total_message': 0,
        'total_notifications' : 0
    }
    user = models.Profile.objects.filter(user_id=request.user.id).first()
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
        followers = models.Order.objects.filter(owner_id=user.id).first()
        if followers is not None:
            context['user_followers'] = followers.orderdetail_set.all()
            messages_order = MessageOrder.objects.filter(owner_id=user.id).first()
            if messages_order is not None:
                context['messages'] = messages_order.messages_set.order_by('-time').all()
                context['message_order'] = messages
                detail_messages = messages_order.messages_set.filter(is_read=False)
                for s in detail_messages:
                    context['total_message'] += 1
    open_order_main: Order = Order.objects.filter(owner_id=user.id).first()
    if open_order_main is not None:
        context['followers'] = open_order_main.orderdetail_set.all()
    return render(request, 'MNG/Select_follower.html', context)

@login_required(login_url='/')
def Notifications(request, *args, **kwargs):
    context = {
    'total_message' : 0,
    'total_notifications' : 0
    }
    user = models.Profile.objects.filter(user_id=request.user.id).first()
    if user is not None:
        context['user'] = user
        get_notifications = NotificationFollower.objects.filter(user_id=user.id).order_by('-time')
        context['notifications'] = get_notifications 
        for n in get_notifications:
            n.is_read = True
            n.save()
        get_notifications_total = NotificationFollower.objects.filter(user_id=user.id, is_read=False).order_by('-time')
        context['notifications_total'] = get_notifications 
        for n in get_notifications_total:
            context['total_notifications'] += 1
        get_notifications2 = NotificationComment.objects.filter(user_id=user.id, is_read=False).order_by('-time')
        context['notifications2'] = get_notifications2 
        for n in get_notifications2:
            context['total_notifications'] += 1
            n.is_read = True
            n.save()
        get_notifications_comment = NotificationComment.objects.filter(user_id=user.id)
        context['nft_comment'] = get_notifications_comment
        messages_order = MessageOrder.objects.filter(owner_id=user.id).first()
        if messages_order is not None:
            context['messages'] = messages_order.messages_set.order_by('-time').all()
            context['message_order'] = messages
            detail_messages = messages_order.messages_set.filter(is_read=False)
            for s in detail_messages:
                context['total_message'] += 1

    return render(request, 'MNG/Notifications.html', context)
