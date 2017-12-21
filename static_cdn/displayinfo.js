

   $(function() {
    startRefresh();
    });

function startRefresh() {
      setTimeout(startRefresh,10000);
      foo();
    };

    function foo() {
      
      var data = $.ajax(
        {url:"/status/",
        type: "GET",
        data: {IP: new URLSearchParams(window.location.search).get("IP")},
        beforeSend: function(data, settings) {
        },
        success: function(data){

        document.getElementById("distance").innerHTML = data.distance + ' feet';
        document.getElementById("signal").innerHTML = data.signal +' (Need to keep this below -70)';
        document.getElementById("hostname").innerHTML = data.hostname;
      }});
    }

