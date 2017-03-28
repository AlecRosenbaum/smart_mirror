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
                document.querySelector('myscript-text-web').clear();
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

        var bus_interval = setInterval(function() {
            var parseXml = function(xmlStr) {
                return ( new window.DOMParser() ).parseFromString(xmlStr, "text/xml");
            };
            $.get(
                "http://realtime.portauthority.org/bustime/api/v1/getpredictions",
                {key : 'VTnArfBnZ7xDacvUcCdqdqwYT', stpid : '2634'},
                function(data) {
                    $('#bus-times').empty();

                    var predictions = data.getElementsByTagName("prd");
                    console.log(predictions);

                    // want them to be in descending order
                    for (var i = 0; i < predictions.length; i++) {
                        // parse predicted arrival time
                        var prdtm = moment(predictions[i].getElementsByTagName("prdtm")[0].innerHTML, "YYYYMMDD HH:mm");

                        // create element with route number
                        var route = document.createElement('span');
                        route.setAttribute('class', 'prd-name');
                        route.innerHTML = predictions[i].getElementsByTagName("rt")[0].innerHTML + ":";

                        // create element with prediction time (minutes until arrival)
                        var time = document.createElement('span');
                        time.setAttribute('class', 'prd-time');
                        time.innerHTML = moment.duration(prdtm.diff(moment())).asMinutes().toFixed(1) + " min";

                        // add to page
                        var ctr = document.createElement('div');
                        ctr.setAttribute('class', 'prd-ctr');
                        ctr.appendChild(route);
                        ctr.appendChild(time);

                        $('#bus-times').append(ctr);
                    }
                }
            );
        }, 15000);

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
