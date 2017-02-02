$(function() {
    $('.input-daterange input').each(function() {
        $(this).datepicker({language: "fr"});
     });
    $('.date').datepicker({language: "fr"});
    $("#switch").change(function() {
        if(this.checked) {
            //$(".end_dp").hide()
            $('#recurrence_off').hide()             //new
            $('#recurrence_on').show()             //new 
            $(".date_input_form").first().removeClass('col-sm-3').addClass('col-sm-5')
        }
        else{
            //$(".end_dp").show()
            $('#recurrence_on').hide()             //new   
            $('#recurrence_off').show()             //new 
            $(".date_input_form").first().removeClass('col-sm-5').addClass('col-sm-3')
        }
    });
});

function select(element) {
    $(function() {
        $(element).toggleClass("selected");
    });
}

function reset_modal_view() {
    $(function() {
        $('.selected').removeClass('selected');
    });
}