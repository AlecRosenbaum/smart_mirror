
$(document).ready(function() {
    navigator.geolocation.getCurrentPosition(function(position) {
        startInterval(60*5, function() {
            loadWeather(position.coords.latitude+','+position.coords.longitude); //load weather using your lat/lng coordinates
        });
    })
  
});

function loadWeather(location, woeid) {
  $.simpleWeather({
    location: location,
    woeid: woeid,
    unit: 'f',
    success: function(weather) {
        var iconType = getIcon(weather.code);
        $("#weather").empty();
        console.log("weather-empty");

        for(var i = 0; i < Math.min(weather.forecast.length, 2); i++) {
            // day label
            var label = document.createElement("span");
            label.innerHTML = weather.forecast[i].day;
            
            var label_ctr = document.createElement("li");
            label_ctr.setAttribute('class', 'weather-center-ctr');
            label_ctr.appendChild(label)

            // icon
            var icon = document.createElement("i");
            icon.setAttribute('class', 'icon-'+weather.forecast[i].code);
            
            var icon_ctr = document.createElement("li");
            icon_ctr.setAttribute('class', 'icon-ctr');
            icon_ctr.appendChild(icon)

            // forecast high
            var high = document.createElement("span");
            high.innerHTML = weather.forecast[i].high;
            high.setAttribute('class', 'weather-high');

            // forecast divider
            var slash = document.createElement("span");
            slash.innerHTML = "/";

            // forecast low
            var low = document.createElement("span");
            low.innerHTML = weather.forecast[i].low;
            low.setAttribute('class', 'weather-low');

            // temperature container
            var temp_ctr = document.createElement("li");
            temp_ctr.setAttribute('class', 'weather-center-ctr');
            temp_ctr.appendChild(high);
            temp_ctr.appendChild(slash);
            temp_ctr.appendChild(low);

            // add to predictions
            var prediction = document.createElement("ul");
            prediction.appendChild(label_ctr);
            prediction.appendChild(icon_ctr);
            prediction.appendChild(temp_ctr);
            prediction.setAttribute('class', 'weather-prediction');
            
            var prediction_ctr = document.createElement("li");
            prediction_ctr.appendChild(prediction);
            prediction_ctr.setAttribute('class', 'weather-prediction-ctr');


            $("#weather").append(prediction_ctr);
            console.log("weather-added");

        }
    
        // html = '<table><tr><td><h2><i class="wi wi-'+iconType+'"></i> '+weather.temp+'&deg;'+weather.units.temp+'</h2>';
        // html += '<ul style="list-style-type:none"><li>'+weather.city+', '+weather.region+'</li>';
        // html += '<li class="currently">'+weather.currently+'</li>';
        // html += '<li>'+weather.temp+'&deg;F</li></td></ul>';
        // for(var i=0;i<weather.forecast.length;i++) {
        //   html += '<td><ul style="list-style-type:none"><li>'+weather.forecast[i].day+':</li>' + '<li>HI: '+weather.forecast[i].high+'</li><li>LO: '+weather.forecast[i].low+'</li></ul></td>';
        // }
        // html += '</tr></table>';
        
        // $("#weather").html(html);
    },
    error: function(error) {
      $("#weather").html('<p>'+error+'</p>');
    }
  });
}

function getIcon(code) {
    switch(code)
      {
        case "5":
        case "35":
            iconType = 'rain-mix'; 
            break;
        case "8":
        case "10":
        case "6":
        case "18":
            iconType = 'sleet'; 
            break;
        case "7":
        case "41":
        case "42":
        case "43":
        case "46":
            iconType = 'snow'; 
            break;
        case "9":
            iconType = 'sprinkle'; 
            break;
        case "11":
        case "12":
        case "40":
            iconType = 'showers';
            break;
        case "13":
        case "14":
        case "15":
        case "16":
            iconType = 'snow-wind';
            break;
        case "19":
        case "22":
        case "23":
        case "24":
            iconType = "windy";
            break;
        case "20":
            iconType = 'fog';
            break;
        case "21":
            iconType = 'day-haze';
            break;
        case "26":
        case "28":
        case "30":
            iconType = 'day-cloudy';
            break;
        case "27":
        case "29":
            iconType = 'night-cloudy';
            break;
        case "31":
            iconType = 'night-clear';
            break;
        case "32":
        case "34":
        case "36":
            iconType = 'day-sunny';
            break;
        case "33":
            iconType = 'night-clear';
            break;
        case "3": 
        case "4": 
        case "37":
        case "38":
        case "39":
        case "45":
        case "47":
            iconType = 'thunderstorm';
            break;
        default:
            iconType = 'thermometer';
            break;
      }
      return iconType;
}

function startInterval(seconds, callback) {
    callback();
    return setInterval(callback, seconds * 1000);
}
