(function (document) {
    'use strict';

    function $(selector){
        return document.querySelector(selector);
    }

    window.addEventListener('WebComponentsReady', function () {

        var last_res_time = new Date().getTime();
        var handling_res = false;
        // var writing = false;
        // $('body').addEventListener('mousedown', function(e) {
        //     console.log("mousedown");
        //     last_drawn_time = new Date().getTime();
        //     writing = true;
        // }, true);
        // $('body').addEventListener('mousemove', function(e) {
        //     last_drawn_time = new Date().getTime();
        //     console.log("mousemove");
        // }, true);
        // $('body').addEventListener('mouseup', function(e) {
        //     console.log("mouseup");
        //     last_drawn_time = new Date().getTime();
        //     writing = false;
        //     setTimeout(handle_result(), 1500);

        // }, true);

        document.addEventListener("keypress", function(event) {
            if (event.keyCode == 13) {
                alert($('myscript-text-web').firstcandidate);
                $('myscript-text-web').clear();
            }
        })


        $('myscript-text-web').addEventListener('myscript-text-web-result', function(e) { 
            last_res_time = new Date().getTime();
            if(!handling_res) {
                // handle_result();
                handling_res = true;
            }
            
        });

        function handle_result() {
            if (new Date().getTime() - last_res_time < 2000) {
                setTimeout(handle_result, 100)
            } else {
                alert($('myscript-text-web').firstcandidate);
                handling_res = false;
            }
        }
    });

})(document);
