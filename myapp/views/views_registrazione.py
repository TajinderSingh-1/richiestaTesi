from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.shortcuts import redirect, render
from myapp.forms import AziendaForm, DocenteForm, StudenteForm
from myapp.models import Azienda, Docente, Studente, Corso


def registratiAziende(request):
    if request.method == 'POST':
        form = AziendaForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form['nome'].value()).exists():
                return HttpResponse("Username gia esistente")
            else:
                form['nome'].value()
                azienda = Azienda()
                azienda.sede = form['sede'].value()
                azienda.pIva = form['pIva'].value()
                azienda.email = form['email'].value()
                user = User.objects.create_user(form['nome'].value(), form['email'].value(), form['password'].value())
                g = Group.objects.get(name='Aziende')
                g.user_set.add(user)
                azienda.user = user
                azienda.save()
                return redirect('myapp:index')
    else:
        form = AziendaForm()

    return render(request, 'myapp/registrati.html', {'form': form, 'descr': "Aziende"})


def registratiDocenti(request):
    if request.method == 'POST':
        form = DocenteForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form['codice'].value()).exists():
                return HttpResponse("Username gia esistente")
            else:
                form['nome'].value()
                docente = Docente()
                docente.nome = form['nome'].value()
                docente.cognome = form['cognome'].value()
                docente.materia = form['materia'].value()
                docente.email = form['email'].value()
                user = User.objects.create_user(form['codice'].value(), form['email'].value(), form['password'].value())
                g = Group.objects.get(name='Docenti')
                g.user_set.add(user)
                docente.user = user
                docente.save()
                return redirect('myapp:index')
    else:
        form = DocenteForm()

    return render(request, 'myapp/registrati.html', {'form': form, 'descr': "Docenti"})


def registratiStudenti(request):
    if request.method == 'POST':
        form = StudenteForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form['matricola'].value()).exists():
                return HttpResponse("Username gia esistente")
            else:
                form['nome'].value()
                studente = Studente()
                studente.nome = form['nome'].value()
                studente.cognome = form['cognome'].value()
                studente.anno_corso = form['anno_corso'].value()
                studente.crediti = form['crediti'].value()
                studente.email = form['email'].value()

                corso = Corso.objects.get(id=form['corso'].value())
                studente.corso = corso
                user = User.objects.create_user(form['matricola'].value(), form['email'].value(),
                                                form['password'].value())
                g = Group.objects.get(name='Studenti')
                g.user_set.add(user)
                studente.user = user
                studente.save()
                return redirect('myapp:index')
    else:
        form = StudenteForm()

    return render(request, 'myapp/registrati.html', {'form': form, 'descr': "Studenti"})
