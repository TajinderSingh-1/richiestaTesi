from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

TIPOLOGIA_CHOICES = [
    ("Tesi", "Tesi"),
    ("Attività progettuale", "Attività progettuale"),
]

CORSO_CHOICES = [
    ("triennale", "triennale"),
    ("magistrale", "magistrale"),
    ("magistrale a ciclo unico", "magistrale a ciclo unico"),
    ("dottorato", "dottorato"),
]

# macrostati di proposta
STATO_PROPOSTA = [
    ("proposta richiedibile", " proposta richiedibile"),
    (" proposta non richiedibile", " proposta non richiedibile"),
]

STATO_PROPOSTA2 = [
    ("proposta senza richieste", "proposta senza richieste"),
    ("proposta con richieste", "proposta con richieste"),
    ("proposta assegnata", "proposta assegnata"),
    ("proposta archiviata", "proposta archiviata"),
]

STATO_OFFERTA0 = [
    ("in attesa di valutazione", "in attesa di valutazione"),
    ("approvata", "approvata"),
    ("rifiutata", "rifiutata"),
]

# macrostati di offerta
STATO_OFFERTA = [
    ("offerta richiedibile", " offerta richiedibile"),
    ("offerta non richiedibile", " offerta non richiedibile"),
]

STATO_OFFERTA2 = [
    ("offerta senza richieste", "offerta senza richieste"),
    ("offerta con richieste", "offerta con richieste"),
    ("offerta assegnata", "offerta assegnata"),
    ("offerta archiviata", "offerta archiviata"),
]

STATO_RICHIESTA = [
    ("pendente", "pendente"),
    ("approvata", "approvata"),
    ("accettata", "accettata"),
]


class Docente(models.Model):
    user = models.OneToOneField(User)
    nome = models.CharField(max_length=200)
    cognome = models.CharField(max_length=200)
    materia = models.CharField(max_length=100, default='materia')
    email = models.EmailField()

    def __unicode__(self):
        return self.user.first_name + ' ' + self.user.last_name

    def __str__(self):
        return self.nome + ' ' + self.cognome

    class Meta:
        verbose_name_plural = "Docenti"


class Dipartimento(models.Model):
    nome = models.CharField(max_length=200)
    sede = models.CharField(max_length=200)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "Dipartimenti"


class Corso(models.Model):
    nome = models.CharField(max_length=100)
    durata = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(6), ])

    # magistrale o triennale
    tipologia = models.CharField(max_length=30, choices=CORSO_CHOICES)
    dipartimento = models.ForeignKey(Dipartimento, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome + '-' + self.dipartimento.nome + ' [' + self.tipologia + ']'

    class Meta:
        verbose_name_plural = "Corsi"


class Studente(models.Model):
    user = models.OneToOneField(User)
    nome = models.CharField(max_length=200)
    cognome = models.CharField(max_length=200)
    email = models.EmailField()
    anno_corso = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(6), ])
    crediti = models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(180), ])
    corso = models.ForeignKey(Corso, on_delete=models.CASCADE)
    isAssegnato = models.BooleanField(default=False)

    def __unicode__(self):
        return self.user.first_name + ' ' + self.user.last_name

    def __str__(self):
        return self.nome + ' ' + self.cognome + ', ' + str(self.user)

    class Meta:
        verbose_name_plural = "Studenti"


class Azienda(models.Model):
    sede = models.CharField(max_length=200)
    pIva = models.CharField(max_length=30)
    email = models.EmailField()
    user = models.OneToOneField(User)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name_plural = "Aziende"


class Offerta(models.Model):
    titolo = models.CharField(max_length=200)
    descrizione = models.TextField()
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE, null=True, blank=True)
    corso = models.ForeignKey(Corso, on_delete=models.CASCADE)
    azienda = models.ForeignKey(Azienda, on_delete=models.CASCADE)
    data_pub = models.DateField(default=timezone.now)
    data_rifiuto = models.DateField(null=True, blank=True)
    durata = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])
    stato_valutazione = models.CharField(max_length=100, choices=STATO_OFFERTA0, default=STATO_OFFERTA0[0][0])
    macrostato = models.CharField(max_length=100, choices=STATO_OFFERTA, default=STATO_OFFERTA[1][0])
    stato = models.CharField(max_length=100, choices=STATO_OFFERTA2, default=STATO_OFFERTA2[0][0])

    def __str__(self):
        return str(self.azienda) + ", " + self.titolo

    class Meta:
        verbose_name_plural = "Offerte tirocinio aziende"


class Proposta(models.Model):
    descrizione = models.TextField()
    titolo = models.CharField(max_length=200)
    macrostato = models.CharField(max_length=100, choices=STATO_PROPOSTA, default=STATO_PROPOSTA[0][0])
    stato = models.CharField(max_length=100, choices=STATO_PROPOSTA2, default=STATO_PROPOSTA2[0][0])

    # tesi, attivita progettuale o tirocinio
    tipologia = models.CharField(max_length=50, choices=TIPOLOGIA_CHOICES)
    data_immissione = models.DateField(default=timezone.now)
    durata = models.PositiveSmallIntegerField()
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    corso = models.ForeignKey(Corso, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Proposte"

    def __str__(self):
        return str(self.docente.nome) + " " + str(self.docente.cognome) + ", " + self.titolo


# richiesta per le proposte di tesi e attività progettuale
class Richiesta(models.Model):
    data_richiesta = models.DateField()
    stato = models.CharField(max_length=50, choices=STATO_RICHIESTA, default=STATO_RICHIESTA[0][0])
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE)
    studente = models.ForeignKey(Studente, on_delete=models.CASCADE)
    proposta = models.ForeignKey(Proposta, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Richieste per tesi o AP"

    def __str__(self):
        return "Docente " + str(self.proposta) + ", " + "Studente " + str(self.studente)


# richiesta per le offerte di tirocinio in aziende
class RichiestaO(models.Model):
    data_richiesta = models.DateField()
    stato = models.CharField(max_length=50, choices=STATO_RICHIESTA, default=STATO_RICHIESTA[0][0])
    azienda = models.ForeignKey(Azienda, on_delete=models.CASCADE)
    studente = models.ForeignKey(Studente, on_delete=models.CASCADE)
    offerta = models.ForeignKey(Offerta, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Richieste per tirocinio"

    def __str__(self):
        return "Azienda " + str(self.offerta) + ", " + "Studente " + str(self.studente)
