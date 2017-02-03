var last_element
function select(element) {
    $(function() {
        if(last_element){
            $(last_element).removeClass("selected")
        }
        $(element).addClass("selected")
        last_element = element
    });
}

function submit_invisible_form() {
    var room_select = $('#room_select').val();
    var student_group = $('#student_group').val();
    var reason = $('#reason').val();
    
    add_to_form('room_select', room_select)
    add_to_form('student_group', student_group)
    add_to_form('reason', reason)
    
    var full_form = $('#invisible_form').html();
    $('<form action="search_confirm" method="post">' + full_form + '</form>').submit();
}

$( "#room_select" ).change(function() {
    console.log($("#room_select").val())
  $("#room").text($("#room_select").val())
});


$(function() {
 $("#room").text($("#room_select").val())
});