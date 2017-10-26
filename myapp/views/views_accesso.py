from myapp.forms import LoginForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import Group


def accesso(request):
    app_url = request.path
    dictgroup = {
        'gruppo1': '/accessoStudenti/',
        'gruppo2': '/accessoDocenti/',
        'gruppo3': '/accessoAziende/'
    }

    if app_url == dictgroup['gruppo1']:
        g = Group.objects.get(name='Studenti')
        descr = '(Studenti)'

    if app_url == dictgroup['gruppo2']:
        g = Group.objects.get(name='Docenti')
        descr = '(Docenti)'

    if app_url == dictgroup['gruppo3']:
        g = Group.objects.get(name='Aziende')
        descr = '(Aziende)'

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form['username'].value()
            password = form['password'].value()
            user = authenticate(username=username, password=password)
            if user is not None:
                if not user.groups.filter(name__in=[g]).exists():
                    return HttpResponse("Autenticazione fallita: password o username errato")
                login(request, user)
                if app_url == dictgroup['gruppo1']:
                    return redirect('myapp:spazioStudenti')
                elif app_url == dictgroup['gruppo2']:
                    return redirect('myapp:spazioDocenti')
                elif app_url == dictgroup['gruppo3']:
                    return redirect('myapp:spazioAziende')
                    # return redirect('myapp:index')
            else:
                return HttpResponse("Autenticazione fallita: password o username errato")

    else:
        form = LoginForm()

    return render(request, 'myapp/accesso.html', {'form': form, 'descr': descr})


def logout_view(request):
    logout(request)
    return redirect('myapp:index')
