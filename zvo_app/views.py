from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .models import *
import bcrypt


def home(request):
    if request.method == "POST":
        if 'currentUserId' not in request.session or request.session['currentUserId'] != 1:
            return redirect('/login')
        else:
            errors = {}

            if len(request.POST['url']) < 1:
                errors['videoChange'] = "URL is blank!"

            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/admin')
            else:
                if len(Video.objects.all()) == 0:
                    Video.objects.create(url = request.POST['url'])
                else:
                    Video.objects.first().delete()
                    Video.objects.create(url = request.POST['url'])

                messages.success(request, "Greetings Video successfully updated !")
                return redirect('/')
    else:
        context = {'video': Video.objects.first()}
        return render(request, 'index.html', context)


def about(request):
    if request.method == "POST":
        if 'currentUserId' not in request.session or request.session['currentUserId'] != 1:
            return redirect('/login')
        else:
            errors = {}

            if len(About.objects.all()) == 0 and (len(request.POST['aboutHeader']) == 0 or len(request.POST['aboutP1']) == 0 or len(request.POST['aboutP2']) == 0 or not request.FILES):
                errors['aboutNew'] = "All fields must be filled for the initial setup!"
            if len(request.POST['aboutHeader']) == 0 and len(request.POST['aboutP1']) == 0 and len(request.POST['aboutP2']) == 0 and not request.FILES:
                errors['aboutChange'] = "All fields cannot be blank!"
            if len(request.POST['aboutHeader']) == 0 and len(request.POST['aboutP1']) < 11 and len(request.POST['aboutP2']) < 11 and not request.FILES:
                errors['aboutLength'] = "The updated paragraph(s) must be at least 11 characters long!"

            if len(errors) > 0:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/admin')
            elif len(About.objects.all()) == 0:
                About.objects.create(paragraph_1 = request.POST['aboutP1'], paragraph_2 = request.POST['aboutP2'], pic = request.FILES['picFile'])
                return redirect('/about')
            else:
                aboutBody = About.objects.first()
                newHead = request.POST['aboutHeader']
                newP1 = request.POST['aboutP1']
                newP2 = request.POST['aboutP2']

                if request.FILES:
                    newPic = request.FILES['picFile']
                    aboutBody.pic.delete()
                    aboutBody.pic = newPic
                if len(newHead) != 0:
                    aboutBody.header = newHead
                if len(newP1) != 0:
                    aboutBody.paragraph_1 = newP1
                if len(newP2) != 0:
                    aboutBody.paragraph_2 = newP2
                aboutBody.save()

                messages.success(request, "About successfully updated!")
                return redirect('/about')
    else:
        context = {
            'about': About.objects.first(),
        }
        return render(request, 'about.html', context)


def demos(request):
    if request.method == 'POST':
        if 'currentUserId' not in request.session or request.session['currentUserId'] != 1:
            return redirect('/login')

        errors = Demo.objects.demo_validator(request.POST)

        if not request.FILES:
            errors['audioMissing'] = "Demo post is missing audio file!"

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/admin')
        else:
            Demo.objects.create(
                label=request.POST['demoLabel'], genre=request.POST['demoGenre'], file=request.FILES['demoFile'])
            messages.success(request, "Demo successfully posted!")
        return redirect('/demos')
    else:
        if 'currentUserId' not in request.session or request.session['currentUserId'] != 1:
            context = {
                'demos': reversed(Demo.objects.all()),
                'userIsAdmin': False,
            }
        else:
            context = {
                'demos': reversed(Demo.objects.all()),
                'userIsAdmin': request.session['currentUserId'] == 1,
            }
        return render(request, 'demos.html', context)


def admin_delete_demo(request, demoId):
    if 'currentUserId' not in request.session or request.session['currentUserId'] != 1:
        return redirect('/login')
    Demo.objects.get(id=demoId).delete()
    return redirect('/demos')


def news(request):
    if request.method == 'POST':
        if 'currentUserId' not in request.session or request.session['currentUserId'] != 1:
            return redirect('/login')

        errors = Article.objects.article_validator(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/admin')
        else:
            Article.objects.create(
                headline=request.POST['articleHeadline'], body=request.POST['articleBody'])
            messages.success(request, "Article successfully posted!")
            return redirect('/news')
    else:
        if 'currentUserId' not in request.session:
            context = {
                'articles': reversed(Article.objects.all()),
                'userIsAdmin': False,
            }
        else:
            context = {
                'articles': reversed(Article.objects.all()),
                'userIsAdmin': request.session['currentUserId'] == 1,
            }
        return render(request, 'news.html', context)


def admin_delete_article(request, articleId):
    if 'currentUserId' not in request.session or request.session['currentUserId'] != 1:
        return redirect('/login')
    Article.objects.get(id=articleId).delete()
    return redirect('/news')


def bookings(request):
    if request.method == 'POST':
        errors = Message.objects.message_validator(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/bookings')
        else:
            Message.objects.create(name=request.POST['msgName'], email=request.POST['msgEmail'],
                                   content=request.POST['msgContent'], script_url=request.POST['msgURL'])
            messages.success(request, "Message successfully sent!")
            return redirect('/bookings')
    else:
        return render(request, 'bookings.html')


def login(request):
    if request.method == "POST":
        errors = User.objects.login_validator(request.POST)

        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/login')
        else:
            userByEmail = User.objects.filter(
                email=request.POST['userEmail'].lower())
            request.session['currentUserId'] = userByEmail[0].id
            return redirect('/admin')
    else:
        if 'currentUserId' not in request.session or request.session['currentUserId'] != 1:
            return render(request, 'login.html')
        else:
            return redirect('/admin')


def admin_login(request):
    if request.method == 'GET':
        return redirect('/login')

    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/login')
    else:
        userByEmail = User.objects.filter(
            email=request.POST['userEmail'].lower())
        request.session['currentUserId'] = userByEmail[0].id
        return redirect('/admin')


def admin(request):
    if 'currentUserId' not in request.session or request.session['currentUserId'] != 1:
        return redirect('/login')

    if request.method == 'GET':
        if 'sortBy' not in request.session or 'reverseSort' not in request.session:
            context = {
                "inbox": reversed(Message.objects.all()),
                "areNew": len(Message.objects.filter(isNew=1)),
            }
        elif request.session['sortBy'] == 'created_at':
            if request.session['reverseSort'] == False:
                context = {
                    'inbox': reversed(Message.objects.order_by(request.session['sortBy'])),
                    "areNew": len(Message.objects.filter(isNew=1)),
                }
            else:
                context = {
                    'inbox': Message.objects.order_by(request.session['sortBy']),
                    "areNew": len(Message.objects.filter(isNew=1)),
                }
        else:
            if request.session['reverseSort'] == False:
                context = {
                    'inbox': Message.objects.order_by(request.session['sortBy']),
                    "areNew": len(Message.objects.filter(isNew=1)),
                }
            else:
                context = {
                    'inbox': reversed(Message.objects.order_by(request.session['sortBy'])),
                    "areNew": len(Message.objects.filter(isNew=1)),
                }
        context['currentUserId'] = request.session['currentUserId']
        return render(request, 'admin.html', context)
    else:
        errors = User.objects.pw_update_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/admin')
        else:
            currentUser = User.objects.get(id=request.POST['currentUserId'])
            currentUser.pw_hash = bcrypt.hashpw(request.POST['newPw'].encode(), bcrypt.gensalt()).decode()
            currentUser.save()
            messages.success(request, "Password successfully updated!")
            return redirect('/admin')


def admin_sort(request, sortBy):
    if 'currentUserId' not in request.session or request.session['currentUserId'] != 1:
        return redirect('/login')

    if 'sortBy' not in request.session:
        request.session['sortBy'] = sortBy
        request.session['reverseSort'] = False
    elif request.session['sortBy'] == sortBy:
        request.session['reverseSort'] = not request.session['reverseSort']
    else:
        request.session['sortBy'] = sortBy
        request.session['reverseSort'] = False

    return redirect('/admin')


def admin_view(request, msgId):
    if 'currentUserId' not in request.session or request.session['currentUserId'] != 1:
        return redirect('/login')

    viewMessage = Message.objects.get(id=msgId)
    viewMessage.isNew = 0
    viewMessage.save()

    context = {
        "inquiry": Message.objects.get(id=msgId),
    }

    return render(request, 'view.html', context)


def admin_delete_message(request, msgId):
    if 'currentUserId' not in request.session or request.session['currentUserId'] != 1:
        return redirect('/login')

    deleteMessage = Message.objects.get(id=msgId)
    deleteMessage.delete()

    return redirect('/admin')


def admin_logout(request):
    request.session.clear()
    return redirect('/')
