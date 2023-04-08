 //ДОБАВЛЕНИЕ
 $(".create_tgo").each(function () {
    $(this).modalForm({formURL: $(this).data("form-url")});
 });

 $(".add_tgo_object").each(function () {
    $(this).modalForm({formURL: $(this).data("form-url")});
 });

 $(".add_tgo_object_resource").each(function () {
       $(this).modalForm({formURL: $(this).data("form-url")});
 });


 //ИЗМЕНЕНИЕ
 $(".edit").each(function () {
    $(this).modalForm({formURL: $(this).data("form-url")});
 });

 $(".edit_tgo_object").each(function () {
    $(this).modalForm({formURL: $(this).data("form-url")});
 });

$(".edit_resource").each(function () {
    $(this).modalForm({formURL: $(this).data("form-url")});
 });


 //УДАЛЕНИЕ
 $(".delete_tgo_object").each(function () {
    $(this).modalForm({formURL: $(this).data("form-url"), isDeleteForm: true});
});

$(".delete_resource_object").each(function () {
 $(this).modalForm({formURL: $(this).data("form-url"), isDeleteForm: true});
});