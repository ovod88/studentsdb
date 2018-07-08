
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
        $ajax_message_indicator_ok = $alert_message.find('#ajax-progress-indicator-ok'),
        $ajax_message_indicator_nok = $alert_message.find('#ajax-progress-indicator-nok'),
        pulsateInterval,
        ajax_response_reaction_timeout = null;

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

            console.log('CALLED HERE' + date);
            ajax_settings = {
                url      : url,
                type     : "DELETE",
                data     : {"date" : date},
                dataType : "json"
            }

        }

        $.ajax(ajax_settings).then(function (data){

                if(ajax_response_reaction_timeout) {

                    clearTimeout(ajax_response_reaction_timeout);

                }

                if(data.status == 'ok') {

                    ajax_response_reaction_timeout = setTimeout(function() {
                    
                        startIndicatorMessageTimeout($ajax_message_indicator_ok)

                    }, 1500);

                } else {

                    ajax_response_reaction_timeout = setTimeout(function() {
                    
                        startIndicatorMessageTimeout($ajax_message_indicator_nok)

                    }, 1500);

                }

            },
                function (errorXHR) {

                    if(ajax_response_reaction_timeout) {

                        clearTimeout(ajax_response_reaction_timeout);

                    }


                    ajax_response_reaction_timeout = setTimeout(function() {

                        stopPulsateMessage();
                        $ajax_message_indicator.fadeOut();
                        $ajax_message_indicator_error.text('Error returned with code ' + errorXHR.status).fadeIn('slow');

                    }, 1500);

                }
                
            );

    }

    function startIndicatorMessageTimeout(elem) {

        stopPulsateMessage();

        $ajax_message_indicator.fadeOut(300, function() {

            elem.fadeIn(300, function() {

                $alert_message.delay(200)
                          .animate({
                                    opacity: 0
                                }, 300, function() {

                                    elem.fadeOut();

                                });

            });

        });

    }

    function startPulsateSaveMessage(elem) {

        pulsateInterval = setInterval(function() {

            if (elem.is(':visible')) {

                elem.fadeOut(300);

            } else {

                elem.fadeIn(300);

            }   

        }, 300);

    }

    function stopPulsateMessage() {

        clearInterval(pulsateInterval);

    }

    $daybox.change(function() {

            let $this = $(this),
                $date = $this.data('date'),
                $url = $this.data('url');

            // $ajax_message_indicator_error.finish();
            // $ajax_message_indicator.finish();
            // $ajax_message_indicator_nok.finish();
            // $ajax_message_indicator_ok.finish();
            $ajax_message_indicator_error.fadeOut();

            if($alert_message.css('opacity') == 0) {

                $alert_message.animate({opacity: 1}, 400, function() {

                    startPulsateSaveMessage($ajax_message_indicator);

                }); 

            } else {

                clearTimeout(ajax_response_reaction_timeout);

            }

            if($this.is(':checked')) {

                updateDaystatus($url, 'POST', $date);

            } else {
                
                updateDaystatus($url, 'DELETE', $date);

            };        

    });
	
});