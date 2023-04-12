var label = $(".rating-form label");

label.hover(function() {
    label.removeClass("fa-regular fa-star");
    label.addClass("fa-solid fa-star")
}, function() {
    label.addClass("fa-regular fa-star")
});
