from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from myapp.models import *
from richiestaTesi.settings import EMAIL_HOST_USER


def notificastudenteO(studente, richiestaO):
    subject = "Approvazione richiesta per offerta " + "\"" + str(richiestaO.offerta) + "\""
    message = "Gentile studente, le comunichiamo che  la richiesta per l'offerta " + "\"" + str(
        richiestaO.offerta) + "\"" + " è"\
        "stata approvata dall'azienda proponente " + "\"" + str(richiestaO.azienda) + "\""
    send_mail(subject,message,EMAIL_HOST_USER,[studente.email],fail_silently=True)


def notificastudente(studente, richiesta):
    subject = "Approvazione richiesta per proposta" + "\"" + str(richiesta.proposta) + "\""
    message = "Gentile studente, le comunichiamo che  la richiesta per la  proposta " + "\"" + str(
        richiesta.proposta) + "\"" + " è"\
        "stata approvata dal docente proponente " + "\"" + str(richiesta.docente) + "\""
    send_mail(subject,message,EMAIL_HOST_USER,[studente.email],fail_silently=True)


def notificatolta_approvazione(studente, r):
    subject = "Approvazione per  richiesta per proposta" + "\"" + str(r.proposta) + "\"" + " ritirata."
    message = "Gentile studente, le comunichiamo che  l'approvazione per la sua richiesta per la  proposta " + "\"" + str(
        r.proposta) + "\"" + " è" \
                                     "stata ritirata dal docente proponente " + "\"" + str(r.docente) + "\""
    send_mail(subject, message, EMAIL_HOST_USER, [studente.email], fail_silently=True)


def notificatolta_approvazioneO(studente, ro):
    subject = "Approvazione per  richiesta per offerta" + "\"" + str(ro.offerta) + "\"" + " ritirata."
    message = "Gentile studente, le comunichiamo che  l'approvazione per la sua richiesta per la  offerta " + "\"" + str(
        ro.offerta) + "\"" + " è" \
                                     "stata ritirata dalla azienda  proponente " + "\"" + str(ro.azienda) + "\""
    send_mail(subject, message, EMAIL_HOST_USER, [studente.email], fail_silently=True)


@method_decorator(login_required, name='dispatch')
class ListaRichiedentiO(View):
    @method_decorator(user_passes_test(lambda u: u.groups.filter(name='Aziende').exists()))
    def get(self, request, pk):
        user = request.user
        azienda = Azienda.objects.get(user=user)
        offerta = get_object_or_404(Offerta, id=pk)
        if azienda == offerta.azienda:
            richieste = RichiestaO.objects.filter(offerta=offerta)
            return render(request, 'myapp/listarichiedentiO.html', {'offerta': offerta,
                                                                    'richieste': richieste})
        else:
            raise PermissionDenied

    @method_decorator(user_passes_test(lambda u: u.groups.filter(name='Aziende').exists()))
    def post(self, request, pk):
        idStud = request.POST.get('studente')
        offerta = get_object_or_404(Offerta, id=pk)
        try:
            user = User.objects.get(username=str(idStud))
            studente = Studente.objects.get(user=user)
            richiestaO = RichiestaO.objects.get(offerta=offerta, studente=studente)
        except (Studente.DoesNotExist, User.DoesNotExist):
            studente = None
            richiestaO = None

        if richiestaO is not None and studente is not None:
            richiestaO.stato = STATO_RICHIESTA[1][0]  # richiestaO.stato = approvata
            richiestaO.save()
            notificastudenteO(studente, richiestaO)
            richiesteO = RichiestaO.objects.filter(offerta=offerta)
            for ro in richiesteO:
                if ro != richiestaO:
                    if ro.stato != STATO_RICHIESTA[0][0]:
                        ro.stato = STATO_RICHIESTA[0][0]  # ro.stato = pendente
                        ro.save()
                        notificatolta_approvazioneO(studente, ro)

        return redirect('myapp:listarichiedentiO', pk)




@method_decorator(login_required, name='dispatch')
class ListaRichiedenti(View):
    @method_decorator(user_passes_test(lambda u: u.groups.filter(name='Docenti').exists()))
    def get(self, request, pk):
        user = request.user
        docente = Docente.objects.get(user=user)
        proposta = get_object_or_404(Proposta, id=pk)
        if docente == proposta.docente:
            richieste = Richiesta.objects.filter(proposta=proposta)
            return render(request, 'myapp/listarichiedenti.html', {'proposta': proposta,
                                                                   'richieste': richieste})
        else:
            raise PermissionDenied

    @method_decorator(user_passes_test(lambda u: u.groups.filter(name='Docenti').exists()))
    def post(self, request, pk):
        idStud = request.POST.get('studente')
        proposta = get_object_or_404(Proposta, id=pk)
        try:
            user = User.objects.get(username=str(idStud))
            studente = Studente.objects.get(user=user)
            richiesta = Richiesta.objects.get(proposta=proposta, studente=studente)
        except (Studente.DoesNotExist, User.DoesNotExist):
            studente = None
            richiesta = None

        if richiesta is not None and studente is not None:
            richiesta.stato = STATO_RICHIESTA[1][0]  # richiesta.stato=approvata
            richiesta.save()
            notificastudente(studente,richiesta)
            richieste = Richiesta.objects.filter(proposta=proposta)
            for r in richieste:
                if r != richiesta:
                    if r.stato != STATO_RICHIESTA[0][0]:
                        r.stato = STATO_RICHIESTA[0][0]  # r.stato=pendente
                        r.save()
                        notificatolta_approvazione(studente,r)

        return redirect('myapp:listarichiedenti', pk)
