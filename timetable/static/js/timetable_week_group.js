$(document).ready(function () {


    // timetable_week_group
    $('#timetable_week_group thead tr.forFilter')
    .clone(true)
    .addClass('filters_timetable_week_group')
    .appendTo('#timetable_week_group thead')
    .removeAttr('style');

    var groupColumn = 0;

    var timetable_week_group = $('#timetable_week_group').DataTable({
        "dom": 'ftipr',
        order: [[groupColumn, 'asc']],
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

        drawCallback: function (settings) {
            var api = this.api();
            var rows = api.rows({ page: 'current' }).nodes();
            var last = null;
 
            api
                .column(groupColumn, { page: 'current' })
                .data()
                .each(function (group, i) {
                    if (last !== group) {
                        $(rows)
                            .eq(i)
                            .before('<tr class="group bg-secondary p-2 opacity-50"><td colspan="20" class="h4 text-warning">' + group.substring(2) + '</td></tr>');
 
                        last = group;
                    }
                });
        },

        initComplete: function () {
        
            var api = this.api();
            api
            .columns()
            .eq(0)
            .each(function (colIdx) {
                // перебираем каждый элеемент клонированного 
                var cell = $('.filters_timetable_week_group th').eq(
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
                    $('.filters_timetable_week_group th').eq($(api.column(colIdx).header()).index())
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
                    
                    $('input', $('.filters_timetable_week_group th')[colIdx]).val( res );
                }
                savedSelected = state.selected;
                });
            }
        },
    });
    timetable_week_group.column( 0 ).visible( false );

    $('#timetable_week_group tbody').on('click', 'tr.group', function () {
        var currentOrder = timetable_week_group.order()[0];
        if (currentOrder[0] === groupColumn && currentOrder[1] === 'asc') {
            timetable_week_group.order([groupColumn, 'desc']).draw();
        } else {
            timetable_week_group.order([groupColumn, 'asc']).draw();
        }
    });


    //Сбросить фильтры
    $('#timetable_week_group-resetFilter').on('click', function (e) {
        timetable_week_group_resetFilters()
    });



    function timetable_week_group_resetFilters() {
        timetable_week_group.state.clear();
        location.reload()
    }
});

