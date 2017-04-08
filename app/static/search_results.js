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
    var room_select = $('#room_select').val()
    var student_group = $('#student_group').val()
    var reason = $('#reason').val()
    var res_name = $('#res_name').val()

    remove_form()
    create_form()
    add_to_form('room_select', room_select)
    add_to_form('student_group', student_group)
    add_to_form('reason', reason)
    add_to_form('res_name', res_name)
    
    $('#invisible_form').wrap('<form id="full_invisible_form" action="search_confirm" method="post"></form>');
    $('#full_invisible_form').submit();
}

$("#room_select").change(function() {
  $("#room").text($("#room_select").val())
});

$(function() {
    $("#room").text($("#room_select").val());
});