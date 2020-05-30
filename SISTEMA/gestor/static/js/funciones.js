
/* RESERVAS.HTML */

$('#submitBtn').click(function pruebaFunciones() {
  
  /* when the button in the form, display the entered values in the modal */
  $('#Productor').text($('#productor').text());
  $('#Chacra').text($('select[name=chacra] option').filter(':selected').text());
  $('#Producto').text($('select[name=producto] option').filter(':selected').text());
  $('#Fecha').text($('#fecha').val());
  $('#Hora').text($('#hora').val());
  $('#Observaciones').text($('#observaciones').val());
});


$('#submit').click(function(){
  /* when the submit button in the modal is clicked, submit the form */
  $('#forms').submit();
  AvisoFinal();
});

function AvisoFinal() {
  alert('Solicitud realizada');
}

    /* RESERVAS_OP */

    $("#id_productor").change(function () {
      var url = $("#ReservaOperForm").attr("data-chacras-url");
      var productorId = $(this).val();

      $.ajax({
        url: url,
        data: {
          'productor': productorId
        },
        success: function (data) {
          $("#id_chacra").html(data);
        }
      });

    });
