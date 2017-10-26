from django.conf.urls import url

from myapp.views import views_accesso
from . import views

app_name = 'myapp'

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^logout/$', views_accesso.logout_view, name='logout'),

    url(r'^registratiAziende/$', views.registratiAziende, name='registratiAziende'),
    url(r'accessoAziende/$', views_accesso.accesso, name='accessoAziende'),

    url(r'^registratiDocenti/$', views.registratiDocenti, name='registratiDocenti'),
    url(r'accessoDocenti/$', views_accesso.accesso, name='accessoDocenti'),

    url(r'^registratiStudenti/$', views.registratiStudenti, name='registratiStudenti'),
    url(r'accessoStudenti/$', views_accesso.accesso, name='accessoStudenti'),

    url(r'^spazioAziende/$', views.spazioAziende, name='spazioAziende'),
    url(r'^spazioDocenti/$', views.spazioDocenti, name='spazioDocenti'),
    url(r'^spazioStudenti/$', views.SpazioStudenti.as_view(), name='spazioStudenti'),

    # /spazioAziende/offerta/<offerta_id>/
    url(r'^spazioAziende/offerta/(?P<pk>[0-9]+)/$', views.offertaDettaglioAz, name='offertaDettaglioAz'),

    # /spazioAziende/offerta/<offerta_id>/listaO/
    url(r'^spazioAziende/offerta/(?P<pk>[0-9]+)/listarichiedentio/$', views.ListaRichiedentiO.as_view(), name="listarichiedentiO"),

    # /spazioDocenti/proposta/<proposta_id>/
    url(r'^spazioDocenti/proposta/(?P<pk>[0-9]+)/$', views.propostaDettaglioDoc, name='propostaDettaglioDoc'),

    # /spazioDocenti/proposta/<proposta_id>/lista/
    url(r'^spazioDocenti/proposta/(?P<pk>[0-9]+)/listarichiedenti/$', views.ListaRichiedenti.as_view(), name='listarichiedenti'),

    #/spazioDocenti/offerta/<offerta_id>/
    url(r'^spazioDocenti/offerta/(?P<pk>[0-9]+)/$',views.offertaDettaglioDoc, name='offertaDettaglioDoc'),

    # /spazioDocenti/offerta/<offerta_id>/approva/
    url(r'^spazioDocenti/offerta/(?P<pk>[0-9]+)/approva/$', views.approvaOfferta, name='approvaOfferta'),

    # /spazioDocenti/offerta/<offerta_id>/rifiuta/
    url(r'^spazioDocenti/offerta/(?P<pk>[0-9]+)/rifiuta/$', views.rifiutaOfferta, name='rifiutaOfferta'),

    # /spazioStudenti/proposta/<proposta_id>/
    url(r'^spazioStudenti/proposta/(?P<pk>[0-9]+)/$', views.propostaDettaglioStud, name='propostaDettaglioStud'),

    # /spazioStudenti/proposta/<proposta_id>/richiedi/
    url(r'^spazioStudenti/proposta/(?P<pk>[0-9]+)/richiedi/$', views.richiediProposta, name='richiediProposta'),

    # /spazioStudenti/proposta/<proposta_id>/cancellarichiesta/
    url(r'^spazioStudenti/proposta/(?P<pk>[0-9]+)/cancellarichiesta/$', views.cancellaRichiesta, name='cancellaRichiesta'),

    # /spazioStudenti/offerta/<offerta_id>/
    url(r'^spazioStudenti/offerta/(?P<pk>[0-9]+)/$', views.offertaDettaglioStud, name='offertaDettaglioStud'),

    # /spazioStudenti/offerta/<offerta_id>/richiedi/
    url(r'^spazioStudenti/offerta/(?P<pk>[0-9]+)/richiedi/$', views.richiediOfferta, name='richiediOfferta'),

    # /spazioStudenti/offerta/<offerta_id>/cancellarichiesta/
    url(r'^spazioStudenti/offerta/(?P<pk>[0-9]+)/cancellarichiesta/$', views.cancellaRichiestaO, name='cancellaRichiestaO'),

]
