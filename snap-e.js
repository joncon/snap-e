$(function(){
  var mapOptions = {
    zoom: 7,
    center: new google.maps.LatLng(44.9, -120.95),
    mapTypeId: google.maps.MapTypeId.TERRAIN,
    scaleControl: true,
    draggable: true,
    // scrollwheel: false,
    // navigationControlOptions: {
    //   style: google.maps.NavigationControlStyle.SMALL
    // },
    mapTypeControl: false,
    streetViewControl: false
  };
  var mapCanvas = document.getElementById('map');
  var map = new google.maps.Map(mapCanvas, mapOptions);
  
  var count=0;
  var arr=[];
  var url="http://assets.pnsn.org/snap-e/pnsn_station_latencies.json"
  $.getJSON(url, function(json) { //requests each url
    count += 1;
    $.each(json, function(j, response) {
      arr.push(response);
    });
    
    $.each(arr,function(i, sta){
      console.log(sta);
      var latency= sta.latency || -1;
      latency= Math.min(latency, 100)
      var color; 
      if(latency < 4){
        color="green";
      }else if(latency < 10){
        color="blue";
      }else if(latency < 30){
        color="yellow";
      }else{
        color="red";
      }
      var path;
      if(latency < 0){
        path="alpha-icons-no-color/letter_u.png";
      }else{
        path="numeric-icons-" + color + "/number_" + latency + ".png";
      }
       path = "http://assets.pnsn.org/snap-e/images/" + path; 
       var image = {
           url: path,
           scaledSize: new google.maps.Size(26, 26),
           origin: new google.maps.Point(0, 0),
           anchor: new google.maps.Point(0, 24)
      };
      var marker = new google.maps.Marker({
        position: {lat: sta.lat, lng: sta.lon},
        map: map,
        icon: image
      });
      var contentString="<div id='content'> <h2> some text</h2></div";
      var infowindow = new google.maps.InfoWindow({
          content: contentString
      });
      marker.addListener('click', function() {
          infowindow.open(map, marker);
        });
    
    });
  });
});