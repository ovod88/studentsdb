$(function(){
	let ajax_page = 1;
	$button = $('.load_more_button');

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

                    		console.log(data.students);


                    		students = _.template($(student_tmpl).html()) (data);

                    		$('.table > tbody').append(students);

                    } else {

                    	$button.hide()
                    
                    }

                },
                function (errorXHR) {

                    console.log(errorXHR)

                });

	});
});