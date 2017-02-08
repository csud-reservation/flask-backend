$(function() {
    if (/just_reserved$/.test(window.location.href)) {
        $('#message_url').removeClass('hidden')
            .html('Votre réservation a bien été effectuée.')
    }
});