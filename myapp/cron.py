from myapp.models import *


# se l'admin cambia la valutazione di un offerta da rifiutata a approvara o in attesa, si toglie la data di rifiuto
from myapp.views import si_azzerano_richiesteO, si_azzerano_richieste


def aggiustaDataRifiuto():
    offerte = Offerta.objects.all()
    for o in offerte:
        if o.stato_valutazione != STATO_OFFERTA0[2][0]:  # o.stato_valutazione !=rifiutata
            o.data_rifiuto = None
            o.save()


def aggiusta_stato_con_richieste_senza():
    offerte = Offerta.objects.all()
    for o in offerte:
        if o.stato is not STATO_OFFERTA2[2][0]: # o.stato!=offerta assegnata
            si_azzerano_richiesteO(o)

    proposte = Proposta.objects.all()
    for p in proposte:
        if p.stato is not STATO_PROPOSTA2[2][0]: # p.stato!=proposta assegnata
                si_azzerano_richieste(p)