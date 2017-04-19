$( document ).ready( function () {

    // reset the animation on hover
    $('#settings-btn-ctr').mouseenter(function() {
        $(".timer-r").css('-webkit-animation-name', 'none');
        void $(".timer-r").outerWidth();
        $(".timer-r").css('-webkit-animation-name', '');

        $(".timer-l").css('-webkit-animation-name', 'none');
        void $(".timer-l").outerWidth();
        $(".timer-l").css('-webkit-animation-name', '');

        setTimeout(function () {
            if ($('#settings-btn-ctr').hasClass("hover")) {
                
                // stop the animation during the redirect
                $('#settings-btn-ctr').removeClass("hover");

                // redirect
                window.location.replace('/pair');
            }
        }, 3000);
    });
    
});