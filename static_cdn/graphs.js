

$(function() {

		var data = [];
			totalPoints = 300;
        var currentTX;
        var current;

function GetData() {
     $.ajax({
       url:"/rates/",
       dataType: 'json',
       method: "GET",
       data: {IP: new URLSearchParams(window.location.search).get("IP")},
       beforeSend: function(data, settings) {},
       success: function(jdata){
                
       if (typeof(last) == 'undefined') {
           last = jdata.uptime
           }
       current = jdata.uptime - last 
       if (typeof(lastTX) == 'undefined')
            { lastTX = jdata.TX }
       currentTX = jdata.TX //- lastTX
    
}}); //end of ajax call

    if (data.length > 0)
        data = data.slice(1);
    while (data.length < totalPoints) {
        data.push(currentTX);}
        
    var res = [];
    for (var i = 0; i < data.length; ++i) {
        res.push([current, data[i]])
    }
    console.log(res)
	return res;
}

		var updateInterval = 30;
		$("#updateInterval").val(updateInterval).change(function () {
			var v = $(this).val();
			if (v && !isNaN(+v)) {
				updateInterval = +v;
				if (updateInterval < 1) {
					updateInterval = 1;
				} else if (updateInterval > 2000) {
					updateInterval = 2000;
				}
				$(this).val("" + updateInterval);
			}
		});

		var plot = $.plot("#placeholder", [ GetData() ], {
			series: {
				shadowSize: 0,	// Drawing is faster without shadows
				lines: {
					show:true,
					linewidth:1.2,
					fill:true
				}
			},
			yaxis: {
				min: 0,
				max: 100
			},
			xaxis: {
				show: false
			}
		});

		function update() {

			plot.setData([GetData()]);

			// Since the axes don't change, we don't need to call plot.setupGrid()

			plot.draw();
			setTimeout(update, updateInterval);
		}

		update();

		// Add the Flot version string to the footer

		$("#footer").prepend("Flot " + $.plot.version + " &ndash; ");
	});
