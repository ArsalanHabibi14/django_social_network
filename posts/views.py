from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from MGN.models import MessageOrder, NotificationComment, NotificationFollower, Activity
from users.models import Profile, Order, OrderFollowing
from .forms import AddPostForm, CommentForm
from .models import Posts, Comments
import os
from django.contrib.auth.decorators import login_required


def get_file_path(filepath):
    basename = os.path.basename(str(filepath))
    name, ext = os.path.splitext(str(basename))
    return name, ext

@login_required(login_url='/')
def PostListView(request, *args, **kwargs):
    context = {
        'total_message': 0,
        'total_notifications': 0,
        'total_comment': 0
    }
    user = Profile.objects.filter(user_id=request.user.id).first()
    if user is not None:
        context['user'] = user
        get_notifications = NotificationFollower.objects.filter(user_id=user.id, is_read=False).order_by('-time')
        for n in get_notifications:
            context['total_notifications'] += 1
        get_notifications2 = NotificationComment.objects.filter(user_id=user.id, is_read=False).order_by('-time')
        context['notifications2'] = get_notifications2
        for n in get_notifications2:
            context['total_notifications'] += 1
        # ==================================== Best People =============
        best_people_list = []
        best_order = Order.objects.exclude(owner_id=user.id).order_by('-total_follower')
        for order_best in best_order:
            best_people_list.append(order_best)
        print(best_people_list)
        context['best_User'] = best_people_list
        # ======================
        activity = Activity.objects.filter(user_id=user.id).order_by('-time')[:6]
        if activity is not None:
            context['activities'] = activity
        # ==================================== Following =============
        followers_list = []
        followers_order = Order.objects.filter(owner_id=user.id)
        for order_follower in followers_order:
            followers_list.append(order_follower.orderdetail_set.all())
        print(followers_list)
        context['followers_user'] = followers_list
        # ======================
        # context['object_list'] = Posts.objects.order_by('-id').all()
        posts = Posts.objects.order_by('-time').all()
        for s in posts:
            name, ext = get_file_path(s.file)
            context['ext'] = ext
            print(context['ext'])
        context['object_list'] = posts
        messages_order = MessageOrder.objects.filter(owner_id=user.id).first()
        if messages_order is not None:
            context['messages'] = messages_order.messages_set.order_by('-time').all()
            context['message_order'] = messages_order
            detail_messages = messages_order.messages_set.filter(is_read=False)
            for s in detail_messages:
                context['total_message'] += 1
                print(s)

        #     =============================== Follower posts =====================
    else:
        return redirect('home')
    open_order_main: Order = Order.objects.filter(owner_id=user.id).first()
    if open_order_main is not None:
        context['order'] = open_order_main
        context['followers'] = open_order_main.orderdetail_set.all()

    return render(request, 'posts/post_list_view.html', context)

@login_required(login_url='/')
def add_post(request, *args, **kwargs):
    profile = Profile.objects.filter(user_id=request.user.id).first()
    post_form = AddPostForm(initial={'user': profile.id})
    context = {
        'post_form': post_form,
        'total_message': 0,
        'total_notifications': 0
    }
    user = Profile.objects.filter(user_id=request.user.id).first()
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
            post_form = AddPostForm(request.POST, request.FILES, initial={'user.id': user.id})
            if post_form.is_valid():
                post_form.save()
                get_post = Posts.objects.filter(title=post_form.cleaned_data.get('title')).first()
                Activity.objects.create(user_id=user.id, activity_text=f"Created The {get_post.title} Post")
                return redirect(f'/posts/')
    open_order_main: Order = Order.objects.filter(owner_id=user.id).first()
    if open_order_main is not None:
        context['order'] = open_order_main
        context['followers'] = open_order_main.orderdetail_set.all()
    messages_order = MessageOrder.objects.filter(owner_id=user.id).first()
    if messages_order is not None:
        context['messages'] = messages_order.messages_set.order_by('-time').all()
        context['message_order'] = messages_order
        detail_messages = messages_order.messages_set.filter(is_read=False)
        for s in detail_messages:
            context['total_message'] += 1
    else:
        return redirect('home')
    return render(request, 'posts/add_post.html', context)

@login_required(login_url='/')
def post_detail(request, *args, **kwargs):
    comment_form = CommentForm(request.POST or None)
    user_id = kwargs.get('user_id')
    post_id = kwargs.get('post_id')
    context = {
        'comment_form': comment_form,
        'total_comment': 0,
        'total_message': 0,
        'total_notifications': 0
    }

    user = Profile.objects.filter(user_id=request.user.id).first()
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
        post = Posts.objects.filter(id=post_id).first()
        if post is not None:
            context['post'] = post
            comments = Comments.objects.filter(post_id=post.id)
            context['comments'] = comments
            for s in comments:
                context['total_comment'] += 1
            if comment_form.is_valid():
                comment_text = comment_form.cleaned_data.get('comment_text')
                Comments.objects.create(user_id=user.id, message=comment_text, post_id=post.id)
                context['comment_form'] = CommentForm()
                NotificationComment.objects.create(user_id=post.user.id, send_user_id=user.id, post_id=post.id,
                                                   description=f"commented on your {post.title} post")
                Activity.objects.create(user_id=user.id, activity_text=f"Commented To The {post.title}")
                return redirect(f'/post/{post.id}/{post.title.replace(" ", "-")}')
        open_order_main: Order = Order.objects.filter(owner_id=user.id).first()
        if open_order_main is not None:
            context['order'] = open_order_main
            context['followers'] = open_order_main.orderdetail_set.all()
        messages_order = MessageOrder.objects.filter(owner_id=user.id).first()
        if messages_order is not None:
            context['messages'] = messages_order.messages_set.order_by('-time').all()
            context['message_order'] = messages_order
            detail_messages = messages_order.messages_set.filter(is_read=False)
            for s in detail_messages:
                context['total_message'] += 1
    else:
        return redirect('home')
    return render(request, 'posts/post_detail.html', context)

@login_required(login_url='/')
def delete_post(request, *args, **kwargs):
    post_id = kwargs.get('post_id')
    context = {
        'total_message': 0,
        'total_notifications': 0
    }
    user = Profile.objects.filter(user_id=request.user.id).first()
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
        post = Posts.objects.filter(id=post_id).first()
        if post is not None:
            context['post'] = post
            if request.method == "POST":
                if post is not None:
                    post.delete()
                    Activity.objects.create(user_id=user.id, activity_text=f"Deleted The {post.title}")
                    return redirect(f'/profile/')
        messages_order = MessageOrder.objects.filter(owner_id=user.id).first()
        if messages_order is not None:
            context['messages'] = messages_order.messages_set.order_by('-time').all()
            detail_messages = messages_order.messages_set.filter(is_read=False)
            for s in detail_messages:
                context['total_message'] += 1
    return render(request, 'posts/delete_post.html', context)
