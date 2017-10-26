$(window).load(function () {
    $(document).ready(function () {
        $('#infocontent div:not(:first)').hide();
        var $allContentDivs = $('#infocontent div'); // Hide All Content Divs

        $('#linkwrapper a').click(function () {
            var $contentDiv = $("#" + this.id + "content");

            if ($contentDiv.is(":visible")) {
                //$contentDiv.hide(); // Hide Div
            } else {
                $allContentDivs.hide(); // Hide All Divs
                $contentDiv.show(); // Show Div
            }
            //return false;
        });
    });
});