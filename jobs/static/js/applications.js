$(document).ready(function() {
    // Show applications section by default
    $('#applications-pending-id').show();
    $('#applications-accepted-id').hide();
    $('#applications-button').addClass('active');

    // Handle button clicks
    $('#applications-button').click(function() {
        $(this).addClass('active');
        $('#invitations-button').removeClass('active');
        $('#applications-pending-id').show();
        $('#applications-accepted-id').hide();
    });

    $('#invitations-button').click(function() {
        $(this).addClass('active');
        $('#applications-button').removeClass('active');
        $('#applications-pending-id').hide();
        $('#applications-accepted-id').show();
    });
});

$(document).ready(function() {
    // Show vacancies section by default
    $('#applications-vacancies-id').show();
    $('#applications-applicants-id').hide();

    // Handle button clicks
    $('#vacancies-button').click(function() {
        $(this).addClass('active');
        $('#applicants-button').removeClass('active');
        $('#applications-vacancies-id').show();
        $('#applications-applicants-id').hide();
    });

    $('#applicants-button').click(function() {
        $(this).addClass('active');
        $('#vacancies-button').removeClass('active');
        $('#applications-vacancies-id').hide();
        $('#applications-applicants-id').show();
    });
});
