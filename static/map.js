function initMap() {
  const berlin = new google.maps.LatLng(52.51807415366815, 13.403719548295928)

  const map = new google.maps.Map(document.getElementById("map"), {
    center: berlin,
    zoom: 12,
  })

  const infoWindow = new google.maps.InfoWindow()
  venues.forEach(venue => initMarker(venue, map, infoWindow))
}

function initMarker(venue, map, infoWindow) {
  const marker = new google.maps.Marker({
    map: map,
    position: venue.location
  })

  marker.addListener('click', () => {
    infoWindow.setContent(
      `<div class='venue-name'>${venue.name}</div>
      <div class="venue-address">${venue.address}</div>`)

    infoWindow.open({
      anchor: marker,
      map,
      shouldFocus: false,
    })
  })
}