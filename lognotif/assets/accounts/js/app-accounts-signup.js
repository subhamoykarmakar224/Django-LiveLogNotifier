$(function() {
    $('.tabs').tabs();
    $('.modal').modal();
    $('#btn-close-new-user-form').on('click', function() {
        $('#modal-add-user').slideToggle()
    });
    $('#btn-toggle-add-user-form').on('click', function() {
        $('#modal-add-user').slideToggle()
    });

    $(".role").on('click', function() {
        $("#id_role").val($(this).val())
    });

    $('.to-del-uname').on('click', function() {
        var t = ($(this).text()).split(" ")[1]
        $('#link-delete-u').attr('href', '/account/delete/' + t)
    });


    $("#btn-create-new-user-form").on('click', function() {

        if($("#passwd1").val() == '' ||  $("#username").val() == '') {
            $("#new-user-errors").text("Passwords/Username cannot be blank!");
        } else if( $("#passwd1").val().length < 8 ) {
            $("#new-user-errors").text("Passwords too short. Should be minimum of 8 characters.");
        } else if($("#passwd1").val() == $("#passwd2").val()) {
            $("#id_username").val($("#username").val());
            $("#id_password").val($("#passwd1").val());
            $("#btn-submit-new-user").trigger('click')
        } else {
            $("#new-user-errors").text("Passwords did not match!");
        }
    })
});