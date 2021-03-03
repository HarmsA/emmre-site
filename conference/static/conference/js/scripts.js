//TODO mouseleave does not alwayse fire, sometimes multiple children are shown at the same time
$(document).ready(function(){
    $('.menu-item').on('mouseover', function () {
        let element = $(this);
        element.find('.menu-display').show(200);
    });
    $('.menu-item').on('mouseleave', function () {
        let element = $(this);
        element.find('.menu-display').hide();
    });


    $("#topic-buttons > button:first-child").on("click", function () {
        $("#agent-list > *").fadeIn(2000);
    });
    $("#topic-buttons > button:not(:first-child)").on("click", function () {
        let slug=$(this).data("slug");
        $("#agent-list > *:not(."+slug+")").hide(500);
        $("."+slug).fadeIn(2000, function () {
            // $("#agent-list > *:not(."+slug+")").hide();
        });

    });

});

