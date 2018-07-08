
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
        $alert_message = $('.alert'),
        $ajax_message_indicator = $alert_message.find('#ajax-progress-indicator'),
        $ajax_message_indicator_error = $alert_message.find('#ajax-progress-indicator-error'),
        pulsateInterval;

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

    function updateDaystatus(url, method, date) {
        let ajax_settings = {};

        if(method == 'POST') {

            ajax_settings = {
                url      : url,
                method   : "POST",
                data     : {"date" : date},
                dataType : "json"
            }

        } else if(method == 'DELETE') {

            ajax_settings = {
                url      : url,
                type   : "DELETE",
                data     : {"date" : date},
                dataType : "json"
            }

        }

        $.ajax(ajax_settings).then(function (data){

                    if(data.status == 'ok') {

                        $alert_message.stop(false, true)
                                      .animate({
                                                    opacity: 0
                                                }, 400, function() {

                                                    stopPulsateMessage($ajax_message_indicator);

                                                });

                    }

                },
                function (errorXHR) {

                    stopPulsateMessage($ajax_message_indicator);
                    $ajax_message_indicator_error.animate({
                                                    opacity: 1
                                                }, 400);

                });

    }

    function startPulsateSaveMessage(elem) {

        pulsateInterval = setInterval(function() {

            if (elem.css('opacity') == 0) {

                elem.stop(false, true).animate({
                                opacity: 1
                            }, 400)

            } else {

                elem.stop(false, true).animate({
                                opacity: 0
                            }, 400)

            }   

        }, 500);

    }

    function stopPulsateMessage(el) {

        clearInterval(pulsateInterval);

    }

    $daybox.change(function() {

            let $this = $(this),
                $date = $this.data('date'),
                $url = $this.data('url');

            console.log($date);
            console.log($url);

            if($this.is(':checked')) {

                console.log('CHECKED');
                $alert_message.stop(false, true)
                              .animate({
                                    opacity: 1
                                }, 200, function() {

                                    startPulsateSaveMessage($ajax_message_indicator);
                                    // updateDaystatus($url, 'POST', $date);

                                });

            } else {

                console.log('UNCHECKED');
                $alert_message.stop(false, true)
                              .animate({
                                    opacity: 1
                                }, 200, function() {

                                    startPulsateSaveMessage($ajax_message_indicator);
                                    // updateDaystatus($url, 'POST', $date);

                                });


            }

            // $alert_message.stop(false, true).animate({
            //     opacity: 1
            // }, 400).delay(5000)
            //        .animate({
            //     opacity: 0
            // }, 400);

            

    });
	
});