$(document).ready(function(){
    var images = ['home-pic-6.jpg', 'home-pic-8.jpg', 'home-pic-9.jpg', 'home-pic-12.jpg', 'home-pic-13.jpg', 'home-pic-14.jpg', 'home-pic-15.jpg'];
    var randIndex = Math.floor(Math.random() * images.length);
    var randImage = images[randIndex];
    $('.home-main-image').attr('src', 'static/images/home/' + randImage);
});