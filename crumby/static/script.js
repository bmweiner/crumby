function initTable(tbl, days){
  url = 'api/' + tbl + '?days=' + days;
  $.ajax({url: url, success: function(result){
    columns = []
    for(i=0; i<result['columns'].length; i++){
      columns[i] = {title: result['columns'][i]};
    }

    $('#tbl-title').text(tbl);

    if($.fn.DataTable.isDataTable('#tbl-data')){
      $('#tbl-data').DataTable().destroy();
      $('#tbl-data').empty();
    };

    $('#tbl-data').DataTable({
      destry: true,
      data: result['data'],
      columns: columns
    });
  }});
};

$('#arg-days').on('change', function() {
  initTable($('#arg-tbl').val(), this.value);
});

$('#arg-tbl').on('change', function() {
  initTable(this.value, $('#arg-days').val());
});

$(document).ready(function() {
  initTable($('#arg-tbl').val(), $('#arg-days').val());
});
