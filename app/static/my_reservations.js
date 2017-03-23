$(function() {
    $('th').css('background-color', 'rgb(249,249,249)');
});

function reset_modal_view() {
    $(function() {
        $('.selected').removeClass('selected');
        $('.pivot').removeClass('pivot');
    });
}

$( ".delete" ).click(function() {
    ReservationId = $(this).parent().attr("id");
    Table = $(this).parent().parent();
    DetailedInfos = []
    $("#deletedReservation").empty()
    $(Table.children()).each(function(){
        $("#deletedReservation").append($(this).text()+"</br>")
});
    console.log(DetailedInfos)
});

$( "#deleteButton" ).click(function() {
    $.ajax({
    url: "my_reservations?" + $.param({
        "id": ReservationId
    }),
        type: "POST",
    })
    .done(function(data, textStatus, jqXHR) {
        $('#'+ReservationId).parent().remove()
        $('#res_deleted_message').removeClass('hidden')
    })
    .fail(function(jqXHR, textStatus, errorThrown) {
        alert('une erreur est survenue');
    })
});
$(".delete").click(function(){
    $("#myModal").modal()
});



$( ".update" ).click(function() {
    
    console.log(DetailedInfos)
});
