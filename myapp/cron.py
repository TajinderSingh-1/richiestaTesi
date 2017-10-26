from myapp.models import *


# se l'admin cambia la valutazione di un offerta da rifiutata a approvara o in attesa, si toglie la data di rifiuto
def aggiustaDataRifiuto():
    offerte = Offerta.objects.all()
    for o in offerte:
        if o.stato_valutazione != STATO_OFFERTA0[2][1]:
            o.data_rifiuto = None
            o.save()
