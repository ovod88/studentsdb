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
  var $waiter = $('.waiter'),
      $waiter_to_modal = $waiter.clone().removeAttr('style'),
      $inputs = form.find('input'),
      $select = form.find('select'),
      $textarea = form.find('textarea'),
      $modal_title = modal.find('.modal-title'),
      $modal_body = modal.find('.modal-body'),
      $modal_footer = modal.find('.modal-footer');

  $waiter_to_modal.appendTo(modal.find('.modal-body'));

  form.find('input[name="cancel_button"]').click(function(event){

    event.preventDefault();
    modal.modal('hide');

  });

  var $url = form.attr('action');

  form.ajaxForm({
    dataType : 'html',
    beforeSend: function( xhr ) {
      
      $waiter_to_modal.animate({
        opacity: 1
      }, 100);
      $inputs.prop('disabled', true);
      $select.prop('disabled', true);
      $textarea.prop('disabled', true);
    },
    error : function(){

      setTimeout(function() {

        $waiter_to_modal.animate({
          opacity: 0
        }, 100, function() {

          $inputs.prop('disabled', false);
          $select.prop('disabled', false);
          $textarea.prop('disabled', false);
          $modal_footer.html('<p class="alert-danger">Помилка i на сервері. Спробуйте будь-ласка пізніше.</p>');
          
          setTimeout(function() {
            $modal_footer.html('');
          }, 3000);

        });

      }, 4000);

    },
    success  : function(data, status, xhr) {

      setTimeout(function() {

        var html = $(data), 
        newform = html.find('#content-column form');
    
        $modal_body.html(html.find('.alert'));
        $modal_footer.html('');

        // console.log(html);

        if ( !newform.hasClass('delete-students') && newform.length > 0) {
          
          $modal_body.append(newform);

          initEditStudentForm(newform, modal);

        } else {

          setTimeout(function(){
            
            location.reload(true);

          }, 2000);

        }

      }, 3000);

    }

  });

}

function changeBrowserURL(dom_element) {
  // Change URL with browser address bar using the HTML5 History API.
  if (history.pushState) {
    // Parameters: data, page title, URL
    history.pushState(null, null, dom_element.href);
  }
  // Fallback for non-supported browsers.
  else {
    document.location.hash = dom_element.getAttribute("href");
  }
}

function getPageHtml(url, callback) {
  
  var xhr = new XMLHttpRequest();
  xhr.open("GET", url, true);
  xhr.send();


  xhr.onreadystatechange = function() {

    if (xhr.readyState != 4) return;
      if (xhr.status != 200) {
        callback(xhr.status);
      } else {
        callback(null, xhr.responseText);
      }

    }

}

function initEditStudentPage(event) {
  console.log('INITIATED STUDENT PAGE');
  $('a.student-edit-form-link').click(function(event){
    event.preventDefault();
    var $link = $(this),
        $loader_wrapper = $('.loader-wrapper'),
        modal = $('#myModal'); 

    // console.log('CLICKED');
    // console.log($link[0].getAttribute('href'));

    $loader_wrapper.fadeIn('slow'); 

    setTimeout(function() {

        changeBrowserURL($link[0]);

        // getModal($link, $loader_wrapper, modal);

        getPageHtml($link.attr('href'), function(error, html) {

          if(error) {

            $loader_wrapper.fadeOut(100, function() {

              modal.find('.modal-body').html('<p class="alert-danger">Помилка error на сервері. Спробуйте будь-ласка пізніше.</p>');
              modal.find('.modal-footer').html('');
              modal.find('.modal-title').html('');
              modal.modal({
                'keyboard': false,
                'backdrop': false,
                'show': true
              });

            });

          } else {

            $loader_wrapper.fadeOut(100, function() {

              var $html = $(html), 
                  form_html = $html.find('#content-column form');


              modal.find('.modal-title').html($html.find('#content-column h2').text());
              modal.find('.modal-body').html(form_html);

              initEditStudentForm(form_html, modal);

              modal.modal({
                'keyboard': false,
                'backdrop': false,
                'show': true
              }); 

            });

          }

        });

    }, 3000);

  });

}

function popStateHandler() {
  // FF, Chrome, Safari, IE9.
  if (history.pushState) {

    // window.onpopstate = function (){
    //     alert(location.href);
    // }

    window.addEventListener("popstate", function(e) {

      // alert(location.href);

      getPageHtml(location.href, function(error, html) {

        if(error) {

          return;

        } else {

          var html_tag = document.getElementsByTagName("html")[0];
          html_tag.innerHTML = html;
          init();

        }

      });

    });
  }
}

function loadJournalPage() {

  $('#journal').click(function(event){

    var $loader_wrapper = $('.loader-wrapper'),
        $link = $(this);

    $('.main-nav li').removeClass('active');
    $('#journal').addClass('active');

    event.preventDefault();

    $loader_wrapper.fadeIn('slow');

    setTimeout(function() {

      $.ajax({
        url      : $link.find('a').attr('href'),
        method   : "GET",
        dataType : "html"
      }).then(function(data, status, xhr) {

        var $html = $(data),
            $body = $('body'),
            $scripts = $html.filter('#scripts').find('script').not('.common-script');



        $loader_wrapper.fadeOut('slow');

        // console.log($html);
        // console.log($html.filter('#scripts').find('script'));

        if (status != 'success') {
          
          $loader_wrapper.fadeOut(100, function() {

            alert('Error on server');
            return;
          }); 

        }

        $('#content-columns').html($html.find('#content-columns').html());
        $body.append($html.find('.pagination-nav'));

        $('link').not(".common").remove();
        $('head').append($html.filter('link').not(".common"));

        $body.find('#scripts script').not('.common-script').remove();
        $body.append($scripts);

        initEditStudentPage();

      }, function(xhr, status, error) {

        $loader_wrapper.fadeOut(100, function() {

          alert('Error on server');

        }); 

      });

}, 3000);

  })


}

function init() {

  setGroupSelector();
  initEditStudentPage();
  loadJournalPage();

}

$(function(){

  popStateHandler();
  init();
  // initDatePicker();

});