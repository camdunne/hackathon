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
    var urls = Object.keys(values).map((key, i) => {
      return values[key].url;
    });
    var options = { 
      method: 'POST',
      body: JSON.stringify({ urls }),
     };
    fetch('http://localhost:8888/send_urls', options)
      .then(res => res.json())
      .then((data) => {

        var columnsUnsorted = Object.keys(data).map((key, i) => [ key, data[key]]);
        var sorted = [... columnsUnsorted].sort((a,b) => {
          return b[1] - a[1];
        });
        var columns = sorted.slice(0, 4);
        chart.unload();
        chart.load({
          columns,
        });
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

      ],
      type : 'pie',
      onclick: function (d, i) { console.log("onclick", d, i); },
      onmouseover: function (d, i) { console.log("onmouseover", d, i); },
      onmouseout: function (d, i) { console.log("onmouseout", d, i); }
  }
});




})();

