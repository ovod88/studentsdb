
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
                            initEditStudentPage();

                		}

                    }

                    if(row_count > length || length == 0)  {

                    	$button.hide()
                    	$button.off('click');
                    	$(window).off('scroll');
                    
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
	
});