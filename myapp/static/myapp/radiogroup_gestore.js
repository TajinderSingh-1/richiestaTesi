$(document).ready(function () {
    $('input[type=radio]').prop('checked', false);
    $('input[type=radio]:first').prop('checked', true)

    $('input[type=radio]').click(function (event) {
        $('input[type=radio]').prop('checked', false);
        $(this).prop('checked', true);

        //event.preventDefault();
    });
});