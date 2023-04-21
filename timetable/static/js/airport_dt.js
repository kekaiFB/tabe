$(document).ready(function () {

    $('#airport_dt thead tr')
    .clone(true)
    .addClass('filters-airport')
    .appendTo('#airport_dt thead');
    var airport_dt = $('#airport_dt').DataTable({
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
                    var cell = $('.filters-airport th').eq(
                        $(api.column(colIdx).header()).index()
                    );
                    var title = $(cell).text();
                    
                    if (title != '' ) {
                        //добавляем input 
                        $(cell).html('<input class="form-control" type="text" placeholder="' + title + '" />');
        
                    } else {
                    }
        
                    // делаем input "живым"
                    $(
                        'input',
                        $('.filters-airport th').eq($(api.column(colIdx).header()).index())
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
                        $('input', $('.filters-airport th')[colIdx]).val( res );
                    }
                    savedSelected = state.selected;
                    });
                }
              
            },
           
        });

            //Сбросить фильтры
    $('#airport_dt-resetFilter').on('click', function (e) {
        airport_dt_resetFilters()
    });



    function airport_dt_resetFilters() {
        airport_dt.state.clear();
        location.reload()
    } 
});

