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
  table_header_2.setAttribute('id', 'farm_name');
  table_header_2.innerHTML = "Farm Name";
  table_header_2.style.border = "1px solid white";
  table_body.appendChild(table_header_2);

  var table_header_3 = document.createElement('th');
  table_header_3.setAttribute('id', 'field_name');
  table_header_3.innerHTML = "Field Name";
  table_header_3.style.border = "1px solid white";
  table_body.appendChild(table_header_3);

  var table_header_4 = document.createElement('th');
  table_header_4.setAttribute('id', 'status');
  table_header_4.innerHTML = "Task Status";
  table_header_4.style.border = "1px solid white";
  table_body.appendChild(table_header_4);

  var table_header_5 = document.createElement('th');
  table_header_5.setAttribute('id', 'due_date');
  table_header_5.innerHTML = "Due Date";
  table_header_5.style.border = "1px solid white";
  table_body.appendChild(table_header_5);

  tablee.appendChild(table_body);
  body.appendChild(tablee);
  console.log("Created new table with class name " + tableclass);
}

function tableRowCreate(tableclass, rowid)
//creates a row in a table with a user-defined rowID and a pre-determined column id in the form: row[row#]-col[col#]
{
  var tableToEdit = document.getElementsByClassName(tableclass)[0]; //get table to edit
  var numCols = tableToEdit.getElementsByTagName('th').length; //number of columns
  //gets the number of tableheader elements in table. made so we can keep number of columns the same
  var numRows = tableToEdit.rows.length; //becomes a part of the id of new tds (columns)

  var tableRow = document.createElement('tr'); // create a row
  tableRow.setAttribute('id', rowid);

  var newCol = document.createElement('td');
  newCol.setAttribute('id', 'row' + numRows + '-col' + 0); //id is in form: row[rowNumber]-col[colNumber]
  newCol.align="left"
  newCol.style.border = "1px solid white";
  tableRow.appendChild(newCol); //append to row

  for (var i = 1; i < numCols; i++) //number of td (columns)
  {
    var newCol = document.createElement('td');
    newCol.setAttribute('id', 'row' + numRows + '-col' + i); //id is in form: row[rowNumber]-col[colNumber]
    newCol.style.border = "1px solid white";
    tableRow.appendChild(newCol); //append to row
  }
  tableToEdit.appendChild(tableRow); //append the entire row to table itself
  console.log("Created new row in " + tableclass + " with " + numCols + " columns");
}

function changeTableText(tableclass, rowNum, colNum, text)
//changes the text on a table of user-defined class and the (row,col) coordinates of that table (note: table headers th don't count as a row)
{
  var tableToEdit = document.getElementsByClassName(tableclass)[0];
  var row = tableToEdit.rows[rowNum];
  var col = row.cells[colNum];
  col.innerHTML = text;
}

function setTableElemColor(tableclass, rowNum, colNum, color)
//changes the background color of specific (row,col) location of a table
{
  var table = document.getElementsByClassName(tableclass)[0];
  var row = table.rows[rowNum];
  var elemToChange = row.cells[colNum];
  elemToChange.setAttribute("bgcolor", color);
  //console.log(tableclass + " at (" + rowNum + "," + colNum + ") changed to " + color);
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
    var current_row = table.rows[i];
    var col = current_row.cells[3]; //this is the location of task status at the current row !!HARDCODED!!
    if (col.innerHTML == "IN-PROGRESS-NO-DUE-DATE" || col.innerHTML == "IN-PROGRESS-GOOD")
    {
      setTableElemColor(tableclass, i, 3, "#D7DF01"); //d7df01 dark yellow if in-progress and not late (or no due date set)
    }
    else if (col.innerHTML == "COMPLETE-LATE")
    {
      setTableElemColor(tableclass, i, 3, "#86B404"); //change to green-yellow if complete but late
    }
    else if (col.innerHTML == "COMPLETE-ON-TIME" || col.innerHTML == "COMPLETE-NO-DUE-DATE")
    {
      setTableElemColor(tableclass, i, 3, "#088A08"); //changes to dark green if complete and on time (or no due date set)
    }
    else if (col.innerHTML == "IN-PROGRESS-LATE")
    {
      setTableElemColor(tableclass, i, 3, "#FF0000"); //changes to red if in progress and late
    }
    else
    {
      setTableElemColor(tableclass, i, 3, "#848484"); //change to gray if none of the above
    }
  }
}

function populateTable(tableclass, csv_rows)
{
  for (var i = 0; i < (csv_rows.length - 2); i++) //offset i by 1 to account for top header of CSV file (which is at csv_rows[0]), csv_rows.length offset by 2 because of the i offset and the fact that PapaParse seems to include an extra blank line in the end of the CSV file
  {
    changeTableText(tableclass, i, 0, csv_rows[i + 1][2]); //task_name
    changeTableText(tableclass, i, 1, csv_rows[i + 1][5]); //farm_name
    changeTableText(tableclass, i, 2, csv_rows[i + 1][6]); //field_name
    changeTableText(tableclass, i, 3, csv_rows[i + 1][8]); //job_status
    changeTableText(tableclass, i, 4, csv_rows[i + 1][3]); //due_at
  }
  console.log("Populated table with " + (csv_rows.length - 2) + " rows of data");
}
