from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from myapp.models import *


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='Aziende').exists())
def offertaDettaglioAz(request, pk):
    user = request.user
    azienda = get_object_or_404(Azienda, user=user)
    offerta = get_object_or_404(Offerta, id=pk)
    aziendaApp = offerta.azienda
    if azienda == aziendaApp:
        return render(request, 'myapp/offertaDettaglioAz.html',
                      {'offerta': offerta,
                       'isApprovata': STATO_OFFERTA0[1][1],
                       'isRifiutata': STATO_OFFERTA0[2][1]})

    else:
        raise PermissionDenied


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='Docenti').exists())
def offertaDettaglioDoc(request, pk):
    user = request.user
    offerta = get_object_or_404(Offerta, id=pk)
    offerte = Offerta.objects.filter(docente=Docente.objects.get(user=user))
    if offerta in offerte:
        return render(request, 'myapp/offertaDettaglioDoc.html',
                      {'offerta': offerta,
                       'isApprovata': STATO_OFFERTA0[1][1],
                       'isRifiutata': STATO_OFFERTA0[2][1]})
    else:
        raise Http404('not found')


@login_required()
@user_passes_test(lambda u: u.groups.filter(name='Studenti').exists())
def offertaDettaglioStud(request, pk):
    user = request.user
    offerta = get_object_or_404(Offerta, id=pk)
    studente = Studente.objects.get(user=user)
    offerte = Offerta.objects.filter(corso=studente.corso)
    if offerta in offerte:
        return render(request, 'myapp/offertaDettaglioStud.html', {'offerta': offerta})
    else:
        raise Http404('not found')
