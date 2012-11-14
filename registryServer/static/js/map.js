window.onload = function(){

  var myLatlng = new google.maps.LatLng(42.366520, -71.077135);
  // sorry - this demo is a beta
  // there is lots of work todo
  // but I don't have enough time for eg redrawing on dragrelease right now
  var myOptions = {
    zoom: 9,
    center: myLatlng,
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    disableDefaultUI: false,
    scrollwheel: true,
    draggable: true,
    navigationControl: true,
    mapTypeControl: false,
    scaleControl: true,
    disableDoubleClickZoom: false
  };
  var map = new google.maps.Map(document.getElementById("heatmapArea"), myOptions);

  var drawingManager = new google.maps.drawing.DrawingManager({
      drawingMode: google.maps.drawing.OverlayType.MARKER,
      drawingControl: true,
      drawingControlOptions: {
      position: google.maps.ControlPosition.TOP_CENTER,
      drawingModes: [google.maps.drawing.OverlayType.POLYGON]
      },
      markerOptions: {
      icon: new google.maps.MarkerImage('http://www.example.com/icon.png')
      },
      circleOptions: {
        fillColor: '#ffff00',
        fillOpacity: .3,
        strokeWeight: 5,
        clickable: false,
        zIndex: 1,
        editable: true
      },
      polygonOptions: {
        fillColor: '#ffff00',
        fillOpacity: .3,
        strokeWeight: 5,
        clickable: true,
        zIndex: 1,
        editable: true,
        draggable: true
      }
      });
  drawingManager.setMap(map);




}





