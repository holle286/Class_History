
  var iconImg;
  var pictures = ["gophers-mascot", "harshit", "ruofeng", "yang"];
  var descriptions = ["one", "two", "three", "four"];
  var index = 1;
  var geocoder;
  var marker = "Goldy.png"
  //window.addEventListener("load", function() {document.getElementById("contacts").addEventListener("load",makeMarkers)});
  function showImage() {
    iconImg.setAttribute("src", pictures[index] + ".png");
    iconImg.setAttribute("alt", descriptions[index]);
    index = (index +1)%pictures.length;
  }
  function startImg() {
    iconImg = document.getElementById("image");
    id = setInterval(function(){showImage()}, 2000);
  }
  var map;
  function initMap() {
    geocoder = new google.maps.Geocoder();
    map = new google.maps.Map(document.getElementById('map'), {
      center: {lat: 44.9727, lng: -93.23540000000003},
      zoom: 14
    });
  }
  function stopImg() {
    id = clearInterval(id);
  }
  var markers = [];
  function makeMarkers(){
    //this function is kind of a mess but basically used closures and results object to
    //pull clickable info
    var names = [];
    var addresss = [];
    var i;
    var marker;
    var infoWin = new google.maps.InfoWindow();
    for(i = 1; i < document.getElementById("contacts").rows.length; i+=1) {
      var address = document.getElementById("contacts").rows[i].cells[2].innerHTML;;
      infoWin.setContent(address);
      var ogName = document.getElementById("contacts").rows[i].cells[0].innerHTML;
      var index = ogName.indexOf("<"); //lose the img stuff on the names
      var name = ogName.slice(0,index);
      names.push(name);
      geocoder.geocode({ 'address': address},
      (function(name){ //first closure to get names
        return function(results,status) {
        marker = new google.maps.Marker({
          map: map,
          icon: "Goldy1.png",
          position: results[0].geometry.location,
          title: results[0].formatted_address //readable address
        });
        markers.push(marker);
        //make each marker clickable,  more closure
        marker.addListener('click',(function(name) {
          return function() {
            infoWin.setContent(name + "<br>" + results[0].formatted_address);
            infoWin.open(map, this);
          }
        }) (name));
      }
    })(names[i -1]));
    }
  }
  function startSearch() {
    var type = document.getElementById("searchType").value;
    if(type == "other") {
      type = document.getElementById("other").value;
    }
    var range = document.getElementById("distance").value;
    var request = {
      keyword : type,
      fields: ['name','geometry'],
      location:{lat: 44.9727, lng: -93.23540000000003},
      radius: parseInt(range),
      locationBias : {
      radius: parseInt(range),
      center: {lat: 44.9727, lng: -93.23540000000003}}
  };
  clearOverlays();
    var service = new google.maps.places.PlacesService(map);

    service.nearbySearch(request, function(results, status) {
      if (status === google.maps.places.PlacesServiceStatus.OK) {
        for (var i = 0; i < results.length; i++) {
          createMarker(results[i]);
        }
        map.setCenter(results[0].geometry.location);
      }
    });
  }
  function clearOverlays() {
    for (var i = 0; i < markers.length; i++ ) {
      markers[i].setMap(null);
    }
    markers.length = 0;
  }
  function createMarker(place) {
    var marker = new google.maps.Marker({
      map: map,
      position: place.geometry.location,
      title: place.name
    });
    var infoWin = new google.maps.InfoWindow();
    google.maps.event.addListener(marker, 'click', function() {
      infoWin.setContent(place.name);
      infoWin.open(map, this);
    });
  }
  function getPos() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {
        var pos = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };
        console.log(pos);
        return pos;
      });
    }
  }
var infoWindow
  function handleLocationError(browserHasGeolocation, infoWindow, pos) {
    infoWindow.setPosition(pos);
    infoWindow.setContent(browserHasGeolocation ?
                          'Error: The Geolocation service failed.' :
                          'Error: Your browser doesn\'t support geolocation.');
    infoWindow.open(map);
  }

  function getDirections() {
    infoWindow = new google.maps.InfoWindow;
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position) {
        var pos = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };
        var destination = document.getElementById("destination").value;
        var modes = document.getElementsByName("transportation");
        var checkedMode;
        for(var f =0; f < modes.length; f+=1) {
          if(modes[f].checked){
            checkedMode = modes[f].value;
          }
        }
        var request = {
          origin: pos,
          destination: destination,
          travelMode: checkedMode
        }
        clearOverlays();
        //console.log("pos");
        //infoWindow.setPosition(pos);
        //infoWindow.setContent('Location found.');
        //infoWindow.open(map);
        //map.setCenter(pos);

        var directionsService = new google.maps.DirectionsService();
        var directionsRenderer = new google.maps.DirectionsRenderer();
        directionsRenderer.setMap(map);

        directionsService.route({
          origin: pos,
          destination: destination,
          travelMode: checkedMode
        }, function(result, status) {
          if (status == 'OK') {console.log("HERE");
            directionsRenderer.setDirections(result);
            directionsRenderer.setPanel(document.getElementById('left-panel'));
            var control = document.getElementById('floating-panel');
                    control.style.display = 'block';
                    map.controls[google.maps.ControlPosition.TOP_CENTER].push(control);
          }
        });
      }, function() {
        handleLocationError(true, infoWindow, map.getCenter());
      });
    } else {
      // Browser doesn't support Geolocation
      handleLocationError(false, infoWindow, map.getCenter());
    }
}
function displayDirections() {


}
