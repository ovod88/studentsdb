
/* THIS SCRIPT IS MIXED FOR TWO CASES - ONE - FOR BUTTON load more AND SECOND FOR SCROLL EVENT*/
$(function(){
	let ajax_page = 1,
		$button = $('.load_more_button'),
		$student_table = $('.table'),
		row_height = $student_table.find('tbody tr').first().height(),
		$student_template = $(student_tmpl),
		row_count = $student_table.find('tbody tr').length,
		row_num = row_count,
		full_url = window.location.href,
		post_url = full_url.substring(full_url.lastIndexOf('/'), full_url.length);

    initEditStudentPage();

	if($student_table.length) {
		$button.on('click', function (e) {

			e.preventDefault();
			send_post(post_url);

		});

		$(window).on('scroll', scrollEventHadler);

		if(window.innerHeight > document.body.offsetHeight) {

			send_post(post_url);

		}

		function scrollEventHadler(e) {

			if((window.innerHeight + window.scrollY) >= document.body.offsetHeight) {

				send_post(post_url);

			}

		}

		function send_post(url) {

			ajax_page++;
			$.ajax({	
					url      : url,
                    method   : "POST",
                    data     : {"load_more": true, "ajax_page": ajax_page,
                				'csrfmiddlewaretoken' : $('input[name="csrfmiddlewaretoken"]').val()
                				},
                    dataType : "json"
                }).then(function (data){

                	let length = data.students.length;

                    if(length > 0) {

                    	for(let i = 0; i < length; i++) {

                    		row_num++;
                    		// console.log('NUMBER ->' + row_num);
                    		student = data.students[i];
                			student_html = _.template($student_template.html()) ({'student': student, 
                																'row_num': row_num});

                			student_html = student_html.replace(/\/students\/(\d+)\/(\w+)/g, 
                									'/students/' + student.id + '/$2');
                			student_html = student_html.replace(/\/journal\/(\d+)/g, 
                									'/journal/' + student.id);

                			$(student_html).appendTo($('.table > tbody')).show('slow');

                		}

                    }

                    initEditStudentPage();

                    if(row_count > length || length == 0)  {

                    	$button.hide()
                    	$button.off('click');
                    	$(window).off('scroll');
                        initEditStudentPage();
                    
                    }

                    if(length != 0) {
                    	if(window.innerHeight > document.body.offsetHeight) {

							send_post(post_url);

						}
                    }

                },
                function (errorXHR) {

                    console.log(errorXHR)

                });

		}
	}
	
    // initEditStudentPage();
});


function initEditStudentPage(event) {
  // console.log('INITIATED STUDENT PAGE');

  $('a.student-edit-form-link').off('click');

  $('a.student-edit-form-link').click(function(event){
    event.preventDefault();
    var $link = $(this),
        $loader_wrapper = $('.loader-wrapper'),
        modal = $('#myModal'); 

    // console.log('CLICKED');
    // console.log($link[0].getAttribute('href'));

    $loader_wrapper.fadeIn('slow'); 

    setTimeout(function() {

        // console.log(location.href);

        // getModal($link, $loader_wrapper, modal);

        getPageHtml($link.attr('href'), function(error, html) {

          changeBrowserURL($link[0]);

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

              // alert('HERE');
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
            
            var State = History.getState();
            location.href = State.url;//REDIRECT TO PREVIOUS PAGE (URL IS STORED IN STATE WHILE PUSHSTATE)

          }, 2000);

        }

      }, 3000);

    }

  });

}
