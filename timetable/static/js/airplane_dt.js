$(document).ready(function () {

    $('#airplane_dt thead tr')
    .clone(true)
    .addClass('filters-airplane')
    .appendTo('#airplane_dt thead');
    var airplane_dt = $('#airplane_dt').DataTable({
            "dom": 'ftipr',
             //--------------------Память фильторв---------------------------
             stateSave: true,
             select: true,
             searchPanes: {
                // cascadePanes: true,
                initCollapsed: true,
             },
             
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
                    var cell = $('.filters-airplane th').eq(
                        $(api.column(colIdx).header()).index()
                    );
                    var title = $(cell).text();
                    
                    if (title != '' ) {
                        //добавляем input 
                        $(cell).html('<input  type="text" placeholder="' + title + '" />');
        
                    } else {
                    }
        
                    // делаем input "живым"
                    $(
                        'input',
                        $('.filters-airplane th').eq($(api.column(colIdx).header()).index())
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
                        $('input', $('.filters-airplane th')[colIdx]).val( res );
                    }
                    savedSelected = state.selected;
                    });
                }
              
            },
           
        });

            //Сбросить фильтры
    $('#airplane_dt-resetFilter').on('click', function (e) {
        airplane_dt_resetFilters()
    });



    function airplane_dt_resetFilters() {
        airplane_dt.state.clear();
        location.reload()
    } 
});

