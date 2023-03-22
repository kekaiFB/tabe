$(document).ready(function(){
    
    var loadForm = function () { 
      var btn = $(this);
      $.ajax({
        url: btn.attr("data-url"),
        type: 'get',
        dataType: 'json',
        beforeSend: function () {
          $("#modal-product .modal-content").html("");
          $("#modal-product").modal("show");
        },
        success: function (data) {
          $("#modal-product .modal-content").html(data.html_form);
        },
      
      });
    };
   

    var saveForm = function () {
      var form = $(this);
      $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        success: function (data) {
          if (data.form_is_valid) {
            location.reload();
          }
          else {
            $("#modal-product .modal-content").html(data.html_form);
          }
        }
      });
      return false;
    };

     // Add product
     $(".addSpan").on("click", loadForm);
     $("#modal-product").on("submit", ".js-product-update-form", saveForm);


    // Update product
    $("#bootstrapdatatable").on("click", ".editSpan", loadForm);
    $("#modal-product").on("submit", ".js-product-add-form", saveForm);
  });