$(document).ready(function () {


    // timetable_history_dt
    $('#timetable_history_dt thead tr')
    .clone(true)
    .addClass('filters_timetable_history_dt')
    .appendTo('#timetable_history_dt thead');

    var timetable_history_dt = $('#timetable_history_dt').DataTable({
        "dom": 'ftipr',
         //--------------------Память фильторв---------------------------
         stateSave: true,
         select: true,
         searchPanes: {
            // cascadePanes: true,
            initCollapsed: true,
         },
         
         "iDisplayLength": -1,  
         order: [[0, 'desc']],
         stateSaveParams: function (s, data) {
            //выбор строки
            data.selected = this.api().rows({selected:true})[0];
        },

        initComplete: function () {
        
            var api = this.api();
            api
            .columns()
            .eq(0)
            .each(function (colIdx) {
                // перебираем каждый элеемент клонированного 
                var cell = $('.filters_timetable_history_dt th').eq(
                    $(api.column(colIdx).header()).index()
                );
                var title = $(cell).text();
                
                if (title != '' ) {
                    //добавляем input 
                    $(cell).html('<input class="form-control" style="width:100%" type="text" placeholder="' + title + '" />');
    
                } else {
                }
    
                // делаем input "живым"
                $(
                    'input',
                    $('.filters_timetable_history_dt th').eq($(api.column(colIdx).header()).index())
                )
                    .off('keyup change')
                    .on('change', function (e) {
                        // Get the search value
                        $(this).attr('title', $(this).val());
                        var regexr = '({search})'; //$(this).parents('th').find('select').val();
    
                        var cursorPosition = this.selectionStart;
                        // Search the column for that value
                        api
                            .column(colIdx)
                            .search(
                                this.value != ''
                                    ? regexr.replace('{search}', '(((' + this.value + ')))')
                                    : '',
                                this.value != '',
                                this.value == ''
                            )
                            .draw();
                    })
                    .on('keyup', function (e) {
                        e.stopPropagation();
    
                        $(this).trigger('change');
                        $(this)
                            .focus()[0]
                            .setSelectionRange(cursorPosition, cursorPosition);
                    });
            });
    
            var state = api.state.loaded();
            if ( state ) {
                    api.columns().eq( 0 ).each( function ( colIdx ) {
                    var colSearch = state.columns[colIdx].search;
                    var res = ''
                if ( colSearch.search ) {
                    res = colSearch.search.replace('))))','')
                    res = res.replace('((((','')
                    
                    $('input', $('.filters_timetable_history_dt th')[colIdx]).val( res );
                }
                savedSelected = state.selected;
                });
            }
          
        },
       
    });

    //Сбросить фильтры
    $('#timetable_history_dt-resetFilter').on('click', function (e) {
        timetable_history_dt_resetFilters()
    });



    function timetable_history_dt_resetFilters() {
        timetable_history_dt.state.clear();
        location.reload()
    }
});

