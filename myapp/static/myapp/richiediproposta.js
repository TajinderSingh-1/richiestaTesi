window.onload = function () {
    debugger;
    var a = document.getElementById("richiediproposta");
    a.onclick = function () {
        if (confirm('Sei sicuro di richiedere questa proposta al docente?')) {
            $.ajax({
                url: 'richiedi/',
                type: 'POST',
                data: {csrfmiddlewaretoken: getCookie('csrftoken')},
                success: function (json) {
                    alert(json.messaggio);
                },
                error: function (error) {
                    alert("Si è verificato un errore, ritenta.");
                }
            });
        }
    }

    var b = document.getElementById("cancellarichiesta");
    b.onclick = function () {
        if (confirm('Sei sicuro di cancellare la richiesta per questa proposta?')) {
            $.ajax({
                url: 'cancellarichiesta/',
                type: 'POST',
                data: {csrfmiddlewaretoken: getCookie('csrftoken')},
                success: function (json) {
                    alert(json.messaggio);
                },
                error: function (error) {
                    alert("Si è verificato un errore, ritenta.");
                }
            });
        }
    }
}