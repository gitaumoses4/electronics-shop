$(document).ready(function () {
    const registrationForm = $("#registration_form");
    const submitButton = registrationForm.find(".ui.button");
    registrationForm.find("input[type=checkbox]").on('change', function () {
        if ($(this).prop('checked')) {
            submitButton.removeClass('disabled')
        } else {
            submitButton.addClass('disabled')
        }
    });

    registrationForm.on('submit', function (e) {
        e.preventDefault();

        registrationForm.addClass("loading");
        $.ajax({
            url: "/admin/register",
            method: 'POST',
            data: registrationForm.serialize(),
            success: function (result) {
                registrationForm.removeClass("loading");
                window.location.href = "/admin";
            },
            error: function (result) {
                registrationForm.removeClass("loading");
                let errors = result['responseJSON']['errors'];

                let html = "<ul>";
                errors.forEach(function (error) {
                    html += "<li>" + error + "</li>";
                });
                html += "</ul>";

                registrationForm.find(".ui.error.message .content").html(html);
                registrationForm.addClass("error");
            }
        })
    })
});