(function(){
  var data = {
    columns: [ 'data1', 0]
  };
var container = document.querySelector('div.container');
var search = container.querySelector('div.search');
var button = document.querySelector('button');


function clickHandler(event) {
  var from = document.querySelector('input.fromDate');
  var to = document.querySelector('input.toDate');
  var fromDate = from && from.value;
  var startTime = (fromDate) ? new Date(fromDate).getTime(): undefined;

  var toDate = to && to.value;
  var endTime = (toDate) ? new Date(toDate).getTime(): new Date().getTime();
  var url = document.querySelector('input.urlText');
  var text = url && url.value;

  var options = { 
    text,
    startTime,
    endTime,
  };

  function searchHandler(values) {
    var data = Object.keys(values).map((key, i) => {
      return values[key].url;
    });
    var options = { 
      method: 'POST',
      body: JSON.stringify(data),
     };
    fetch('http://localhost:8888/send_urls', options)
      .then(res => res.json())
      .then(({ data }) => {
        var columns = Object.keys(data).map((key, i) => [ key, data[key]]);
        var sorted = [... columns].sort((a,b) => {

        });
        chart.load({
          columns,
        })
      });
  }
  chrome.history.search(options, searchHandler);
}

button.addEventListener('click', clickHandler);


// chart

var chart = c3.generate({
  data: {
      // iris data from R
      columns: [
          // ['data1', 30],
          // ['data2', 120],
      ],
      type : 'pie',
      onclick: function (d, i) { console.log("onclick", d, i); },
      onmouseover: function (d, i) { console.log("onmouseover", d, i); },
      onmouseout: function (d, i) { console.log("onmouseout", d, i); }
  }
});

setTimeout(function () {
  chart.load({
      columns: [
          ["setosa", 0.2, 0.2, 0.2, 0.2, 0.2, 0.4, 0.3, 0.2, 0.2, 0.1, 0.2, 0.2, 0.1, 0.1, 0.2, 0.4, 0.4, 0.3, 0.3, 0.3, 0.2, 0.4, 0.2, 0.5, 0.2, 0.2, 0.4, 0.2, 0.2, 0.2, 0.2, 0.4, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.2, 0.2, 0.3, 0.3, 0.2, 0.6, 0.4, 0.3, 0.2, 0.2, 0.2, 0.2],
          ["versicolor", 1.4, 1.5, 1.5, 1.3, 1.5, 1.3, 1.6, 1.0, 1.3, 1.4, 1.0, 1.5, 1.0, 1.4, 1.3, 1.4, 1.5, 1.0, 1.5, 1.1, 1.8, 1.3, 1.5, 1.2, 1.3, 1.4, 1.4, 1.7, 1.5, 1.0, 1.1, 1.0, 1.2, 1.6, 1.5, 1.6, 1.5, 1.3, 1.3, 1.3, 1.2, 1.4, 1.2, 1.0, 1.3, 1.2, 1.3, 1.3, 1.1, 1.3],
          ["virginica", 2.5, 1.9, 2.1, 1.8, 2.2, 2.1, 1.7, 1.8, 1.8, 2.5, 2.0, 1.9, 2.1, 2.0, 2.4, 2.3, 1.8, 2.2, 2.3, 1.5, 2.3, 2.0, 2.0, 1.8, 2.1, 1.8, 1.8, 1.8, 2.1, 1.6, 1.9, 2.0, 2.2, 1.5, 1.4, 2.3, 2.4, 1.8, 1.8, 2.1, 2.4, 2.3, 1.9, 2.3, 2.5, 2.3, 1.9, 2.0, 2.3, 1.8],
      ]
  });
}, 1500);

// setTimeout(function () {
//   chart.unload({
//       ids: 'data1'
//   });
//   chart.unload({
//       ids: 'data2'
//   });
// }, 2500);


})();

