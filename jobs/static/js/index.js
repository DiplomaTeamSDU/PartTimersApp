const subMenu = document.getElementById("subMenu");

function toggleMenu(){
    subMenu.classList.toggle("open-menu")    
};


$(".nav-item").hover(function() {
    $(this).removeClass('font-weight-500');
    $(this).addClass('font-weight-600');
}, function() {
    $(this).removeClass('font-weight-600');
    $(this).addClass('font-weight-500');
});
