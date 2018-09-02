function setGroupSelector() {

  $('#group-selector select').change(function(event){

      var group_id = $(this).val();
      group_id = group_id.replace(/\s/g, '')
      
      if (group_id) {

        Cookies.set('current_group', group_id, {'path': '/', 'expires': 365});

      } else {

        Cookies.remove('current_group', {'path': '/'});

      }

      location.reload(true);
    });

}

function initDatePicker() {

  var $date_input_bt = $('button.dateinput'),
        $input_date = $('.input-group input');

    $date_input_bt.on('click', function() {

      $input_date.datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
        language: 'uk'
      }).focus();

  });

}

function initEditStudentForm(form, modal) {

  initDatePicker();

  form.find('input[name="cancel_button"]').click(function(event){

    event.preventDefault();
    modal.modal('hide');

  });

  form.ajaxForm({
    dataType : 'html',
    error    : function(){

      alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
      return;

    },
    success  : function(data, status, xhr) {

      var html = $(data), 
          newform = html.find('#content-column form');
    
      modal.find('.modal-body').html(html.find('.alert'));

      // console.log(newform);

      if ( !newform.hasClass('delete-students') && newform.length > 0) {
        
        modal.find('.modal-body').append(newform);

        initEditStudentForm(newform, modal);

      } else {

        setTimeout(function(){location.reload(true);}, 2000);

      }

    }

  });

}


function initEditStudentPage(event) {

  $('a.student-edit-form-link').click(function(event){
    event.preventDefault();
    var $link = $(this);

    $.ajax({
      url      : $link.attr('href'),
      method   : "GET",
      dataType : "html"
    }).then(function(data, status, xhr) {

      if (status != 'success') {
        
        alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
        return;

      }

      var modal = $('#myModal'), 
          html = $(data), 
          form_html = html.find('#content-column form');
      
      // console.log(data);

      modal.find('.modal-title').html(html.find('#content-column h2').text());
      modal.find('.modal-body').html(form_html);

      initEditStudentForm(form_html, modal);

      modal.modal({
        'keyboard': false,
        'backdrop': false,
        'show': true
      });

    }, function() {

      alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');

    });

  });

}

$(function(){

  setGroupSelector();
  initEditStudentPage();
  // initDatePicker();

});