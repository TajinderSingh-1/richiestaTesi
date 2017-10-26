from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render

from myapp.models import *


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='Docenti').exists())
def propostaDettaglioDoc(request, pk):
    user = request.user
    docente = get_object_or_404(Docente, user=user)
    proposta = get_object_or_404(Proposta, id=pk)
    docenteApp = proposta.docente
    if docente == docenteApp:
        return render(request, 'myapp/propostaDettaglioDoc.html', {'proposta': proposta})
    else:
        raise PermissionDenied


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='Studenti').exists())
def propostaDettaglioStud(request, pk):
    user = request.user
    studente = Studente.objects.get(user=user)
    proposta = get_object_or_404(Proposta, id=pk, corso=studente.corso)
    try:
        studHaRichiestoProposta = True
        richiesta = Richiesta.objects.get(studente=studente, proposta=proposta)
    except Richiesta.DoesNotExist:
        studHaRichiestoProposta = False

    return render(request, 'myapp/propostaDettaglioStud.html', {'proposta': proposta,
                                                                'studHaRichiestoProposta': studHaRichiestoProposta})
