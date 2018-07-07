
/* THIS SCRIPT IS MIXED FOR TWO CASES - ONE - FOR BUTTON load more AND SECOND FOR SCROLL EVENT*/
$(function(){
	let ajax_page = 1,
		$button = $('.load_more_button'),
		$student_table = $('.table'),
		$student_template = $(student_tmpl),
		row_count = $student_table.find('tbody tr').length,
		row_num = row_count,
		full_url = window.location.href,
		post_url = full_url.substring(full_url.lastIndexOf('/'), full_url.length),
        $daybox = $('.day-box > input'),
        $alert_message = $('.alert');

	if($student_table.length) {
		$button.on('click', function (e) {

			e.preventDefault();
			send_post(post_url);

		});


		function send_post(url) {

			ajax_page++;
			$.ajax({	
					url      : url,
                    method   : "POST",
                    data     : {"load_more": true, "ajax_page": ajax_page},
                    dataType : "json"
                }).then(function (data){

                	let length = data.students.length;

                    if(length > 0) {

                    	for(let i = 0; i < length; i++) {

                    		row_num++;
                    		student = data.students[i];

                			student_html = _.template($student_template.html()) ({'student': student, 
                																'row_num': row_num});

                			student_html = student_html.replace(/\/students\/(\d+)\/(\w+)/g, 
                									'/students/' + student.id + '/$2');
                			// student_html = student_html.replace(/\/journal\/(\d+)/g, 
                			// 						'/journal/' + student.id);

                			$(student_html).appendTo($('.table > tbody')).show('slow');

                		}

                    }

                    if(row_count > length || length == 0)  {

                    	$button.hide()
                    	$button.off('click');
                    
                    }

                },
                function (errorXHR) {

                    console.log(errorXHR)

                });

		}
	}

    function hideMessage() {

        $alert_message.hide('slow');
        timer = setTimeout(hideMessage, 10000)

    }

    $daybox.change(function() {

            // $alert_message.stop(false, true).animate({
            //     opacity: 1
            // }, 400).delay(5000)
            //        .animate({
            //     opacity: 0
            // }, 400);

            

    });
	
});