//note: honestly the ids don't seem to matter, they're just for organizational purposes
//the ids don't matter since we access the table's rows and cols by row,col coordinates
//the tableclass is important, though, because we access that specific table by the table class name
function tableCreation(tableclass)
//creates a table with user-defined class name with 4 table headers
//note: tableclass must be in quotes
{
  var body = document.body;
  tablee = document.createElement("table");
  tablee.style.width = "100%";
  tablee.style.border = "1px solid white";
  tablee.setAttribute('class', tableclass);

  var table_body = document.createElement("tbody");

  var table_header_1 = document.createElement('th');
  table_header_1.setAttribute('id', 'task_name');
  table_header_1.innerHTML = "Task Name";
  table_header_1.style.border = "1px solid white";
  table_body.appendChild(table_header_1);

  var table_header_2 = document.createElement('th');
  table_header_2.setAttribute('id', 'foreman_name');
  table_header_2.innerHTML = "Foreman Name";
  table_header_2.style.border = "1px solid white";
  table_body.appendChild(table_header_2);

  var table_header_3 = document.createElement('th');
  table_header_3.setAttribute('id', 'status');
  table_header_3.innerHTML = "Task Status";
  table_header_3.style.border = "1px solid white";
  table_body.appendChild(table_header_3);

  var table_header_4 = document.createElement('th');
  table_header_4.setAttribute('id', 'due_date');
  table_header_4.innerHTML = "Due Date";
  table_header_4.style.border = "1px solid white";
  table_body.appendChild(table_header_4);

  tablee.appendChild(table_body);
  body.appendChild(tablee);
  console.log("Created new table with class name " + tableclass);
}

function tableRowCreate(tableclass, rowid)
//creates a row in a table with a user-defined rowID and a pre-determined column id in the form: row[row#]-col[col#]
{
  var tableToEdit = document.getElementsByClassName(tableclass)[0]; //get table to edit
  var numCols = tableToEdit.getElementsByTagName('th').length;
  //gets the number of tableheader elements in table. made so we can keep number of columns the same
  var numRows = tableToEdit.rows.length; //becomes a part of the id of new tds (columns)

  var tableRow = document.createElement('tr'); // create a row
  tableRow.setAttribute('id', rowid);

  for (var i=0; i < numCols; i++) //number of td (columns)
  {
    var newCol = document.createElement('td');
    newCol.setAttribute('id', 'row'+numRows+'-col'+i); //id is in form: row[rowNumber]-col[colNumber]
    newCol.style.border = "1px solid white";
    tableRow.appendChild(newCol); //append to row
  }
  tableToEdit.appendChild(tableRow); //append the entire row to table itself
  console.log("Created new row in " + tableclass + " with " + numCols + " columns");
}



function changeTableText(tableclass, rowNum, colNum, text)
//changes the text on a table of user-defined class and the (row,col) coordinates of that table
{
  var tableToEdit = document.getElementsByClassName(tableclass)[0];
  var row = tableToEdit.rows[rowNum];
  var col = row.cells[colNum];
  col.innerHTML = text;
}








function openTab(TabName, elmnt, color) {
  // Hide all elements with class="tabcontent" by default */
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Remove the background color of all tablinks/buttons
  tablinks = document.getElementsByClassName("tablink");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].style.backgroundColor = "";
  }

  // Show the specific tab content
  document.getElementById(TabName).style.display = "block";

  // Add the specific color to the button used to open the tab content
  elmnt.style.backgroundColor = color;
}

// Get the element with id="defaultOpen" and click on it
document.getElementById("defaultOpen").click(); 







function setTableElemColor(tableclass, rowNum, colNum, color)
//changes the background color of specific (row,col) location of a table
{
  var table = document.getElementsByClassName(tableclass)[0];
  var row = table.rows[rowNum];
  var elemToChange = row.cells[colNum];
  elemToChange.setAttribute("bgcolor", color);
  console.log(tableclass + " at (" + rowNum + "," + colNum + ") changed to " + color);
  // all need to be in quotes, color needs to be in form of "#000000"
  // also it works :)
}

// ---
// from here on, it's functions that call other functions (with more things obviously)
// ---

function addColorToTaskStatus(tableclass)
//change bg of task status (tableclass[row#][2]) based on incomplete/complete
{
  var table = document.getElementsByClassName(tableclass)[0];
  var numRows = table.rows.length;
  for (var i = 0; i < numRows; i++)
  {
    var row = table.rows[i];
    var col = row.cells[2]; //this is the location of task status !!HARDCODED!!
    if (col.innerHTML == "Incomplete")
    {
      setTableElemColor(tableclass, i, 2, "#FF0000"); //change to red if incomplete
    }
    else if (col.innerHTML == "Complete")
    {
      setTableElemColor(tableclass, i, 2, "#00FF00"); //change to green if complete
    }
    else
    {
      setTableElemColor(tableclass, i, 2, "#FFFF00"); //change to yellow if neither/unsure
    }
  }
}

function populateTable(tableclass)
//populate table with data, but it's all hardcoded for now
{
  //something tells me based on this pattern, we can do this is a few for-loops
  changeTableText(tableclass, 0, 0, "Water Field 69: Watermelons");
  changeTableText(tableclass, 0, 1, "Smith Johnson");
  changeTableText(tableclass, 0, 2, "Complete");
  changeTableText(tableclass, 0, 3, "April 20, 1969");

  changeTableText(tableclass, 1, 0, "Till Field 23: Wheat");
  changeTableText(tableclass, 1, 1, "Greg Sevensen");
  changeTableText(tableclass, 1, 2, "Incomplete");
  changeTableText(tableclass, 1, 3, "January 29, 2020");

  changeTableText(tableclass, 2, 0, "Fertilize Field 1: Tomatoes");
  changeTableText(tableclass, 2, 1, "Jimmy John");
  changeTableText(tableclass, 2, 2, "Incomplete");
  changeTableText(tableclass, 2, 3, "September 21, 2019");

  changeTableText(tableclass, 3, 0, "Till Field 2: Corn");
  changeTableText(tableclass, 3, 1, "Bryan Hendrix");
  changeTableText(tableclass, 3, 2, "Complete");
  changeTableText(tableclass, 3, 3, "June 13, 2019");

  changeTableText(tableclass, 4, 0, "Fertilize Field 20: Cabbages");
  changeTableText(tableclass, 4, 1, "Matt Matthews");
  changeTableText(tableclass, 4, 2, "Complete");
  changeTableText(tableclass, 4, 3, "April 30, 2019");

  changeTableText(tableclass, 5, 0, "Water Field 19: Buttersquash");
  changeTableText(tableclass, 5, 1, "Ken Kensington");
  changeTableText(tableclass, 5, 2, "Incomplete");
  changeTableText(tableclass, 5, 3, "May 1, 2019");

  changeTableText(tableclass, 6, 0, "Water Field 51: Potatoes");
  changeTableText(tableclass, 6, 1, "Fore Foremanson");
  changeTableText(tableclass, 6, 2, "Incomplete");
  changeTableText(tableclass, 6, 3, "July 4, 2019");

  console.log("Populated table " + tableclass + " with data");
}
