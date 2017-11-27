queue()
    .defer(d3.json, "/data")
.await(makeGraphs);


function makeGraphs(error, recordsJson){
  var records=recordsJson;
  //console.log(records);
  var dateFormat = d3.time.format("%Y-%m-%d");
  records.forEach(function(d) {
    d["psdate"] = dateFormat.parse(d["psdate"]);
});

  var data=crossfilter(records);
  var dateDim = data.dimension(function(d) { return d["psdate"]; });
  var numRecordsByDate = dateDim.group();
  var psDim=data.dimension(function(d){ return d["pstation"]});
  var disDim=data.dimension(function(d){ return d["district"]});
  var paharDim=data.dimension(function(d){return d["pahar"]});
  var offenceDim=data.dimension(function(d){return d["group_charge"]});
  var timeDim=data.dimension(function(d){return d["hour"]});
  var allDim = data.dimension(function(d) {return d;});
  //var dateDim=data.dimension(function(d){return d["psdate"]});
  var minDate = dateDim.bottom(1)[0]["psdate"];
  var maxDate = dateDim.top(1)[0]["psdate"];

    console.log(minDate);
    console.log(maxDate);
  //var numRecordsByDate=dateDim.group();
  var psGroup=psDim.group();
  var offenceGroup=offenceDim.group();


   var psGroup2= getTops(psGroup);
   var offenceGroup2= getTops(offenceGroup);

    function getTops(psGroup) {
    return {
        all: function () {
            return psGroup.top(Infinity).filter(function(d) {
            //console.log(d.value)
            return d.value > 0; });
        }
    };
}


   console.log(psGroup2);




  var disGroup=disDim.group();
  var paharGroup=paharDim.group();
  var all=data.groupAll();
  var offenceGroup=offenceDim.group();
  var timeGroup=timeDim.group();


  var numberRecordsND=dc.numberDisplay("#number-records");
  //var timeChart=dc.barChart("#time-chart");
  var pstationChart=dc.rowChart("#pstation-chart");
  var disChart=dc.rowChart("#dis-chart");


  var paharChart=dc.pieChart("#pahar-chart");
  var dateChart = dc.lineChart("#date-chart");
  var offenceChart=dc.rowChart('#offence-chart');
  var timeChart = dc.lineChart("#time-chart");

  numberRecordsND
    .formatNumber(d3.format("d"))
    .valueAccessor(function(d){return d; })
    .group(all);

  pstationChart
    .width(700)
    .height(1000)
    .dimension(psDim)
    .group(psGroup2)
    .elasticX(true)
    .xAxis().ticks(4);



  disChart
    .width(700)
    .height(1000)
    .dimension(disDim)
    .group(disGroup)
    .elasticX(true)
    .xAxis().ticks(10);


  paharChart
    .width(250)
    .height(300)
    .innerRadius(10)
    .dimension(paharDim)
    .group(paharGroup);

  dateChart
    .width(650)
    .height(140)
    .margins({top: 10, right: 50, bottom: 20, left: 20})
    .dimension(dateDim)
    .group(numRecordsByDate)
    .x(d3.time.scale().domain([minDate, maxDate]))
    .elasticY(true)
    .xAxis().ticks(4);

  offenceChart
    .width(700)
    .height(1000)
    .dimension(offenceDim)
    .group(offenceGroup2)
    .elasticX(true)
    .xAxis().ticks(4);

  timeChart.width(650)
    .height(100)
    .dimension(timeDim)
    .group(timeGroup)
	.elasticY(true)
    .x(d3.scale.linear().domain([0,24]))
    .xAxis();

      var map=L.map('map');
var cont;
var markbool;
map.on("overlayadd ",function(ev){if(ev.name=="Markers"){
markbool=true;
}
});
map.on("overlayremove ",function(ev){if(ev.name=="Markers"){
markbool=false;
}
});

  var drawMap=function(){

   var geoData = [];
    _.each(allDim.top(Infinity), function (d) {
        geoData.push([d["Lat"], d["Long"], "Offence:"+d["group_charge"]+"<br>Date:"+d["psdate"]+"<br>Time:"+d["timefrom"]+"<br>Police Station:"+d["pstation"]+"<br><a href="+d["link"]+">Fir Link</a>" ]);
    });
    var geoData2 = [];
    _.each(allDim.top(Infinity), function (d) {
        geoData2.push([d["Lat"], d["Long"], 1 ]);
    });
    map.setView([geoData[0][0],geoData[0][1]],11);
    mapLink='<a href="http://openstreetmap.org">OpenStreetMap</a>';
    //map.worldCopyJump(true);
    L.tileLayer(
      'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
        attribution: '&copy; ' + mapLink + ' Contributors',
        maxZoom: 15,

      }
    ).addTo(map);

    //HeatMap

    var heat = L.heatLayer(geoData2,{
        radius: 10,
        blur: 20,
        maxZoom: 1,
    });
    map.addLayer(heat);

    markers=[];

    for (var i = 0; i < geoData.length; i++) {
			markers.push(new L.marker([geoData[i][0],geoData[i][1]])
			    .bindPopup(geoData[i][2]))
		}

	var markerLayer = L.layerGroup(markers);

	if(markbool==true){
	map.addLayer(markerLayer);}

	var overlayMaps = {
    "Heat": heat,
    "Markers":markerLayer};


    cont=L.control.layers(null, overlayMaps).addTo(map);



  };
  drawMap();

  dcCharts = [disChart,pstationChart,paharChart,offenceChart,timeChart];

  _.each(dcCharts, function (dcChart) {
      dcChart.on("filtered", function (chart, filter) {
      map.removeControl(cont);
          map.eachLayer(function (layer) {
            map.removeLayer(layer)
          });

      drawMap();
      });
  });

  dc.renderAll();



};
