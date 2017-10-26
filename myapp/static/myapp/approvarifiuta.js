window.onload = function () {
    var a = document.getElementById("accetta");
    a.onclick = function () {
        if (confirm('Sei sicuro di approvare la offerta della azienda?')) {
            $.ajax({
                url: 'approva/',
                type: 'POST',
                    data: {csrfmiddlewaretoken: getCookie('csrftoken')},
                success: function (result) {
                    alert("Offerta aziendale accettata, sarà visibile agli studenti.");
                },
                error: function (error) {
                    alert("Si è verificato un errore, ritenta.");
                }
            });
        }
    }

    var b = document.getElementById("rifiuta");
    b.onclick = function () {
        if (confirm('Sei sicuro di rifiutare la offerta della azienda?')) {
            $.ajax({
                url: 'rifiuta/',
                type: 'POST',
                data: {csrfmiddlewaretoken: getCookie('csrftoken')},
                success: function (result) {
                    alert("Offerta aziendale rifiutata, il rifiuto sarà notificato alla azienda.");
                },
                error: function (error) {
                    alert("Si è verificato un errore, ritenta.");
                }
            });
        }

    }
}
