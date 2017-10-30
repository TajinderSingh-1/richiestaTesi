from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from myapp.models import *
from myapp.models import Offerta, Proposta, Studente, Richiesta
from richiestaTesi.settings import EMAIL_HOST_USER


@login_required()
def approvaOfferta(request, pk):
    if request.method == 'POST':
        offerta = get_object_or_404(Offerta, id=pk)
        offerta.stato_valutazione = STATO_OFFERTA0[1][0]
        offerta.macrostato = STATO_OFFERTA[0][0]
        offerta.save()

        subject = "Approvazione offerta " + "\"" + str(offerta) + "\""
        message = "Gentile azienda " + "\"" + str(
            offerta.azienda) + "\"" + " l'offerta che lei aveva immesso( " + "\"" + str(
            offerta) + " è stata approvata dal docente " + "\"" + str(
            request.user.email) + "\"" + " e quindi ora sarà richiedibile dagli studenti"

        send_mail(subject, message, EMAIL_HOST_USER, [offerta.azienda.email], fail_silently=True)

        return JsonResponse({"Operazione": "Accettazione"})
    else:
        return JsonResponse({"nothing to see": "this isn't happening"})


@login_required()
def rifiutaOfferta(request, pk):
    if request.method == 'POST':
        offerta = get_object_or_404(Offerta, id=pk)
        offerta.stato_valutazione = STATO_OFFERTA0[2][0]
        offerta.macrostato = STATO_OFFERTA[1][0]
        offerta.stato = STATO_OFFERTA2[3][0]
        offerta.data_rifiuto = timezone.now()
        offerta.save()

        subject = "Respinsione offerta " + "\"" + str(offerta) + "\""
        message = "Gentile azienda " + "\"" + str(
            offerta.azienda) + "\"" + " l'offerta che lei aveva immesso( " + "\"" + str(
            offerta) + " è stata respinta dal docente " + "\"" + str(
            request.user.email) + "\"" + " e quindi ora non sarà visibile dagli studenti"

        send_mail(subject, message, EMAIL_HOST_USER, [offerta.azienda.email], fail_silently=True)

        return JsonResponse({"Operazione": "Rifiuto"})
    else:
        return JsonResponse({"nothing to see": "this isn't happening"})


########################################################################################################################
'''Operazioni di richiesta di una proposta'''


@login_required()
def richiediProposta(request, pk):
    if request.method == 'POST':
        proposta = get_object_or_404(Proposta, id=pk)
        proposta.stato = STATO_PROPOSTA2[1][0]
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
                subject = "Richiesta proposta " + "\"" + str(proposta)
                message = "Gentile docente " + "\"" + str(
                    proposta.docente) + "\"" + " la proposta che lei aveva immesso( " + "\"" + str(
                    proposta) + "\"" + " ha una richiesta da parte dello studente " + "\"" + str(
                    request.user.email) + "\""

                send_mail(subject, message, EMAIL_HOST_USER, [proposta.docente.email], fail_silently=True)
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
                subject = "Cancellazione richiesta per la proposta " + "\"" + str(proposta)
                message = "Gentile docente " + "\"" + str(
                    proposta.docente) + "\"" + ", lo studente " + "\"" + str(
                    request.user.email) + "\"" + " che aveva fatto richiesta per la proposta " + "\"" + str(
                    proposta) + "\"" + ", ha cancellato la sua richiesta."

                send_mail(subject, message, EMAIL_HOST_USER, [proposta.docente.email], fail_silently=True)

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
        offerta.stato = STATO_OFFERTA2[1][0]
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
                subject = "Richiesta offerta " + "\"" + str(offerta)
                message = "Gentile azienda " + "\"" + str(
                    offerta.azienda) + "\"" + " l'offerta che lei aveva immesso( " + "\"" + str(
                    offerta) + "\"" + " ha una richiesta da parte dello studente " + "\"" + str(
                    request.user.email) + "\""

                send_mail(subject, message, EMAIL_HOST_USER, [offerta.azienda.email], fail_silently=True)
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
                subject = "Cancellazione richiesta per la offerta " + "\"" + str(offerta)
                message = "Gentile azienda " + "\"" + str(
                    offerta.azienda) + "\"" + ", lo studente " + "\"" + str(
                    request.user.email) + "\"" + " che aveva fatto richiesta per la offerta " + "\"" + str(
                    offerta) + "\"" + ", ha cancellato la sua richiesta."

                send_mail(subject, message, EMAIL_HOST_USER, [offerta.azienda.email], fail_silently=True)

            else:
                return JsonResponse({"messaggio": "La richiesta da eliminare non esiste."})

        return JsonResponse({"messaggio": "Richiesta cancellata con successo."})
    else:
        return JsonResponse({"nothing to see": "this isn't happening"})
