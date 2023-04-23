$(document).ready(function () {

//клонируем header и вставляем после него
$('#bootstrapdatatable thead tr')
.clone(true)
.addClass('filters')
.appendTo('#bootstrapdatatable thead');
var savedSelected;
// DataTable
var table = $('#bootstrapdatatable').DataTable({
    deferRender: true,
    orderCellsTop: true,
    fixedHeader: true,
    

     //--------------------Память фильторв---------------------------
     stateSave: true,
     dom: 'Plfrtip',
     select: true,
     searchPanes: {
        // cascadePanes: true,
        initCollapsed: true,
     },
     columnDefs: [
         {
             searchPanes: {
                 show: true,
             },
             targets: [1, 2, 3, 4, 5]
         }
     ],
     language: {
         searchPanes: {
            collapseMessage: 'Скрыть все',
            showMessage: 'Показать все',
            clearMessage: 'Очистить фильтры',
             title: {
                 _: 'Выбранные фильтры - %d',
                 0: 'Нет выбранных фильтров',
             }
         }
     },   
     
     stateSaveParams: function (s, data) {
        //относительые даты
        data.min = $("#minDate").val();
        data.max = $("#maxDate").val();

        //относительные кнопки
        data.buttonDate = $(".relativeDate").find('button.btn-warning').html()
        
        //выбор строки
        data.selected = this.api().rows({selected:true})[0];


        //видимость панели настроек
        data.visibleSetDiv = visVar
    },
    stateLoadParams: function (s, data) {
        $("#minDate").val(data.min);
        $("#maxDate").val(data.max);
        
        if(data.visibleSetDiv){
            $(".settingDiv").slideToggle()
            visVar = data.visibleSetDiv
        }

        $( "button:contains("+ data.buttonDate +")" ).removeClass("btn-success")
        $( "button:contains("+ data.buttonDate +")" ).addClass("btn-warning")
    },

   
    //---------------Конец Память фильторв конец-------------------

   

    columnDefs: [
        {
            targets: [9],
            type: 'date'
        },
        {
            targets: 0,
            visible: false,
        },
        {
            targets: 11,
            visible: false,
        },
        
    ],

    //Для Show
    "aLengthMenu": [[3, 7, 10, 25, -1], [3, 7, 10, 25, "All"]],
    "iDisplayLength": 7,
    

   
    initComplete: function () {
        
        var api = this.api();
        api
        .columns()
        .eq(0)
        .each(function (colIdx) {
            // перебираем каждый элеемент клонированного 
            var cell = $('.filters th').eq(
                $(api.column(colIdx).header()).index()
            );
            var title = $(cell).text();
            
            if (title != '' && title != 'Изменить' && title != 'Удалить') {
                //добавляем input 
                $(cell).html('<input class="form-control" style="width:100%" type="text" placeholder="' + title + '" />');

            } else {
                $(cell).html('');
                $(cell).toggleClass('th');
            }

            // делаем input "живым"
            $(
                'input',
                $('.filters th').eq($(api.column(colIdx).header()).index())
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
                $('input', $('.filters th')[colIdx-1]).val( res );
            }
            savedSelected = state.selected;
            });
        }
      
    },

});

    var visVar;
    //скрывать панель параметров
    $(".settingSVG").click(function(){
        visVar = !$('.settingDiv').is(":visible")
        $(".settingDiv").slideToggle();
        table.draw();
    });

    table.row(savedSelected).select()
     //Скрыть столбцы
    $('.checkColumn input:checkbox').click(function(){
        var column = table.column($(this).attr('data-column'));
        column.visible(!column.visible());
    });
      
    
    var len = 0
    for ( var i=0 ; i<=$("#bootstrapdatatable tr").length+1 ; i++ ) {
        table.column(i).visible() === true ? len+=1 : len=len
    }

   for ( var i=0 ; i<=$("#bootstrapdatatable tr").length+1 ; i++ ) {
        if(table.column(i).visible() === true) {
            $("input[data-column='" + i +"']").prop('checked', true)
        } else {
            $("input[data-column='" + i +"']").prop('checked', false)
        }
    }

    //Сбросить фильтры
    $('#resetFilter').on('click', function (e) {
        resetFilters()
    });



    function resetFilters() {
        table.state.clear();
        location.reload()
    }




    //Выбор строки при наведении 
     $(function() {
        $('#bootstrapdatatable')
          .on('mouseenter', 'tr.mySelect',  function() {
            $(this).css("background-color", "#e5f4ff");
            
          })
          .on('mouseleave', 'tr.mySelect',  function() {
            $(this).css("background-color", "white");
          });
      })

    //Выбор строки при клике 
      $('#bootstrapdatatable tbody').on('click', 'tr.mySelect', function () {
        $('.th.sorting').click();

        if ($(this).hasClass('selected')) {
            $(this).removeClass('selected');

            
            $(this).find('td input.delete_confirm').removeClass("btn-danger");
            $(this).find('td input.delete_confirm').addClass("btn-outline-danger");

            $(this).find('td button').removeClass("btn-success");
            $(this).find('td button').addClass("btn-outline-success");
            
            $(this).find('td.notfound').removeClass('notfoundColor');
        } else {
            //удаляю у не выбранных кнопок класс
            table.$('tr.selected').find('td button').removeClass("btn-success");
            table.$('tr.selected').find('td button').addClass("btn-outline-success");

            table.$('tr.selected').find('td input.delete_confirm').removeClass("btn-danger");
            table.$('tr.selected').find('td input.delete_confirm').addClass("btn-outline-danger");

            //удаляю не выбранным и добавляю выбранной строке клас
            table.$('tr.selected').removeClass('selected');
            table.$('td.notfound').removeClass('notfoundColor');
            $(this).addClass('selected');
            $(this).find('td.notfound').addClass('notfoundColor');

            //добавляю выбранной кнопке класс
            $(this).find('td button').removeClass("btn-outline-success");
            $(this).find('td button').addClass("btn-success");

            $(this).find('td input.delete_confirm').removeClass("btn-outline-danger");
            $(this).find('td input.delete_confirm').addClass("btn-danger");

        }
    });
   
    

    //Рисуем графики в зависимости от состояния таблиц   
    table.on('draw', function () {
        drawTable(table);
        toggleChart();
        
    });
    drawTable(table);
    init();

    

    //Поиск по диапазону дат
    $.fn.dataTable.ext.search.push(
    function (settings, data, dataIndex) {

            
        var valid = true;
        var min = moment($("#minDate").val());
        if (!min.isValid()) { min = null; }


        var max = moment($("#maxDate").val());
        if (!max.isValid()) { max = null; }

        var startDateRange;      
        var EndDateRange;

        if (min === null && max === null) {
            valid = true;
        }
        else {
            $.each(settings.aoColumns, function (i, col) {
                var cDate = moment(data[i],'YYYY-MM-DD');
               
                if (col.sTitle == "Начало") {
                    startDateRange = cDate;
                                  
                }
                if (col.sTitle == "Окончание") {
                    EndDateRange = cDate;
                }
            });

            if (
                !moment(startDateRange).isBetween(min, max, undefined, '[]')
                &&
                !moment(EndDateRange).isBetween(min, max, undefined, '[]')
                &&
                (!moment(min).isBetween(startDateRange, EndDateRange, undefined, '[]')
                && 
                !moment(max).isBetween(startDateRange, EndDateRange, undefined, '[]'))
                ) 
                {valid = false;}

        }
        return valid;
    });
    

     $("#ButtonDateFilter").click(function () {
            table.draw();
    });
      
   //относительные даты
   $(".relativeDate button").addClass("btn-secondary"); 
    $(".relativeDate button").click(function () {
        CurrentOrNotDate = parseInt($(this).val())
        typeDate = $(this).attr('name')
        
        var minDate = moment().subtract(CurrentOrNotDate, typeDate).startOf(typeDate).format('YYYY-MM-DD');
        var maxDate = moment().subtract(CurrentOrNotDate, typeDate).endOf(typeDate).format('YYYY-MM-DD');
        
        $("#minDate").val(minDate);
        $("#maxDate").val(maxDate);

        $(".relativeDate button").attr('class', "btn mt-2 btn-secondary");
        $(this).removeClass("btn-warning");
        $(this).addClass("btn-warning");

        table.draw();
    });

    if ($("#minDate").val() == ''){
        $('button[value="0"][name="year"]').click();
    }  
    

    $("body").css("opacity", 1);
});





