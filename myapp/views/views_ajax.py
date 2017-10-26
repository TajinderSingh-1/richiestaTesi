from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from myapp.models import *
from myapp.models import Offerta, Proposta, Studente, Richiesta


@login_required()
def approvaOfferta(request, pk):
    if request.method == 'POST':
        offerta = get_object_or_404(Offerta, id=pk)
        offerta.stato_valutazione = STATO_OFFERTA0[1][1]
        offerta.macrostato = STATO_OFFERTA[0][0]
        offerta.save()
        return JsonResponse({"Operazione": "Accettazione"})
    else:
        return JsonResponse({"nothing to see": "this isn't happening"})


@login_required()
def rifiutaOfferta(request, pk):
    if request.method == 'POST':
        offerta = get_object_or_404(Offerta, id=pk)
        offerta.stato_valutazione = STATO_OFFERTA0[2][1]
        offerta.macrostato = STATO_OFFERTA[1][1]
        offerta.stato = STATO_OFFERTA2[3][1]
        offerta.data_rifiuto = timezone.now()
        offerta.save()
        return JsonResponse({"Operazione": "Rifiuto"})
    else:
        return JsonResponse({"nothing to see": "this isn't happening"})


########################################################################################################################
'''Operazioni di richiesta di una proposta'''


@login_required()
def richiediProposta(request, pk):
    if request.method == 'POST':
        proposta = get_object_or_404(Proposta, id=pk)
        proposta.stato = STATO_PROPOSTA2[1][1]
        proposta.save()
        richiesta = Richiesta()
        richiesta.data_richiesta = timezone.now()
        richiesta.docente = proposta.docente
        richiesta.proposta = proposta

        user = request.user
        if user.groups.filter(name='Studenti').exists():
            studente = get_object_or_404(Studente, user=user)
            richiesta.studente = studente
            try:
                richiesta_app = Richiesta.objects.get(studente=studente, proposta=proposta)
            except ObjectDoesNotExist:
                richiesta_app = None

            if richiesta_app is None:
                richiesta.save()
            else:
                return JsonResponse({"messaggio": "Richiesta è già stata effettuata."})

        return JsonResponse({"messaggio": "Richiesta effettuata con successo."})
    else:
        return JsonResponse({"nothing to see": "this isn't happening"})


def si_azzerano_richieste(proposta):
    richieste = Richiesta.objects.all()
    con_richieste = False

    if richieste:
        for r in richieste:
            if proposta == r.proposta:
                con_richieste = True
                break

    if con_richieste is False:
        proposta.stato = STATO_PROPOSTA2[0][0]  # proposta.stato="senza richieste"
        proposta.save()


@login_required()
def cancellaRichiesta(request, pk):
    if request.method == 'POST':
        proposta = get_object_or_404(Proposta, id=pk)

        user = request.user
        if user.groups.filter(name='Studenti').exists():
            studente = get_object_or_404(Studente, user=user)

            try:
                richiesta_app = Richiesta.objects.get(studente=studente, proposta=proposta)
            except ObjectDoesNotExist:
                richiesta_app = None

            if richiesta_app is not None:
                richiesta_app.delete()
                # verifica che la proposta non ha più richieste e nel caso modifica lo stato della proposta
                si_azzerano_richieste(proposta)

            else:
                return JsonResponse({"messaggio": "La richiesta da eliminare non esiste."})

        return JsonResponse({"messaggio": "Richiesta cancellata con successo."})
    else:
        return JsonResponse({"nothing to see": "this isn't happening"})


########################################################################################################################
'''operazioni di richiesta di una offerta'''


@login_required()
def richiediOfferta(request, pk):
    if request.method == 'POST':
        offerta = get_object_or_404(Offerta, id=pk)
        offerta.stato = STATO_OFFERTA2[1][1]
        offerta.save()
        richiesta = RichiestaO()
        richiesta.data_richiesta = timezone.now()
        richiesta.azienda = offerta.azienda
        richiesta.offerta = offerta

        user = request.user
        if user.groups.filter(name='Studenti').exists():
            studente = get_object_or_404(Studente, user=user)
            richiesta.studente = studente
            try:
                richiesta_app = RichiestaO.objects.get(studente=studente, offerta=offerta)
            except ObjectDoesNotExist:
                richiesta_app = None

            if richiesta_app is None:
                richiesta.save()
            else:
                return JsonResponse({"messaggio": "Richiesta è già stata effettuata."})

        return JsonResponse({"messaggio": "Richiesta effettuata con successo."})
    else:
        return JsonResponse({"nothing to see": "this isn't happening"})


def si_azzerano_richiesteO(offerta):
    richieste = RichiestaO.objects.all()
    con_richieste = False

    if richieste:
        for r in richieste:
            if offerta == r.offerta:
                con_richieste = True
                break

    if con_richieste is False:
        offerta.stato = STATO_OFFERTA2[0][0]  # assegno offerta.stato="senza richieste"
        offerta.save()


@login_required()
def cancellaRichiestaO(request, pk):
    if request.method == 'POST':
        offerta = get_object_or_404(Offerta, id=pk)

        user = request.user
        if user.groups.filter(name='Studenti').exists():
            studente = get_object_or_404(Studente, user=user)

            try:
                richiesta_app = RichiestaO.objects.get(studente=studente, offerta=offerta)
            except ObjectDoesNotExist:
                richiesta_app = None

            if richiesta_app is not None:
                richiesta_app.delete()
                # verifica che la offerta non ha più richieste e nel caso modifica lo stato della offerta
                si_azzerano_richiesteO(offerta)

            else:
                return JsonResponse({"messaggio": "La richiesta da eliminare non esiste."})

        return JsonResponse({"messaggio": "Richiesta cancellata con successo."})
    else:
        return JsonResponse({"nothing to see": "this isn't happening"})
