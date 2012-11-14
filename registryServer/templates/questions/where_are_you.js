{% extends 'questions/collision_detection.js' %}



{% block %}
setInterval(function(){GetLocation();},10000);
var notified = false;
function GetLocation() {

    var loc = android.getLocation();
    var loc_json = jQuery.parseJSON(loc);
    var latlng = new google.maps.LatLng(loc_json.lat, loc_json.lon);

    if(!notified){
            if(shape.containsLatLng(latlng))
                {
                        android.notify('Welcome to Media Lab', 'http://media.mit.edu');
                        notified = true;
                }
        }
}

{% endblock %}
