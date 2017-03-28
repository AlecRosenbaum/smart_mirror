(function (document) {
    'use strict';

    // function $(selector){
    //     return document.querySelector(selector);
    // }

    // google api client id 922831018117-riq3s1ra0fc2gnqc89nmbo9ua5bv2qgp.apps.googleusercontent.com

    window.addEventListener('WebComponentsReady', function () {

        var last_res_time = new Date().getTime();
        var handling_res = false;

        document.addEventListener("keypress", function(event) {
            if (event.keyCode == 13) {
                alert($('myscript-text-web').firstcandidate);
                $('myscript-text-web').clear();
            }
        })

        var time_interval = setInterval(function() {
            var momentNow = moment();

            // set date, day
            $('#date-part').html(momentNow.format('MMMM D'));
            $('#day-part').html(momentNow.format('dddd'));

            // set seconds
            var sec = document.createElement('span')
            sec.setAttribute('id', 'sec-part')
            sec.innerHTML = momentNow.format('ss A');

            // set hours:min
            $('#hrmin-part').html(momentNow.format('h:mm'));
            $('#hrmin-part').append(sec)
        }, 1000);


        var key = 'VTnArfBnZ7xDacvUcCdqdqwYT'
        var patapi = PatAPI(key, "")
        var bus_interval = setInterval(function() {
            // var momentNow = moment();


            patapi.getPredictions({stpid: '2634'}, function (err, preds) {
                console.log(preds)
            })

            // get bus prediction information for stop 2634
            // xhr = new XDomainRequest();
            // xhr.onload = function() {
            //      $('bus-times').html(xhr.responseText)
            // }
            // xhr.open(method, url);
            // $.get(
            //     "http://realtime.portauthority.org/bustime/api/v1/getpredictions",
            //     {key : 'VTnArfBnZ7xDacvUcCdqdqwYT', stpid : '2634'},
            //     function(data) {
            //         $('bus-times').html(data)
            //     }
            // );

            // // set date, day
            // $('#date-part').innerHTML = momentNow.format('MMMM D');
            // $('#day-part').innerHTML = momentNow.format('dddd');

            // // set seconds
            // var sec = document.createElement('span')
            // sec.setAttribute('id', 'sec-part')
            // sec.innerHTML = momentNow.format('ss A');

            // // set hours:min
            // $('#hrmin-part').innerHTML = momentNow.format('h:mm');
            // $('#hrmin-part').appendChild(sec)
        }, 1000);


        $('myscript-text-web').bind('myscript-text-web-result', function(e) { 
            last_res_time = new Date().getTime();            
        });

        function handle_result() {
            if (new Date().getTime() - last_res_time < 2000) {
                setTimeout(handle_result, 100)
            } else {
                alert($('myscript-text-web').firstcandidate);
            }
        }
    });

})(document);
