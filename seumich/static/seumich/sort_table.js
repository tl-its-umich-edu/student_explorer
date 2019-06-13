$(document).ready(function() {
    $(".table").tablesorter({
        theme: "bootstrap",
        headerTemplate: "{content} {icon}",
        widgets: [ "uitheme", "filter", "columns", "zebra" ]
    })
    .tablesorterPager({
        // target the pager markup - see the HTML block below
        container: $(".ts-pager"),
        // target the pager page select dropdown - choose a page
        cssGoto  : ".pagenum",
        // remove rows from the table to speed up the sort of large tables.
        // setting this to false, only hides the non-visible rows; needed if you plan to add/remove rows with the pager enabled.
        removeRows: false,
        // output string - default is '{page}/{totalPages}';
        // possible variables: {page}, {totalPages}, {filteredPages}, {startRow}, {endRow}, {filteredRows} and {totalRows}
        output: "{startRow} - {endRow} / {filteredRows} ({totalRows})"
      });
});
