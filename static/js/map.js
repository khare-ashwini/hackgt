/* 
  Javascript required for the map.html to work.
*/

  $(document).ready(function() {
    var temp_a=['London', 'Washington'];
    var temp_d=['Capital of Great Britain', 'Capital of the United States'];
  
    var map;
    var overlay;
    var layer;
    var bounds;
  
  
    var n={}
    function initialize() {
      options  = { zoom: 2, mapTypeId: google.maps.MapTypeId.TERRAIN }
      map      = new google.maps.Map(d3.select("#map_canvas").node(),options);
      bounds   = new google.maps.LatLngBounds();
      overlay  = new google.maps.OverlayView();
      overlay.onAdd = function() {
        layer = d3.select(this.getPanes().overlayMouseTarget).append("div").attr("class", "stations");
      }
    }
  
  
  
  
  
    function add(inp) {
      data=JSON.parse(inp)
      console.log(data)
  
      overlay.draw = function() {
        var projection = this.getProjection(), padding = 10;
        var marker = layer.selectAll("svg").data(d3.entries(data)).each(transform)
                          .enter().append("svg:svg")
                          .each(transform)
                          .attr("class", "marker");
  
        // Add a circle.
        marker.append("svg:circle")
                          .attr("r", 4.5)
                          .attr("cx", padding)
                          .attr("cy", padding)
                          .on("click",expandNode)
                          .on("dblclick",contractNode)
                          .on("mouseover",function(d){ console.log(d.key); })
                          //.on("mouseout",contractNode);
  
        // Add a label.
        marker.append("svg:text")
                          .attr("x", padding + 7)
                          .attr("y", padding)
                          .attr("dy", ".31em")
                          .attr("class","marker_text")
                          .text(function(d) {return d.key; });
  
        function transform(d) {
          d = new google.maps.LatLng(d.value[1], d.value[0]);
          d = projection.fromLatLngToDivPixel(d);
          return d3.select(this).style("left", (d.x - padding) + "px").style("top", (d.y - padding) + "px");
        }
        // provides node animation for mouseover
        function expandNode() {
          d3.select(this).transition()
                          .duration(100)
                          .attr("r",7)
        };
  
  
        // provides node animation for mouseout
        function contractNode(){
          d3.select(this).transition()
                          .duration(100)
                          .attr("r",4.5)
        };
      };
  
      overlay.setMap(map);
    }
  
  
    function codeAddress(desc,address,i,temp_res) { 
      var sAddress    = address
      var desc        = desc
  
      // When using a local server for caching, you can't use Google Geocoder
      // In this example I've just attached filed, but when you have your own geocoder server-side change it to 
      // something like $.get('/geocoder/'+address, function(results) {
      $.get(address, function(results) {
        console.log(results)
        results=JSON.parse(results)
  
        // Extend the bounds so that the map fits the markers
        var myLatLng = new google.maps.LatLng(results[0].latitude, results[0].longitude);
        bounds.extend(myLatLng)
  
        // I'm sure this is a death sin format, but it works.
        // Create some temporary variables to pass on to the next iteration
        temp_res+=',"'+desc+'":'+'['+results[0].longitude+','+results[0].latitude+',"'+desc+'",[]]'
        desc=temp_d[i]
        addr=temp_a[i]
        // Make the callback, and make sure to include your results
        // These data doesn't exist on execution time
        c(desc,addr,i,temp_res)
      });   
    }
  
    function c(desc,addr,i,temp_res) {
      if (i>=temp_a.length) { console.log('Completed lookups'); add('{'+temp_res.substring(1)+'}'); map.fitBounds(bounds); return; }                
      i+=1
      codeAddress(desc,addr,i,temp_res)
    }
    
    // Make the markers glow
    var glow = $('.stations');
    setInterval(function(){
      glow.toggleClass('glow');
    }, 1000);
  
    initialize();    
    c(temp_d[0],temp_a[0],0,'')
  });