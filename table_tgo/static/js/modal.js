 //ДОБАВЛЕНИЕ и ИЗМЕНЕНИЕ
 $(".modalButton").each(function () {
    $(this).modalForm({formURL: $(this).data("form-url")});
});
    
    
//УДАЛЕНИЕ
$(".delete").each(function () {
    $(this).modalForm({formURL: $(this).data("form-url"), isDeleteForm: true});
});