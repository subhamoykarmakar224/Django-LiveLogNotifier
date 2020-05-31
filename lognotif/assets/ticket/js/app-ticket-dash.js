$(function() {
    $('.radio-assignment').on('click', function() {

        $('#id_assignment_name').val(
            $(this).val()
        )
    });
    $('.modal').modal();
});