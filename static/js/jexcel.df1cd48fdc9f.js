$(document).ready(function () {

    //Берем нашу HTML таблицу и конвертируем в 2d массив    
    var myTableArray = [];
    $("table#current_tgo tr").each(function() {
        var rowDataArray = [];
        var actualData = $(this).find('td');
        if (actualData.length > 0) {
            actualData.each(function() {
                rowDataArray.push($(this).html());
            });
            myTableArray.push(rowDataArray);
        }
    });
    

    var cell_pos, link_pos = 0;
    var value = []
    var new_cellName = '';
    var time_start_cellName_arr = [];

    var rowOp = []

    var loaded = function(instance) {
        updateMyTable()
    }

    var options = {
        data: myTableArray,
        columns: [
            { type:'text', width: 50, readOnly:true,},
            { type:'html', width: 300, readOnly:true, align: 'left'},
            { type:'html', width: 150, readOnly:true, align: 'left'},
            { type:'text', width: 100, readOnly:true,},
            { type:'text', width: 80, mask:'0:00'},
            { type:'text', width: 100, mask:'0:00'},
            { type:'text', width: 140, mask:'0:00'},
            { type:'text', width: 150, readOnly:true, align: 'left'},
    
            
            { type:'text', width: 100, readOnly:true,},
            { type:'text', width: 100, readOnly:true,},
            { type:'text', width: 100, readOnly:true,},
        ],
    
        nestedHeaders:[
            [
                {
                    title: 'Пункт',
                    colspan: '1',
                },
                {
                    title: 'Операция',
                    colspan: '1',
                },
                {
                    title: 'Ресурс',
                    colspan: '1',
                },
                {
                    title: 'Количество',
                    colspan: '1',
                },
                {
                    title: 'Начало',
                    colspan: '1',
                },
                {
                    title: 'Окончание',
                    colspan: '1',
                },
                {
                    title: 'Продолжительность',
                    colspan: '1',
                },
                {
                    title: 'Подразделения',
                    colspan: '1',
                },
            ],
        ],
    
    
        toolbar:[
            {
                type: 'i',
                tooltip: 'На главную',
                content: 'arrow_back',
                onclick: function () {
                    goUrlIndex()
                }
            },
            {
                type: 'i',
                tooltip: 'Добавить операцию',
                content: 'add_box',
                onclick: function () {
                    addOperation()
                }
            },
    
            {
                type: 'i',
                tooltip: 'Назад',
                content: 'undo',
                onclick: function() {
                    myTable.undo();
                }
            },
            {
                type: 'i',
                tooltip: 'Вперед',
                content: 'redo',
                onclick: function() {
                    myTable.redo();
                }
            },
            {
                type: 'i',
                tooltip: 'Сохранить время',
                content: 'save',
                onclick: function () {
                    saveTime()
                }
            },
            {
                type: 'i',
                tooltip: 'Сохранить в PDF',
                content: 'picture_as_pdf',
                onclick: function () {
                    picture_as_pdf()
                }
            },
        ],
    
    
        updateTable:function(instance, cell, col, row, val, label, cellName) {
            cell.style.color = 'black'
    
            //выделяем операции особым цветом
            if (col == 1) {
                if( cell.innerText != '' && cell.innerText != 'Окончание')
                {
                    rowOp.push(row)
                    cell.style.backgroundColor = '#edf3ff';
                }
            }
    
            //выделяем подразделения для операций особым цветом
            if (rowOp.indexOf(row) != -1) {
                if (col == 7) {
                    cell.style.backgroundColor = '#edf3ff';
                }
            }
    
            //выделяем окончание особым цветом
            if (label == 'Окончание') {
                cell.style.backgroundColor = '#f46e42';
                cell.style.color = '#ffffff';
            }
    
            
            //выделяем колонки со временем особым цветом
            if(col == 4 || col == 5 || col == 6){
                cell.style.backgroundColor = '#FFFFE0'
                
                //если время является формулой
                if (val[0] == '=')
                {
                    //те что не являются формулой все будут белым цветом
                    cell.style.backgroundColor = '#FFFFFF'

                    //колонки которые ссылаются на будущие строки
                    value = val.replaceAll('=', '+').split('+')
                    value.shift()
                    for (var i=0; i<value.length; i++)
                    {   
                        cell_pos = parseInt(cellName.replace(/[^.\d]/g, ''))
                        link_pos = parseInt(value[i].replace(/[^.\d]/g, ''))
                        if (link_pos > cell_pos)
                        {
                            cell.style.backgroundColor = '#D8BFD8'
                        }
                    }
                }  
            }

             //колонки НАЧАЛО которые ссылаются на конец РОДИТЕЛЕЙ
             if(col == 4 ){
                new_cellName = 'D' + cellName.substr(1);
                time_start_cellName_arr.push(new_cellName)
            }
          

        },    
        onafterchanges: loaded,
        columnSorting: false,
        autoIncrement: true,
        license: 'NTg4NGU4ZGVjYjk2ODNlZGM2YzM4OWM1NWJjM2Y4NmYzZGMxODU2NDYwOGRkNDg2NzM4MWU2YmNkZWRlN2UyMjAxMTcyYjIxNDkyNGM2NjdlNzg1Y2QwY2I0ZWIzZmQ0YTRiMzI1OTU4OTkzMWMwYzNjMzA4MWY4ODAzYjEwMWMsZXlKdVlXMWxJam9pU25Od2NtVmhaSE5vWldWMElpd2laR0YwWlNJNk1UWTRNVEkxT1RZMU55d2laRzl0WVdsdUlqcGJJbXB6Y0hKbFlXUnphR1ZsZEM1amIyMGlMQ0pqYjJSbGMyRnVaR0p2ZUM1cGJ5SXNJbXB6YUdWc2JDNXVaWFFpTENKamMySXVZWEJ3SWl3aWJHOWpZV3hvYjNOMElsMHNJbkJzWVc0aU9pSXpJaXdpYzJOdmNHVWlPbHNpZGpjaUxDSjJPQ0lzSW5ZNUlpd2lZMmhoY25Seklpd2labTl5YlhNaUxDSm1iM0p0ZFd4aElpd2ljR0Z5YzJWeUlpd2ljbVZ1WkdWeUlpd2lZMjl0YldWdWRITWlMQ0pwYlhCdmNuUWlMQ0ppWVhJaUxDSjJZV3hwWkdGMGFXOXVjeUlzSW5ObFlYSmphQ0pkTENKa1pXMXZJanAwY25WbGZRPT0=',
    }
    
    var myTable = jspreadsheet(document.getElementById('spreadsheet'), options);
    
    //скрываем по умолчанию столбцы с TableName и ID
    myTable.hideColumn(10);
    myTable.hideColumn(9);
    myTable.hideColumn(8);
   
    draw_tgo_table(myTable)
    var length = myTable.getColumnData([0]).length

    function updateMyTable(){
        for (let i = 0; i < length; i++) {
            //ячейки со временем, которые являются родителями 
            res = myTable.getValue(time_start_cellName_arr[i]);
            if (res == '')
            {
                //если время является формулой
                if (myTable.getRowData([i])[4][0] == '=')
                {
                    //если ячейки на которые они ссылаются тоже родители
                    var parent = 'D' + myTable.getRowData([i])[4].substr(2)
                    parent = myTable.getValue(parent)
                    if (parent == '')
                    {
                        var time = 'E' + time_start_cellName_arr[i].substr(1);
                        myTable.getCell(time).style["backgroundColor"] = '#E0FFFF'
                    } 
                }  
            } else //дочерние ячейки
            {
                //если время является формулой
                if (myTable.getRowData([i])[4][0] == '=')
                {   
                     //ячейки на которые они ссылаются
                    var parent = 'D' + myTable.getRowData([i])[4].substr(2)
                    parent = myTable.getValue(parent)
               
                    //ячейки на которые они ссылаются тоже родители
                    if (parent == '')
                    {
                        //Пункты строк, если они будут равны, значит дочерние ссылаются на СВОИ родительские
                        var punkt_parent =  'A' + myTable.getRowData([i])[4].substr(2)
                        var punkt_child = myTable.getRowData([i])[0]

                        //если ячейки на которые они ссылаются ИХ родители
                        if (punkt_child[0] == myTable.getValue(punkt_parent))
                        {
                            var start_time_color = 'E' + time_start_cellName_arr[i].substr(1);
                            var end_time_color = 'F' + time_start_cellName_arr[i].substr(1);
                            var lenght_time_color = 'G' + time_start_cellName_arr[i].substr(1);
                            childColor(myTable, start_time_color)
                            childColor(myTable, end_time_color)
                            childColor(myTable, lenght_time_color)
                        }                
                    } 
                }    
            }
        }

    }
    function childColor(table, child){
        if (table.getCell(child).style["backgroundColor"] != 'rgb(216, 191, 216)')
            table.getCell(child).style["backgroundColor"] = '#91DFAB'
    }

    updateMyTable()

    //Сохраняем время в БД
    function saveTime() {
        if ($(".requestUser").val() == $( "input[name='author']" ).val())
        {
            var tgo_ogject_update = []; 
        var update_tgoObj_arr = [];
        var update_res_arr = [];
        var res = [];
        
        for (let i = 0; i < length; i++) { 
            res = myTable.getRowData([i]);
            tgo_ogject_update.push([res[8], res[9], res[10], res[4], res[5], res[6]])
        }
        for (let i = 0; i < length; i++) { 
            //получаем массив tgo_obj которые надо обновить
            if (tgo_ogject_update[i][1] == "table_tgo_tgo_object"){
                update_tgoObj_arr.push( tgo_ogject_update[i] )
            }
    
            //получаем массив res_obj которые надо обновить
            if (tgo_ogject_update[i][1] == "table_tgo_ressourceoperation"){
                update_res_arr.push( tgo_ogject_update[i] )
            }
        }
    
        $.ajax({             
            url: '/table_tgo/ajax_update_tgo',
            method : "post",
            dataType : "json",
            data: {
                'update_tgoObj_arr': update_tgoObj_arr, 
                'update_res_arr': update_res_arr,  
              },                
    
            success: function () {  
                console.log('success!')
            }
          });
        }
    }
    
    
    //кнопка Назад
    function goUrlIndex() {
        $("#urlIndex").click();
    }
    
    function addOperation() {
        if ($(".requestUser").val() == $( "input[name='author']" ).val())
            $(".add_tgo_object").click();
    }


    //convert to pdf
    function picture_as_pdf() {
        
        $('#instructions, .jexcel_toolbar, .delete,  .modalButton').attr('data-html2canvas-ignore', 'true');
        var elem = $('#body-to-pdf');
        html2canvas(document.body, {
            scrollY: 0}).then(function(canvas) {
           var data = canvas.toDataURL();
            var docDefinition = {
                info: {  title:  $('#title').text() },
                content: [
                    {
                        image: data,
                        width: 600,
                    }
                ]
            };
            pdfMake.createPdf(docDefinition).open();
        });
    }


    //Инструкции
    $('.instructionsButton').on('click', function () {
        $(".instructions").hide();
    });

    


    //ДОБАВЛЕНИЕ и ИЗМЕНЕНИЕ
    $(".modalButton").each(function () {
        $(this).modalForm({formURL: $(this).data("form-url")});
    });
        
        
    //УДАЛЕНИЕ
    $(".delete").each(function () {
        $(this).modalForm({formURL: $(this).data("form-url"), isDeleteForm: true});
    });
});

