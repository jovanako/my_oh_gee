let map;

function initMap() {
  const berlin = new google.maps.LatLng(52.51807415366815, 13.403719548295928)

  map = new google.maps.Map(document.getElementById("map"), {
    center: berlin,
    zoom: 12,
  });
}