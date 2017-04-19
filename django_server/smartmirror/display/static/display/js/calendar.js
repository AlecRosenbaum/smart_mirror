// handles loading the calendar

$(document).ready(function () {

    // var ical_url = "https://calendar.google.com/calendar/ical/alecr95%40gmail.com/private-3d95642713bfc2ad7ba4aa6c80ba6f3f/basic.ics";
    var ical_url = $('#cal-events').attr('ical');
    var today = new Date();
    today.setHours(0,0,0,0);

    $.get(ical_url, function( data ) {

        // Get the basic data out
        var jCalData = ICAL.parse(data);
        var comp = new ICAL.Component(jCalData);

        // get events in the future
        var displayed_events = [];
        var vevents = comp.getAllSubcomponents('vevent');
        for(var i = 0; i < vevents.length; i++) {
            var event = new ICAL.Event(vevents[i]); 
            if(event.startDate.toJSDate() > today) {
                displayed_events.push(event);
                // console.log(event.summary, event.startDate.toJSDate(), event.endDate.toJSDate());
            }
        }

        // sort events by date
        displayed_events.sort(function(a, b){
            var keyA = new Date(a.startDate.toJSDate()),
                keyB = new Date(b.startDate.toJSDate());
            // Compare the 2 dates
            return keyB - keyA;
        });

        // add events to list
        var cal_ul = document.createElement("ul");
        cal_ul.setAttribute('id', 'cal-ul');
        for (var i = displayed_events.length - 1; i >= Math.max(0, displayed_events.length-10); i--) {
            // console.log(displayed_events[i].summary, displayed_events[i].startDate.toJSDate(), displayed_events[i].endDate.toJSDate());
            
            // format date
            var date = displayed_events[i].startDate.toJSDate()
            var date_str = (parseInt(date.getMonth())+1) + '/' + date.getDate();

            var cal_li = document.createElement("li");
            cal_li.setAttribute('class', 'cal-li');
            cal_li.innerHTML = date_str + " " + displayed_events[i].summary;
            cal_ul.appendChild(cal_li);
        }
        $('#cal-events').append(cal_ul);
    });


});
