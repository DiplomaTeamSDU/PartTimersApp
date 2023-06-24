$(function(){
    $(".li-sub").hover(
        function(){
            $(".ul-sub", this).css("display", "flex").animate({height: "18rem"}, 100);
        },
        function(){
            $(".ul-sub", this).animate({height: 0}, 100, function() {
              $(this).css("display", "none");
            });
        }
    )
});
