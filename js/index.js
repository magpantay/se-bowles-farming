//note: honestly the ids don't seem to matter, they're just for organizational purposes
//the ids don't matter since we access the table's rows and cols by row,col coordinates
//the tableclass is important, though, because we access that specific table by the table class name
function tableCreation(tableclass, csv_rows_length)
//creates a table with user-defined class name with 6 table headers
//creates all of the rows (and columns by necessity) based on the amount of csv rows there are for the table, which will be filled later by populateTable
//note: tableclass must be in quotes
{
  var body = document.body;
  tablee = document.createElement("table");
  //tablee.style.width = "100%";
  //tablee.style.border = "1px solid white";
  tablee.setAttribute('class', tableclass); //!!!! this is important for finding the table (and, by association, table body) in other functions !!!!
  tablee.setAttribute('id', tableclass);

  /* table head creation */
  var table_head = document.createElement("thead");
  table_head.setAttribute('class', tableclass + '_head');

  var table_header_row = document.createElement("tr"); //because the head is supposed to, by convention, contain a row (tr) of columns (th)
  table_header_row.setAttribute('class', tableclass + '_header_row');

  var table_header = document.createElement('th');
  table_header.setAttribute('class', tableclass + '_header');
  table_header.setAttribute('id', 'task_name');
  table_header.innerHTML = "Task Name";
  //table_header.style.border = "1px solid white";
  table_header_row.appendChild(table_header); //append table header to thead

  table_header = document.createElement('th');
  table_header.setAttribute('class', tableclass + '_header');
  table_header.setAttribute('id', 'farm_name');
  table_header.innerHTML = "Farm Name";
  //table_header.style.border = "1px solid white";
  table_header_row.appendChild(table_header); //append table header to thead

  table_header = document.createElement('th');
  table_header.setAttribute('class', tableclass + '_header');
  table_header.setAttribute('id', 'field_name');
  table_header.innerHTML = "Field Name";
  //table_header.style.border = "1px solid white";
  table_header_row.appendChild(table_header); //append table header to row

  table_header = document.createElement('th');
  table_header.setAttribute('class', tableclass + '_header');
  table_header.setAttribute('id', 'status');
  table_header.innerHTML = "Task Status";
  //table_header.style.border = "1px solid white";
  table_header_row.appendChild(table_header); //append table header to row

  table_header = document.createElement('th');
  table_header.setAttribute('class', tableclass + '_header');
  table_header.setAttribute('id', 'due_date');
  table_header.innerHTML = "Due Date";
  //table_header.style.border = "1px solid white";
  table_header_row.appendChild(table_header); //append table header to row

  table_header = document.createElement('th');
  table_header.setAttribute('class', tableclass + '_header');
  table_header.setAttribute('id', 'completed_date');
  table_header.innerHTML = "Completed Date";
  //table_header.style.border = "1px solid white";
  table_header_row.appendChild(table_header); //append table header to row

  table_header = document.createElement('th');
  table_header.setAttribute('class', tableclass + '_header');
  table_header.setAttribute('id', 'author_name');
  table_header.innerHTML = "Author Name";
  table_header_row.appendChild(table_header); //append table header to row

  table_head.appendChild(table_header_row); //append table row (with all of the headers) to head
  tablee.appendChild(table_head); //append table head to table

  console.log("Created new table with " + (table_header_row.getElementsByTagName('th').length) + " columns with class name " + tableclass);

  /* table body creation */
  var tableBody = document.createElement("tbody");
  tableBody.setAttribute("class", tableclass + "_body");
  tableBody.setAttribute("id", tableclass + "_body");
  var numCols = tablee.getElementsByTagName('th').length; //number of columns currently in table (th)

  /* rows creation */
  for (var i = 0; i < csv_rows_length - 2; i++) //i=0 to account for top header of CSV file (which is at csv_rows[0]), csv_rows.length offset by 2 because of the that PapaParse seems to include an extra blank line in the end of the CSV file
  {
    var tableRow = document.createElement('tr'); //create a row
    tableRow.setAttribute('class', tableclass + '_row');
    tableRow.setAttribute('id', i);

    for (var j = 0; j < numCols; j++)
    {
      var newCol = document.createElement('td'); //td = columns
      newCol.setAttribute('class', tableclass + '_non_header_col');
      newCol.setAttribute('id', 'row' + i + '-col' + j); //id is in form: row[rowNumber]-col[colNumber], starts with 0, hence i-1 offset
      tableRow.appendChild(newCol); //place the new column in current row
    }
    tableBody.appendChild(tableRow); //place the entire current row (with columns) in table body
  }

  console.log("Created " + (csv_rows_length - 2) + " rows, each with " + numCols + " columns");

  tablee.appendChild(tableBody); //place the entire body (with rows) in table
  body.appendChild(tablee); //place the entire table in HTML body
}

function changeTableText(tableclass, rowNum, colNum, text)
//changes the text on a table of user-defined class and the (row,col) coordinates of that table (note: table headers th don't count as a row)
{
  var tableBody = document.getElementsByClassName(tableclass)[0].getElementsByTagName('tbody')[0]; //gets body of table by finding table in document with tableclass, then finding the body of that table
  var row = tableBody.rows[rowNum]; //number of rows in tableBody
  var col = row.cells[colNum];
  col.innerHTML = text;
}

function setTableElemColor(tableclass, rowNum, colNum, color)
//changes the background color of specific (row,col) location of a table
{
  var tableBody = document.getElementsByClassName(tableclass)[0].getElementsByTagName('tbody')[0]; //gets body of table by finding table in document with tableclass, then finding the body of that table
  var row = tableBody.rows[rowNum]; //number of rows in tableBody
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
  var tableBody = document.getElementsByClassName(tableclass)[0].getElementsByTagName('tbody')[0]; //gets body of table by finding table in document with tableclass, then finding the body of that table
  var numRows = tableBody.rows.length; //number of rows in tableBody
  var column_of_task_status = 3; //value of column where task status is (reminder that everything starts at 0)

  for (var i = 0; i < numRows; i++)
  {
    var current_row = tableBody.rows[i];
    var col = current_row.cells[column_of_task_status]; //this is the location of task status at the current row !!HARDCODED!!
    if (col.innerHTML == "IN-PROGRESS-NO-DUE-DATE" || col.innerHTML == "IN-PROGRESS-GOOD")
    {
      setTableElemColor(tableclass, i, column_of_task_status, "#D7DF01"); //d7df01 dark yellow if in-progress and not late (or no due date set)
    }
    else if (col.innerHTML == "COMPLETE-LATE")
    {
      setTableElemColor(tableclass, i, column_of_task_status, "#86B404"); //change to green-yellow if complete but late
    }
    else if (col.innerHTML == "COMPLETE-ON-TIME" || col.innerHTML == "COMPLETE-NO-DUE-DATE")
    {
      setTableElemColor(tableclass, i, column_of_task_status, "#088A08"); //changes to dark green if complete and on time (or no due date set)
    }
    else if (col.innerHTML == "IN-PROGRESS-LATE")
    {
      setTableElemColor(tableclass, i, column_of_task_status, "#FF0000"); //changes to red if in progress and late
    }
    else
    {
      setTableElemColor(tableclass, i, column_of_task_status, "#848484"); //change to gray if none of the above
    }
  }
}

function populateTable(tableclass, csv_rows)
{
  for (var i = 0; i < (csv_rows.length - 2); i++) //offset i by 1 to account for top header of CSV file (which is at csv_rows[0]), csv_rows.length offset by 2 because of the i offset and the fact that PapaParse seems to include an extra blank line in the end of the CSV file
  {
    changeTableText(tableclass, i, 0, csv_rows[i + 1][1]); //task_name
    changeTableText(tableclass, i, 1, csv_rows[i + 1][4]); //farm_name
    changeTableText(tableclass, i, 2, csv_rows[i + 1][5]); //field_name
    changeTableText(tableclass, i, 3, csv_rows[i + 1][7]); //job_status
    changeTableText(tableclass, i, 4, csv_rows[i + 1][2]); //due_at
    changeTableText(tableclass, i, 5, csv_rows[i + 1][3]); //completed_at
    changeTableText(tableclass, i, 6, csv_rows[i + 1][8]); //author_name
  }
  console.log("Populated table with " + (csv_rows.length - 2) + " rows of data");
}
