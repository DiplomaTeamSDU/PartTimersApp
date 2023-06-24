$(document).ready(function() {
// Get the rating valueW
    var rating = Math.round(parseFloat($('#rating-value').text()));

    // Get the star elements
    var stars = $('.star');

    // Set the class of each star element based on the rating value
    stars.each(function(index) {
        if (index < rating) {
            $(this).removeClass('fa-regular').addClass('fa-solid');
        } else {
            $(this).removeClass('fa-solid').addClass('fa-regular');
        }
    });
});

$(document).ready(function() {
    // Get the rating valueW
    var rating_user = Math.round(parseFloat($('#rating_user_value').text()));

    // Get the star elements
    var starrs = $('.starr');

    // Set the class of each star element based on the rating value
    starrs.each(function(index) {
        if (index < rating_user) {
            $(this).removeClass('fa-regular').addClass('fa-solid');
        } else {
            $(this).removeClass('fa-solid').addClass('fa-regular');
        }
    });
});
