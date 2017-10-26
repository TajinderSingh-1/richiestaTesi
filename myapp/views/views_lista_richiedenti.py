from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from myapp.models import *


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
            richiestaO.stato = STATO_RICHIESTA[1][1]  # richiestaO.stato = approvata
            richiestaO.save()
            richiesteO = RichiestaO.objects.filter(offerta=offerta)
            for r in richiesteO:
                if r != richiestaO:
                    r.stato = STATO_RICHIESTA[0][0]  # r.stato = pendente
                    r.save()

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
            richiesta.stato = STATO_RICHIESTA[1][1]  # richiesta.stato=approvata
            richiesta.save()
            richieste = Richiesta.objects.filter(proposta=proposta)
            for r in richieste:
                if r != richiesta:
                    r.stato = STATO_RICHIESTA[0][0]  # r.stato=pendente
                    r.save()

        return redirect('myapp:listarichiedenti', pk)
