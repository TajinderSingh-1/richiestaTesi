from django.shortcuts import redirect, render

from myapp.forms import OffertaForm
from myapp.models import *


def spazioAziende(request):
    offerte = Offerta
    if request.method == 'POST':
        form = OffertaForm(request.POST)
        if form.is_valid():
            offerta = Offerta()
            offerta.descrizione = form['descrizione'].value()
            offerta.titolo = form['titolo'].value()
            docenteapp = form['docente'].value()
            # Se l'azienda nel form non ha specificato il docente, l'admin dovrà valutare se validare l'offerta immessa
            if docenteapp != '':
                docente = Docente.objects.get(id=form['docente'].value())
                offerta.docente = docente

            corso = Corso.objects.get(id=form['corso'].value())
            offerta.corso = corso

            user = request.user
            azienda = Azienda.objects.get(user=user)
            offerta.azienda = azienda
            offerta.durata = form['durata'].value()
            offerta.save()
            return redirect('myapp:spazioAziende')
    else:
        form = OffertaForm()

    user = request.user
    if request.user.is_authenticated():
        if user.groups.filter(name='Aziende').exists():
            # lista di tutte le offerte immesse da una certa azienda
            offerte = Offerta.objects.filter(azienda=Azienda.objects.get(user=user))

    return render(request, 'myapp/spazioAziende.html', {'offerte': offerte,
                                                        'form': form})
