function generateTable(ksaData) {

  var col = [];
  for (var i = 0; i < ksaData.length; i++) {
      for (var key in ksaData[i]) {
          if (col.indexOf(key) === -1) {
              col.push(key);
          }
      }
  }

  var tr = table.insertRow(-1);

  // Create table headers
  for (var i = 0; i < col.length; i++) {
      var th = document.createElement("th");
      th.innerHTML = col[i];
      tr.appendChild(th);
  }

  // Add table rows
    for (var i = 0; i < ksaData.length; i++) {
      tr = table.insertRow(-1);

      for (var j = 0; j < col.length; j++) {
          var tabCell = tr.insertCell(-1);
          tabCell.innerHTML = ksaData[i][col[j]];
      }
  }

  // Add the data to the table container
  var divContainer = document.getElementById("ksaTable");
  divContainer.innerHTML = "";
  divContainer.appendChild(table);
}

var table = document.createElement("table");
table.classList.add('table');
table.classList.add('table-striped');
table.classList.add('table-bordered');
table.classList.add('table-hover');
table.classList.add('table-responsive');

d3.json('/api/data/ksa').then(function(ksaData){
  generateTable(ksaData);
});
