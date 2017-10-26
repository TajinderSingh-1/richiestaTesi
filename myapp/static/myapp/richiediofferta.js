window.onload = function () {
    var a = document.getElementById("richiediofferta");
    a.onclick = function () {
        if (confirm('Sei sicuro di richiedere questa offerta alla azienda?')) {
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
        if (confirm('Sei sicuro di cancellare la richiesta per questa offerta?')) {
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