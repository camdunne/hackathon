(function(){

var container = window.document.getElementsByClassName('container');
var button = document.querySelector('button');
console.log('container', container)
button.addEventListener('click', clickHandler);

function clickHandler() {
  var options = { 
    text: ""
  };

  chrome.history.search(options, function(values){
    console.log('values', values);
    
  });
}

})();

