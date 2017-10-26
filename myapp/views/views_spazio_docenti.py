from django.shortcuts import redirect, render

from myapp.forms import PropostaForm
from myapp.models import *


def spazioDocenti(request):
    proposte = Proposta
    offerte = Offerta
    if request.method == 'POST':
        form = PropostaForm(request.POST)
        if form.is_valid():
            proposta = Proposta()
            proposta.descrizione = form['descrizione'].value()
            proposta.titolo = form['titolo'].value()
            proposta.tipologia = form['tipologia'].value()

            corso = Corso.objects.get(id=form['corso'].value())
            proposta.corso = corso

            user = request.user
            docente = Docente.objects.get(user=user)
            proposta.docente = docente
            proposta.durata = form['durata'].value()
            proposta.save()
            return redirect('myapp:spazioDocenti')
    else:
        form = PropostaForm()

    user = request.user

    if request.user.is_authenticated():
        if user.groups.filter(name='Docenti').exists():
            proposte = Proposta.objects.filter(docente=Docente.objects.get(user=user))
            offerte = Offerta.objects.filter(docente=Docente.objects.get(user=user))

    return render(request, 'myapp/spazioDocenti.html', {'proposte': proposte,
                                                        'offerte': offerte,
                                                        'form': form})
