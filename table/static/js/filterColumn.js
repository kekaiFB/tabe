$(document).ready(function () {
    

//скрывать панель параметров
//$(".settingDiv").hide();
$(".settingSVG").click(function(){
    $(".settingDiv").slideToggle();
    });

//клонируем header и вставляем после него
$('#bootstrapdatatable thead tr')
.clone(true)
.addClass('filters')
.appendTo('#bootstrapdatatable thead');

// DataTable
var dataMyTable;
var table = $('#bootstrapdatatable').DataTable({
    deferRender: true,
    orderCellsTop: true,
    fixedHeader: true,
    
    deferRender: true,

    columnDefs: [
        {
          targets: [9],
          type: 'date'
        }
    ],
    //Для Show
    "aLengthMenu": [[3, 7, 10, 25, -1], [3, 7, 10, 25, "All"]],
    "iDisplayLength": 7,
    
    //--------------------Память фильторв---------------------------
    select: true,
    dom: 'Bfrtip',
    language:{
        stateRestore: {
            removeSubmit: 'Удалить',
            removeConfirm: 'Вы действительно хотите удалить %s?',
            emptyStates: 'Нет состояний',
            renameButton: 'Переименовать',
            renameLabel: '',
            removeTitle: '',
            renameTitle: '',
        },
        buttons: {
            createState: 'Создать состояние',
            savedStates: 'Сохраненные состояния',
            updateState: 'Обновить',
            stateRestore: 'Новое состояние %d',
            removeState: 'Удалить',
            renameState: 'Переименовать',

        }},
    buttons: ['createState', 'savedStates'],
    stateSaveParams: function (s, data) {
        data.min = $("#minDate").val();
        data.max = $("#maxDate").val();
    },
    stateLoadParams: function (s, data) {
        $("#minDate").val(data.min);
        $("#maxDate").val(data.max);
    },

      
   //---------------Конец Память фильторв конец-------------------
   
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
                   
                    if (title == 'Смена' || title == 'Служба' || title == 'Должность' || title == 'Причина'){
                        $(cell).html('');
                        $(cell).toggleClass('th');
                    } else if (title != '' && title != 'Изменить' && title != 'Удалить') {
                        //добавляем input 
                        $(cell).html('<input type="text" placeholder="' + title + '" />');

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
       

       //Ставим Option на выбор select
       this.api()
       .columns([1,2,3,5])
       .every(function (colIdx) {


            var cell = $('.filters th').eq(
                $(api.column(colIdx).header()).index()
            );
           var column = this;
           var select = $('<select><option value="">Все</option></select>')
               .appendTo(cell)
               .on('change', function () {
                   var val = $.fn.dataTable.util.escapeRegex($(this).val());

                   column.search(val ? '^' + val + '$' : '', true, false).draw();
               });

           column
               .data()
               .unique()
               .sort()
               .each(function (d, j) {
                   select.append('<option value="' + d + '">' + d + '</option>');
               });     
       });
       
    },

});

    
     //Скрыть столбцы
    $('.checkColumn input:checkbox').click(function(){
        var column = table.column($(this).attr('data-column'));
        column.visible(!column.visible());
    });
      

    //скрываем по умолчанию ID и УДАЛИТЬ
    for ( var i=0 ; i<=$("#bootstrapdatatable tr").length+1 ; i++ ) {
        table.column(i).visible() === true ? '' : table.column(i).visible( true )
    }

    $('.checkColumn input:checkbox').prop('checked', true);
    $('#hideID').click();
    $('#hideDeleteRowButton').click();


    //Сбросить фильтры
    $('#resetFilter').on('click', function (e) {
        resetFilters()
    });



    function resetFilters() {
        //table.search( '' ).columns().search( '' ).draw();
        //table.column($(this).data('col-index')).search('', false, false);
        //table.columns().search("").draw();
        //$("input").val("");
        //$(".delete_confirm").val("Удалить");
        //$('select').prop('selectedIndex',0);
        //$('span.toggle-vis').removeClass('btn-warning');

        
        //скрываем по умолчанию ID и УДАЛИТЬ
      /*  for ( var i=0 ; i<=$("#bootstrapdatatable tr").length+1 ; i++ ) {
            table.column(i).visible() === true ? '' : table.column(i).visible( true )
        }

        $('.checkColumn input:checkbox').prop('checked', true);
        $('#hideID').click();
        $('#hideDeleteRowButton').click();
        */
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


            $(this).find('td button').removeClass("btn-success");
            $(this).find('td.notfound').removeClass('notfoundColor');
            $(this).find('td button').addClass("btn-outline-success");
        } else {
            //удаляю у не выбранных кнопок класс
            table.$('tr.selected').find('td button').removeClass("btn-success");
            table.$('tr.selected').find('td button').addClass("btn-outline-success");

            //удаляю не выбранным и добавляю выбранной строке клас
            table.$('tr.selected').removeClass('selected');
            table.$('td.notfound').removeClass('notfoundColor');
            $(this).addClass('selected');
            $(this).find('td.notfound').addClass('notfoundColor');

            //добавляю выбранной кнопке класс
            $(this).find('td button').removeClass("btn-outline-success");
            $(this).find('td button').addClass("btn-success");
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
    $(".relativeDate button").click(function () {
        CurrentOrNotDate = parseInt($(this).val())
        typeDate = $(this).attr('name')
        
        var minDate = moment().subtract(CurrentOrNotDate, typeDate).startOf(typeDate).format('YYYY-MM-DD');
        var maxDate = moment().subtract(CurrentOrNotDate, typeDate).endOf(typeDate).format('YYYY-MM-DD');
        
        $("#minDate").val(minDate);
        $("#maxDate").val(maxDate);
    });
    
    $("body").css("opacity", 1);
});





