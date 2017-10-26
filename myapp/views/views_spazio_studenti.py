from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View

from myapp.models import *
from richiestaTesi.settings import EMAIL_HOST_USER


def manda_email(proposta, studente):
    docente = proposta.docente  # docente della proposta
    student = studente.nome  # studente che ha fatto la richiesta per la proposta, che è stata approvata e accettata

    # identificare docenti e aziende che hanno approvato una richiesta dello studente ma questi non ha accettato la loro
    richiesteO = RichiestaO.objects.filter(studente=studente)
    richieste = Richiesta.objects.filter(~Q(proposta=proposta), studente=studente)

    print(richieste, richiesteO)

    # identificare gli altri studenti richiedenti quella proposta(in pratica quelli la cui richiesta per la proposta
    # è in stato pendente)
    richiesteProp = Richiesta.objects.filter(~Q(studente=studente), proposta=proposta)
    for r in richiesteProp:
        print(r.studente)

    send_mail("Prova", str(richieste), EMAIL_HOST_USER,
              ['tajisingh07@gmail.com', 'taisingh95@gmail.com', 'taji.singh@live.it'], fail_silently=True)


def manda_emailO(offerta, studente):
    azienda = offerta.docente  # azienda della offerta
    student = studente.nome  # studente che ha fatto la richiesta per la offerta, che è stata approvata e accettata

    # identificare docenti e aziende che hanno approvato una richiesta dello studente ma questi non ha accettato la loro
    richieste = Richiesta.objects.filter(studente=studente)
    richiesteO = RichiestaO.objects.filter(~Q(offerta=offerta), studente=studente)

    print(richieste, richiesteO)

    # identificare gli altri studenti richiedenti quella offerta(in pratica quelli la cui richiesta per la offerta
    # è in stato pendente)
    richiesteOff = RichiestaO.objects.filter(~Q(studente=studente), offerta=offerta)
    for r in richiesteOff:
        print(r.studente)


class SpazioStudenti(View):
    def post(self, request):
        reqP = request.POST.get('richiesteconfermateP')
        reqO = request.POST.get('richiesteconfermateO')
        studente = Studente.objects.get(user=request.user)

        if reqP is None and reqO is not None:
            studente.isAssegnato = True
            offerta = get_object_or_404(Offerta, id=reqO)
            offerta.macrostato = STATO_OFFERTA[1][1]
            offerta.stato = STATO_OFFERTA2[2][1]
            richiestaO = get_object_or_404(RichiestaO, offerta=offerta, studente=studente)
            richiestaO.stato = STATO_RICHIESTA[2][0]  # richiestaO.stato=accettata
            # studente.save()
            # offerta.save()
            # richiestaO.save()
            manda_emailO(offerta, studente)

        elif reqP is not None and reqO is None:
            studente.isAssegnato = True
            proposta = get_object_or_404(Proposta, id=reqP)
            proposta.macrostato = STATO_PROPOSTA[1][1]
            proposta.stato = STATO_PROPOSTA2[2][1]
            richiesta = get_object_or_404(Richiesta, proposta=proposta, studente=studente)
            richiesta.stato = STATO_RICHIESTA[2][0]  # richiesta.stato=accettata
            # studente.save()
            # proposta.save()
            # richiesta.save()
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

                # tutte le proposte dello stesso corso del corso dello studente
                proposte = Proposta.objects.filter(corso=studente.corso)

                # tutte le offerte dello stesso corso del corso dello studente che sono state valutate
                #  positivamente dal docente
                offerte_tutte = Offerta.objects.filter(corso=studente.corso,
                                                       stato_valutazione=STATO_OFFERTA0[1][1],
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
                    if r.stato == STATO_RICHIESTA[1][1]:  # r.stato==approvata
                        richiesteapprovate.append(r)
                        proposte_richieste.remove(r.proposta)

                offerte_richieste = []
                richiesteOapprovate = []
                for r in richiesteO:
                    offerte_richieste.append(r.offerta)
                    if r.stato == STATO_RICHIESTA[1][1]:  # r.stato==approvata
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

        return render(request, 'myapp/spazioStudenti.html', context)
