import requests
import json

def cg_historical_api(id):
    api = "https://api.coingecko.com/api/v3/coins/"+id+"/market_chart?vs_currency=usd&days=max"
    try:
        data = requests.get(api,timeout=10).json()
        return data
    except requests.exceptions.RequestException:
        return False
    except (ValueError):
        return False
        
def crypto_chart(id):
    data = cg_historical_api(id)
    if data:
        try:
            price = json.dumps(data['prices'])
            volume = json.dumps(data['total_volumes'])
            output = chart(price,volume)
        except (IndexError, KeyError, TypeError, ValueError):
            output = "No chart data to display."
    else:
        output = "No chart data to display."
    return output

def chart(price,volume):
    output = '''<script>$(function() {
  Highcharts.setOptions({
    lang: {
      thousandsSep: ","
    },
  });
  var chart = new Highcharts.StockChart({

    chart: {
      events: {
        load: function() {
          Highcharts.fireEvent(
            this.xAxis[0],
            'afterSetExtremes', {
              redraw: true
            }
          );
        }
      },
      backgroundColor: null,
      fontFamily: 'sans-serif',
      zoomType: 'x',
      type: "area",
      margin: [0, 0, 0, 0],
      spacingTop: 0,
      marginTop: 0,
      borderWidth: 0,
      spacing: 0,
      renderTo: 'chart'
    },
    scrollbar: {
      enabled: false
    },
    navigator: {
      maskFill: 'rgba(0, 32, 68, 0.3)',
    },

    credits: {
        position: {
            verticalAlign: 'top',
            x: 0,
            y: 10,
        }
    },

    rangeSelector: {
      buttonTheme: { // styles for the buttons
        fill: 'none',
        stroke: 'none',
        'stroke-width': 0,
        r: 7,
        style: {
          color: '#58A6FF',
          fontWeight: 'bold'
        },
        states: {
          hover: {
            fill: null
          },
          select: {
            fill: '#58A6FF',
            style: {
              color: 'white'
            }
          }
        }
      },

      selected: 4,
      inputEnabled: false,
    },

    yAxis: [{
            gridLineWidth: .3,
            gridLineColor: 'rgba(211, 212, 222, 0.35)',
            floor: 0,
            maxPadding: 0,
            labels: {
                align: 'right',
                x: -5
            }
        }, {
            gridLineWidth: 0,
            floor: 0,
            minPadding: 0,
            top: '80%',
            height: '20%',
						labels: {
            enabled: false
            }
        }],
 tooltip: {
        style: {
        color: 'white'
        },
        shared: true,
        backgroundColor: 'rgba(22, 27, 34, 0.5)',
        split: false,
        crossharis: true,
        shadow: false,
        padding: 5,
        borderWidth: 0,
        borderRadius: 4,
        snap: "1/2"
        },

    xAxis: {
      crosshair: {
        width: 0.5,
        color: '#58A6FF'
      },
      events: {
        afterSetExtremes: function(e) {
          var points = e.target.series[0].points,
            chart = e.target.chart;

          var ky = [],
            i = 0,
            series_color,
            kx = [];
          for (i = 0; i < points.length; i++) {
            var xypoint = points[i];
            kx.push(xypoint.x);
            ky.push(xypoint.y);
          }

          var lr = linear(kx, ky);
          if (lr[0][1] < lr[1][1]) {
            series_color = 'rgba(0,200,83,0.5)'
          } else {
            series_color = 'rgba(255,0,0,0.5)'
          }
          chart.addSeries({
            name: 'Regression Line',
            marker: {
              enabled: false
            },
            lineWidth: 2,
            fillOpacity: 0,
            yAxis: 0,
            data: lr,
            color: series_color,
            dashStyle: 'shortdash',
            id: 'trend'
          }, e.redraw ? true : false);
          while (chart.series.length > 4) {
            chart.get('trend').remove();
          }
        }

      }
    },

    plotOptions: {
            series: {

                lineWidth: 2,
                states: {
                hover: {
                enabled: false,
                }
                },
                dataGrouping: {
                enabled: false,
                },
                area: {

                }

                }
                },
    series: [{
      fillOpacity: .2,
            color: "#58A6FF",
            name: 'Price',
            shadow: {
            color: '#002044',
            yAxis: 0,
        },
      data: '''+price + '''
    }, {
      fillOpacity: .5,
            name: 'Volume',
            step: true,
            color: '#d0d0d1',
            lineWidth: 0,
            showEmpty: false,
            offset: 2,
      			yAxis: 1,
      data: '''+volume + '''
    }]
  });
});
</script>
                        '''
    return output

crypto_chart("bitcoin")
