$(document).ready(function () {


    // DataTable
    var table = $('#tgoList').DataTable({
        "dom": 'fltipr',
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
       
        //---------------Конец Память фильторв конец-------------------

    
    
    });

    //Для главной страницы
    $('#formFilter').hide()
    $('#tgoList_length').text('')
    $('#tgoList_length').append($('#formFilter').html())



 
});

