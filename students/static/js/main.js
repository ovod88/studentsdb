$(function(){
	let ajax_page = 1;
	$button = $('.load_more_button');
	$student_template = $(student_tmpl);

	$button.on('click', function (e) {

		ajax_page++;
		e.preventDefault();
		$.ajax({	
					url      : "/",
                    method   : "POST",
                    data     : {"load_more": true, "ajax_page": ajax_page},
                    dataType : "json"
                }).then(function (data){

                	let length = data.students.length;


                    if(length > 0) {

                    	for(let i = 0; i < length; i++) {

                    		student = data.students[i];
                			student_html = _.template($student_template.html()) ({'student': student});

                			student_html = student_html.replace(/\/students\/(\d+)\/(\w+)/g, 
                									'/students/' + student.id + '/$2');
                			student_html = student_html.replace(/\/journal\/(\d+)/g, 
                									'/journal/' + student.id);

                			$(student_html).appendTo($('.table > tbody')).show('slow');

                		}

                    } else {

                    	$button.hide()
                    
                    }

                },
                function (errorXHR) {

                    console.log(errorXHR)

                });

	});
});