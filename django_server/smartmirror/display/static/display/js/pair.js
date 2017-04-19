// google api client id 922831018117-riq3s1ra0fc2gnqc89nmbo9ua5bv2qgp.apps.googleusercontent.com
$( document ).ready( function () {
    var strLength= $('#short_id').val().length;
    $('#short_id')[0].setSelectionRange(strLength, strLength)

    // globals
    var touching = false;
    var input = true;
    var hovering = false;
    var swipe_stabilizer_timeout = null;
    var parsed_text = "";

    // leap motion controller
    var stageWidth = document.getElementById('textInput').offsetWidth;
    var stageHeight = document.getElementById('textInput').offsetHeight;

    var leap = new Leap.Controller({
        scheme: 'ws:',
        port: 6437,
    });

    var idx_finger = null;
    var last_x = last_y = last_time = 0;
    leap.on("frame", function(frame) {
        // update finger tip display with data from latest frame
        var tipPointer = 0;
        var drawArea = document.getElementById('myscript-input-area');
        if (frame.valid) {
            if (input == false && frame.fingers.length == 0 || hovering == true && input == true) {
                document.querySelector('myscript-text-web').clear();
                hovering = false;
            }
            if (swipe_stabilizer_timeout != null) {
                return;
            }
            for (var p = 0; p < frame.fingers.length; p++) {
                // if it's an index finger
                if (frame.fingers[p].type == 1) {
                    var pointable = idx_finger = frame.fingers[p];
                    var pos = frame.interactionBox.normalizePoint(pointable.tipPosition, true);
                    var x = pos[0] * stageWidth;
                    var y = stageHeight - pos[1] * stageHeight;

                    if (pointable.touchZone == "touching" || pointable.touchZone == "hovering") {
                        console.log(frame);
                        // if not already touching, simulate mouse click event
                        if (touching == false) {
                            // mouse click event
                            // console.log("pointerdown", x, y)
                            drawArea.dispatchEvent(new PointerEvent( 'pointerdown', {
                                pointerId: 1,
                                clientX: x,
                                clientY: y,
                                timeStamp: + new Date()
                            }));
                            touching = true;
                        }
                        // simulate pointer movement
                        // console.log("pointermove", x, y)
                        drawArea.dispatchEvent(new PointerEvent('pointermove', {
                            pointerId: 1,
                            clientX: x,
                            clientY: y,
                            timeStamp: + new Date()
                        }));

                        // determine of hoveing in the same place
                        if (last_time == 0 || Math.sqrt((x-last_x)^2+(y-last_y)^2) > 20) {
                            last_x = x;
                            last_y = y;
                            last_time = frame.timestamp;
                        }

                        // if hovering in the same place for 1 sec, finish and put into textbox
                        if (frame.timestamp - last_time > 2000000) {
                            drawArea.dispatchEvent(new PointerEvent("pointerup", {
                                pointerId: 1,
                                clientX: x,
                                clientY: y,
                                timeStamp: + new Date()
                            }));
                            touching = false;
                            last_time = frame.timestamp + 1000000;

                            var parse_text_func = function() {
                                parsed_text = document.querySelector('myscript-text-web').firstcandidate;
                                if (typeof parsed_text == "undefined"){
                                    setTimeout(parse_text_func, 500);
                                    return;
                                }

                                $('#short_id').val($('#short_id').val() + parsed_text);

                                // make sure drawing is handled
                                document.getElementById('myscript-input-area').dispatchEvent(new PointerEvent("pointerleave", {
                                    pointerId: 1
                                }));

                                document.querySelector('myscript-text-web').clear();
                            }
                            setTimeout(parse_text_func, 500);
                        }
                    } else {
                        // pointer up event, no longer touching
                        if (touching == true) {
                            // console.log("pointerup", x, y)
                            drawArea.dispatchEvent(new PointerEvent("pointerup", {
                                pointerId: 1,
                                clientX: x,
                                clientY: y,
                                timeStamp: + new Date()
                            }));
                        }
                        touching = false;
                    }
                }
            }
        }
    });

    var cclkwise_id = cclkwise_timeout = null;
    leap.on("gesture", function(gesture) {
        if( touching && typeof document.querySelector('myscript-text-web').firstcandidate == "undefined") {
            return;
        }

        // swipe means 
        // if (gesture.type == "swipe") {
        //     // console.log(gesture);
        //     if (swipe_stabilizer_timeout != null) {
        //         clearTimeout(swipe_stabilizer_timeout)
        //     } else if (typeof(document.querySelector('myscript-text-web').firstcandidate) != "undefined") {
        //         parsed_text = document.querySelector('myscript-text-web').firstcandidate;
        //     }

        //     swipe_stabilizer_timeout = setTimeout(function() {
        //         console.log("swipe registered");
                
        //         // put parsed text into textbox
        //         // var parsed_text = document.querySelector('myscript-text-web').firstcandidate;
        //         if (parsed_text == "" || typeof parsed_text == "undefined") {
        //             parsed_text = document.querySelector('myscript-text-web').firstcandidate;
        //         }
        //         $('#short_id').val($('#short_id').val() + parsed_text);

        //         // make sure drawing is handled
        //         document.getElementById('myscript-input-area').dispatchEvent(new PointerEvent("pointerleave", {
        //             pointerId: 1
        //         }));

        //         document.querySelector('myscript-text-web').clear();
        //         swipe_stabilizer_timeout = null;
        //         parsed_text = "";
        //     }, 500);
        // }

        if (gesture.type == "circle") {
            if (gesture.normal[2] * idx_finger.direction[2] > 0) {
                // clockwise for submit
                console.log("clockwise");
                if ($("#short_id").val().length == 5) {
                    $("#input-form").submit();
                    $('#centering-ctr').html("Loading...");
                }
            } else {
                // counterclockwise for delete
                if (gesture.id != cclkwise_id) {
                    console.log("counter-clockwise");

                    // delete last character from input
                    $("#short_id").val(
                        function(index, value){
                            return value.substr(0, value.length - 1);
                    })
                }
                cclkwise_id = gesture.id
                if (cclkwise_timeout != null) {
                    clearTimeout(cclkwise_timeout);
                }
                cclkwise_timeout = setTimeout(function() {
                    cclkwise_id = null;
                    document.querySelector('myscript-text-web').clear();
                }, 500);
            }

        }


    })

    var leap_connect_interval = startInterval(.5, function(){
        if(!leap.connected()){
            leap.connect();
        }
    })

});

function startInterval(seconds, callback) {
    callback();
    return setInterval(callback, seconds * 1000);
}

function isDescendant(parent, child) {
    if (child == null){
        return false;
    }
    var node = child.parentNode;
    while (node != null) {
        if (node == parent) {
            return true;
        }
        node = node.parentNode;
    }
    return false;
}
