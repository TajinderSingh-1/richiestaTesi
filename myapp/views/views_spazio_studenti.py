from itertools import zip_longest

from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View

from myapp.models import *
from richiestaTesi.settings import EMAIL_HOST_USER


def notificadocentiaziende(richieste, richiesteO):
    for r, ro in zip_longest(richieste, richiesteO):
        if r is not None:
            if r.stato == STATO_RICHIESTA[1][0]:  # r.stato == approvata
                send_mail("Avviso riguardo approvazione per studente \"" + str(r.studente) + "\"",
                          "Gentile docente \"" + str(r.docente) + "\" , lo studente \"" + str(
                              r.studente) + "\" , a cui lei aveva approvato la richiesta per la sua proposta \"" + str(
                              r.proposta) + "\", ha accettato un 'altra proposta approvatagli. ",
                          EMAIL_HOST_USER,
                          [r.docente.email],fail_silently=True)
            r.delete()

        if ro is not None:
            if ro.stato == STATO_RICHIESTA[1][0]:  # ro.stato == approvata
                send_mail("Avviso riguardo approvazione per studente \"" + str(ro.studente) + "\"",
                          "Gentile azienda \"" + str(ro.azienda) + "\" , lo studente \"" + str(
                              ro.studente) + "\" , a cui lei aveva approvato la richiesta per la sua offerta \"" + str(
                              ro.offerta) + "\", ha accettato un 'altra proposta approvatagli. ",
                          EMAIL_HOST_USER,
                          [ro.azienda.email],fail_silently=True)
            ro.delete()


def manda_email(proposta, studente):
    # docente che fatto la proposta
    docente = proposta.docente
    send_mail("Accettazione proposta \"" + str(proposta) + "\"",
              "Gentile docente \"" + str(docente) + "\", la proposta \"" + str(
                  proposta) + "\" che lei ha approvato per lo studente \"" + str(
                  studente) + "\" è stata da egli accettata e pertanto è stata ad egli assegnata.",
              EMAIL_HOST_USER,
              [proposta.docente.email], fail_silently=True)

    # identificare altri docenti e aziende dei quali lo studente ha fatto richiesta per una qualche profferta
    richiesteO = RichiestaO.objects.filter(studente=studente)
    richieste = Richiesta.objects.filter(~Q(proposta=proposta), studente=studente)
    notificadocentiaziende(richieste, richiesteO)

    # identificare gli altri studenti richiedenti quella proposta(in pratica quelli la cui richiesta per la proposta
    # è in stato pendente)
    richiesteProp = Richiesta.objects.filter(~Q(studente=studente), proposta=proposta)
    for r in richiesteProp:
        send_mail("Avviso studenti richiedenti proposta \"" + str(r.proposta) + "\"",
                  "Gentile studente \"" + str(r.studente) + "\" la proposta \"" +
                  str(r.proposta) + "\" a cui lei aveva fatto richiesta, è stata assegnata ad un altro studente. ",
                  EMAIL_HOST_USER,
                  [r.studente.email], fail_silently=True)
        r.delete()


def manda_emailO(offerta, studente):
    # azienda che ha fatto l'fferta
    azienda = offerta.azienda
    send_mail("Accettazione offerta \"" + str(offerta) + "\"",
              "Gentile azienda \"" + str(azienda) + "\", l'offerta \"" + str(
                  offerta) + "\" che lei ha approvato per lo studente \"" + str(
                  studente) + "\" è stata da egli accettata e pertanto è stata ad egli assegnata.",
              EMAIL_HOST_USER,
              [offerta.azienda.email], fail_silently=True)

    # identificare docenti e aziende dei quali lo studente ha fatto richiesta per una qualche profferta
    richieste = Richiesta.objects.filter(studente=studente)
    richiesteO = RichiestaO.objects.filter(~Q(offerta=offerta), studente=studente)
    notificadocentiaziende(richieste, richiesteO)

    # identificare gli altri studenti richiedenti quella offerta(in pratica quelli la cui richiesta per la offerta
    # è in stato pendente)
    richiesteOff = RichiestaO.objects.filter(~Q(studente=studente), offerta=offerta)
    for r in richiesteOff:
        send_mail("Avviso studenti richiedenti offerta \"" + str(r.offerta) + "\"",
                  "Gentile studente \"" + str(r.studente) + "\", l'offerta \"" +
                  str(r.offerta) + "\" a cui lei aveva fatto richiesta, è stata assegnata ad un altro studente. ",
                  EMAIL_HOST_USER,
                  [r.studente.email], fail_silently=True)
        r.delete()


class SpazioStudenti(View):
    def post(self, request):
        reqP = request.POST.get('richiesteconfermateP')
        reqO = request.POST.get('richiesteconfermateO')
        studente = Studente.objects.get(user=request.user)

        if reqP is None and reqO is not None:
            studente.isAssegnato = True
            offerta = get_object_or_404(Offerta, id=reqO)
            offerta.macrostato = STATO_OFFERTA[1][0]  # offerta.macrostato = offerta non richiedibile
            offerta.stato = STATO_OFFERTA2[2][0]  # offerta.stato = offerta assegnata
            richiestaO = get_object_or_404(RichiestaO, offerta=offerta, studente=studente)
            richiestaO.stato = STATO_RICHIESTA[2][0]  # richiestaO.stato = accettata
            studente.save()
            offerta.save()
            richiestaO.save()
            manda_emailO(offerta, studente)

        elif reqP is not None and reqO is None:
            studente.isAssegnato = True
            proposta = get_object_or_404(Proposta, id=reqP)
            proposta.macrostato = STATO_PROPOSTA[1][0]  # proposta.macrostato = proposta non richiedibile
            proposta.stato = STATO_PROPOSTA2[2][0]  # proposta.stato = proposta assegnata
            richiesta = get_object_or_404(Richiesta, proposta=proposta, studente=studente)
            richiesta.stato = STATO_RICHIESTA[2][0]  # richiesta.stato = accettata
            studente.save()
            proposta.save()
            richiesta.save()
            manda_email(proposta, studente)

        return redirect('myapp:spazioStudenti')

    def get(self, request):
        proposte_richieste = Proposta
        proposte_richiedibili = Proposta
        offerte_richiedibili = Offerta
        offerte_richieste = Offerta
        richiesteapprovate = Richiesta
        richiesteOapprovate = RichiestaO
        studente = Studente

        if request.user.is_authenticated():
            user = request.user
            if user.groups.filter(name='Studenti').exists():
                studente = Studente.objects.get(user=user)
                if studente.isAssegnato is False:
                    # tutte le proposte dello stesso corso del corso dello studente
                    proposte = Proposta.objects.filter(corso=studente.corso, macrostato=STATO_PROPOSTA[0][0]) # macrostato=proposta richiedibile

                    # tutte le offerte dello stesso corso del corso dello studente che sono state valutate
                    #  positivamente dal docente
                    offerte_tutte = Offerta.objects.filter(corso=studente.corso,
                                                           stato_valutazione=STATO_OFFERTA0[1][0],
                                                           macrostato=STATO_OFFERTA[0][0])

                    # tutte le richieste per tesi o AP fatte dallo studente
                    richieste = Richiesta.objects.filter(studente=studente.id)

                    # tutte le richieste per tirocini fatte dallo studente
                    richiesteO = RichiestaO.objects.filter(studente=studente.id)

                    proposte_richiedibili = []
                    for p in proposte:
                        if not richieste.filter(proposta=p.id).exists():
                            proposte_richiedibili.append(p)

                    # dalle offerte_tutte tolgo quelle a cui lo studente ha già fatto richiesta
                    offerte_richiedibili = []
                    for o_r in offerte_tutte:
                        if not richiesteO.filter(offerta=o_r.id).exists():
                            offerte_richiedibili.append(o_r)

                    proposte_richieste = []
                    richiesteapprovate = []
                    for r in richieste:
                        proposte_richieste.append(r.proposta)
                        if r.stato == STATO_RICHIESTA[1][0]:  # r.stato==approvata
                            richiesteapprovate.append(r)
                            proposte_richieste.remove(r.proposta)

                    offerte_richieste = []
                    richiesteOapprovate = []
                    for r in richiesteO:
                        offerte_richieste.append(r.offerta)
                        if r.stato == STATO_RICHIESTA[1][0]:  # r.stato==approvata
                            richiesteOapprovate.append(r)
                            offerte_richieste.remove(r.offerta)

                    context = {'proposte_richieste': proposte_richieste,
                               'proposte_richiedibili': proposte_richiedibili,
                               'offerte_richiedibili': offerte_richiedibili,
                               'offerte_richieste': offerte_richieste,
                               'richiesteapprovate': richiesteapprovate,
                               'richiesteOapprovate': richiesteOapprovate,
                               'studente': studente,
                               }
                else:
                    richiesta = Richiesta.objects.filter(studente=studente)
                    richiestaO = RichiestaO.objects.filter(studente=studente)
                    #  scoprire se la profferta assegnata allo studente è un offerta o una proposta
                    if not richiesta.count() :
                        profferta = Offerta.objects.get(id=richiestaO.first().offerta.id)
                    if not richiestaO.count():
                        profferta = Proposta.objects.get(id=richiesta.first().proposta.id)

                    context = {
                        'studente': studente,
                        'profferta': profferta,
                    }



        return render(request, 'myapp/spazioStudenti.html', context)
