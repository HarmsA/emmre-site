function resize() {
    if ($(window).width() < 751 ) {
        $(function () {
            let element = $(this);
            element.find('.menu-display').css('display', 'block');
        });
    }
    else {
        $(function () {
            let element = $(this);
            element.find('.menu-display').css('display', 'none');
        $('.menu-item').on('mouseover', function () {
            let element = $(this);
            element.find('.menu-display').show(400);
        });
        $('.menu-item').on('mouseleave', function () {
            let element = $(this);
            element.find('.menu-display').hide(200);
        });
        })
    }
};


$(document).ready(function(){
    resize();
    $(window).resize(resize);
});