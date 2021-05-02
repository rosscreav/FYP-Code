$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

    socket.on('update', function(data) {
    // Global parameters:
      // do not resize the chart canvas when its container does (keep at 600x400px)
      Chart.defaults.global.responsive = false;

      // timeFormat = 'hh:mm:ss'
      function timeConverter(UNIX_timestamp){
        var a = new Date(UNIX_timestamp * 1000);
        var hour = a.getHours();
        var min = a.getMinutes();
        var sec = a.getSeconds();
        var time = hour + ':' + min + ':' + sec ;
        return time;
      }
      //Extract values from input
      var values = data.data;
      var labels = data.labels;

      labels.forEach(function(part, index) {
        this[index] = timeConverter(part);
      }, labels);
      var legend = data.legend;

      console.log(labels);
      // define the chart data
      var chartData = {
        labels : labels,
        datasets : [{
            label: legend,
            fill: true,
            lineTension: 0.1,
            backgroundColor: "rgba(192,192,192,0)",
            borderColor: "rgba(73, 179, 216,1)",
            borderCapStyle: 'butt',
            borderDash: [],
            borderDashOffset: 0.0,
            borderJoinStyle: 'miter',
            pointBorderColor: "rgba(73, 179, 216,1)",
            pointBackgroundColor: "#fff",
            pointBorderWidth: 1,
            pointHoverRadius: 5,
            pointHoverBackgroundColor: "rgba(73, 179, 216,1)",
            pointHoverBorderColor: "rgba(255,255,255,1)",
            pointHoverBorderWidth: 2,
            pointRadius: 1,
            pointHitRadius: 10,
            data : values,
            spanGaps: false
        }]
      };

      // get chart canvas
      var holder = document.getElementById("myChart");
      var ctx = document.getElementById("myChart").getContext("2d");

      // create a callback function for updating the caption
      var original = Chart.defaults.global.legend.onClick;
      Chart.defaults.global.legend.onClick = function(e, legendItem) {
        update_caption(legendItem);
        original.call(this, e, legendItem);
      };

      // create the chart using the chart canvas

      var myChart = new Chart(ctx, {
        type: 'line',
        data: chartData,
        options: {
          tooltips: {
            enabled: true,
            mode: 'single',
            callbacks: {
              label: function(tooltipItems, data) {
                       firstPointCtx = "First Point Selected: (2:20PM, 72.3 cm)";
                       return tooltipItems.yLabel + ' cm';
                     }
            }
          },
          animation: false,
        }
      });

      // get the text element below the chart
      var pointSelected = document.getElementById("pointSelected");

      // create a callback function for updating the selected index on the chart
      holder.onclick = function(evt){
        var activePoint = myChart.getElementAtEvent(evt);
        console.log(activePoint);
        console.log('x:' + activePoint[0]._view.x);
        console.log('maxWidth: ' + activePoint[0]._xScale.maxWidth);
        console.log('y: ' + activePoint[0]._view.y);
        console.log('index: ' + activePoint[0]._index);
        pointSelected.innerHTML = 'Point selected... index: ' + activePoint[0]._index;
      };
    });

     socket.on('ultra_left', function(value) {
        document.getElementById('ultra_left').innerHTML  = value;
     });

     socket.on('ultra_right', function(value) {
        document.getElementById('ultra_right').innerHTML  = value;
     });

     socket.on('lidar_value', function(value) {
        document.getElementById('lidar').innerHTML  = value;
     });

    });

