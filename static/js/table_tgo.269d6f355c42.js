


$('#tgoList').DataTable({
    "ordering": false,
});


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

var rowOp = []
var options = {
    
    data: myTableArray,
    columns: [
        { type:'text', width: 100, readOnly:true,},
        { type:'text', width: 100, readOnly:true,},

        { type:'text', width: 50, readOnly:true,},
        { type:'html', width: 300, readOnly:true,},
        { type:'html', width: 150, readOnly:true,},
        { type:'text', width: 100, readOnly:true,},
        { type:'text', width: 80, mask:'0:00'},
        { type:'text', width: 100, mask:'0:00'},
        { type:'text', width: 140, mask:'0:00'},
        { type:'text', width: 150, readOnly:true },
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
    ],

    
    updateTable:function(instance, cell, col, row, val, label, cellName) {
        cell.style.color = 'black'

        //выделяем операции особым цветом
        if (col == 3) {
            if( cell.innerText != '' && cell.innerText != 'Окончание')
            {
                rowOp.push(row)
                cell.style.backgroundColor = '#edf3ff';
            }
        }

        //выделяем подразделения для операций особым цветом
        if (rowOp.indexOf(row) != -1) {
            if (col == 9) {
                cell.style.backgroundColor = '#edf3ff';
            }
           

        }


        //выделяем окончание особым цветом
        if (label == 'Окончание') {
            cell.style.backgroundColor = '#f46e42';
            cell.style.color = '#ffffff';
        }
    
        //выделяем колонки со временем особым цветом
        if(col == 6 || col == 7 || col == 8){
            cell.style.backgroundColor = '#FFFFE0'

            //если время является формулой
            if (val[0] == '=')
             {
                 cell.style.backgroundColor = '#f8f8ff'
             }  
        }
        
    },
    
  
    columnSorting:false,
    autoIncrement: true,
    license: 'NTg4NGU4ZGVjYjk2ODNlZGM2YzM4OWM1NWJjM2Y4NmYzZGMxODU2NDYwOGRkNDg2NzM4MWU2YmNkZWRlN2UyMjAxMTcyYjIxNDkyNGM2NjdlNzg1Y2QwY2I0ZWIzZmQ0YTRiMzI1OTU4OTkzMWMwYzNjMzA4MWY4ODAzYjEwMWMsZXlKdVlXMWxJam9pU25Od2NtVmhaSE5vWldWMElpd2laR0YwWlNJNk1UWTRNVEkxT1RZMU55d2laRzl0WVdsdUlqcGJJbXB6Y0hKbFlXUnphR1ZsZEM1amIyMGlMQ0pqYjJSbGMyRnVaR0p2ZUM1cGJ5SXNJbXB6YUdWc2JDNXVaWFFpTENKamMySXVZWEJ3SWl3aWJHOWpZV3hvYjNOMElsMHNJbkJzWVc0aU9pSXpJaXdpYzJOdmNHVWlPbHNpZGpjaUxDSjJPQ0lzSW5ZNUlpd2lZMmhoY25Seklpd2labTl5YlhNaUxDSm1iM0p0ZFd4aElpd2ljR0Z5YzJWeUlpd2ljbVZ1WkdWeUlpd2lZMjl0YldWdWRITWlMQ0pwYlhCdmNuUWlMQ0ppWVhJaUxDSjJZV3hwWkdGMGFXOXVjeUlzSW5ObFlYSmphQ0pkTENKa1pXMXZJanAwY25WbGZRPT0=',
}

var myTable = jspreadsheet(document.getElementById('spreadsheet'), options);

//скрываем по умолчанию столбцы с TableName и ID
myTable.hideColumn(1);
myTable.hideColumn(0);
var lenTable = myTable.getColumnData([0]).length

//Сохраняем время в БД
function saveTime() {
    var tgo_ogject_update = []; 
    var update_tgoObj_arr = [];
    var update_res_arr = [];
    var res = [];
    var length = myTable.getColumnData([0]).length

    
    for (let i = 0; i < length; i++) { 
        res = myTable.getRowData([i]);
        tgo_ogject_update.push([res[1], res[0], res[6], res[7], res[8]])
    }

    for (let i = 0; i < length; i++) { 
        //получаем массив tgo_obj которые надо обновить
        if (tgo_ogject_update[i][0] == "table_tgo_tgo_object"){
            update_tgoObj_arr.push( tgo_ogject_update[i] )
        }

        //получаем массив res_obj которые надо обновить
        if (tgo_ogject_update[i][0] == "table_tgo_ressourceoperation"){
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

//кнопка Назад
function goUrlIndex() {
    var url = $("#urlIndex").attr("data-url");
    document.location.href = url
}

//Связть с Ajax в проекте
function addOperation() {
    $(".add_tgo_object").click();
}

//Инструкции
$('.instructionsButton').on('click', function (e) {
    $(".instructions").hide();
});