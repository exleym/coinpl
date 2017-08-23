/**
 * Created by exley on 8/22/17.
 */
function line(data, container, title, subtitle, yLabel) {

  var priceData = [];
  for (d in data) {
      priceData.push([data[d]["timestamp"], data[d]["bid_price"]]);
  }

  Highcharts.chart(
  container,
  {
    title: { text: title,  align: 'left' },
    subtitle: { text: subtitle, align: 'left' },
    yAxis: { title: { text: yLabel, align: 'high' } },
    xAxis: {
        type: 'datetime',
        dateTimeLabelFormats: {
            day: '%e of %b'
        }
    },
    legend: false,
    series: [{
      name: 'Bid Price',
      data: priceData,
      color: "#6600ff"
    }]
  }
)}
