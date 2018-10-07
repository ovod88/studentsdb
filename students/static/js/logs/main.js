$(function(){

	logSizeHandler();
	toggleFilter();
	initDatePicker();
	
});

function logSizeHandler() {

	$('#log-size').change(function(event){

		var page_size = $(this).val();

	    page_size = page_size.trim();
	      
	    if (page_size) {

	        Cookies.set('page_size', page_size, {'path': window.location.pathname, 'expires': 365});

	    } else {

	        Cookies.remove('page_size', {'path': window.location.pathname});

	    }

      getLogs();

	});

}

function initDatePicker() {

   	$('#date_filter_input').on('click', function() {

      $(this).datepicker({
        format: 'yyyy-mm-dd',
        autoclose: true,
        language: 'uk'
      }).focus();

  });

}

function getLogs() {

	// console.log('GET LOGS CALED');

	var $div_errors = $('div.alert'),
		$tbody = $('table tbody'),
		$cur_navigation = $('.pagination-nav');

	$.ajax({
		url      : window.location.href,
		method   : "GET",
        dataType : "html"
	})
		.then(
			function (data, status, xhr){

				var $new_tbody = $(data).find('tbody'),
					$new_navigation = $(data).find('.pagination-nav');

				$tbody.hide().html($new_tbody.html()).fadeIn('slow');

				// console.log($new_navigation);

				if($cur_navigation.length && $new_navigation.length) {

					// alert('PAGE HAS NAVIGATION BUT NEEDED TO BE UPDATED');
					$cur_navigation.hide().html($new_navigation.html()).fadeIn('slow');

				} else if($cur_navigation && !$new_navigation.length) {

					// alert('PAGE HAS NAVIGATION BUT NO NEED');
					$cur_navigation.remove();
 
				} else {

					// alert('PAGE HAS NO NAVIGATION BUT NEEDED');
					$new_navigation.insertBefore('#footer');

				}

				// $('#log-size').empty().html($(data).find('#log-size'));
				
			}, 
			function(xhr, status, error) {

				$div_errors.text('').text(xhr.status + ' ' + xhr.statusText);
				$div_errors.animate({opacity: 1}, 300).delay(5000)
							.animate({opacity: 0}, 100, function() {
								$(this).text('')
							});

			});

}

function ifFilterWithSelect($filter_icon, $filter_window, run) {

	let $filter_window_select = $filter_window.find('.filter-window-select'), 
		$filter_window_select_main = $filter_window_select.find('.filter-window-select-main'),
		$filter_window_select_list = $filter_window_select.find('.filter-window-select-box'),
		$filter_window_select_options = $filter_window_select_list.find(".filter-window-select-box-options li"),
		$document = $(document),
		$button_delete = $filter_window.find('.button-delete'),
		$apply_button = $filter_window.find('.apply-button');

		// alert($filter_icon);

	if(run) {

		$filter_window_select_main.on("click", function () {

			// console.log('CLICKED MAIN');
			// console.log($filter_window_select_list);

			if (!$filter_window_select_list.hasClass("active")) {

	            let windowHeight = $(window).outerHeight(),
	            	dropdownPosition = $(this).offset().top,
	            	dropdownHeight = 95;

	            if (dropdownPosition + dropdownHeight + 50 > windowHeight) {

	                $filter_window_select_list.addClass("drop-up");

	            }
	            else {

	                $filter_window_select_list.removeClass("drop-up");

	            }

	            // let option_selected = $(this).find('.text').text().trim();

	            // $.each($filter_window_select_options, function () {

	            //     let option = $(this).text().trim();

	            //     if (option === option_selected) {

	            //         $(this).addClass("active");

	            //     } else {

	            //         $(this).removeClass("active");

	            // 	}
	            
	            // });
			}

			$filter_window_select_list.toggleClass("active");

		});

		$filter_window_select_options.on("click", function () {

			var option = $(this).html();

			$filter_window_select_main.find('.text').html(option);
			$filter_window_select_list.removeClass("active");
			$(this).addClass('active');

		});

		$document.on('click', function (event) {

			if (!($(event.target).is($filter_window) || 
				$filter_window.find(event.target).length == 1)) {

				$filter_window_select_list.removeClass("active");

			}

		});

	} else {

		$filter_window_select_main.off();
		$filter_window_select_options.off();
		$document.off('click');

	}

}

function deactivateFilter($filter_icon, $filter_window) {

	let $filter_window_select = $filter_window.find('.filter-window-select');

	if($filter_window_select.length) {

		$filter_window_select.find('.filter-window-select-main').find('.text').html('Select');
		$filter_window_select.find('.filter-window-select-box').removeClass('active');
		$filter_window_select.find(".filter-window-select-box-options li").removeClass('active');

	}
	
	$filter_icon.removeClass('active');

}

function configureFilterOptions($filter_icon, $filter_window) {

	let $filter_window_select = $filter_window.find('.filter-window-select'),
		$button_delete = $filter_window.find('.button-delete'),
		$apply_button = $filter_window.find('.apply-button');

	if($filter_window.is(':visible')) {

		if($filter_window_select.length) {

			ifFilterWithSelect($filter_icon, $filter_window, true);

		}
		
		$button_delete.off('click');
		$button_delete.on('click', function() {

			if($filter_window_select.length) {

				// console.log('DEL INSIDE SELECT FILTER');

				$filter_window.slideUp('100', function() {

					ifFilterWithSelect($filter_icon, $filter_window, false);
					deactivateFilter($filter_icon, $filter_window);

					Cookies.remove('log_level', {'path': window.location.pathname});

					getLogs();
					
				});
				
			} else {

				// console.log('DEL INSIDE USUAL FILTER');
				$filter_window.slideUp('100', function() {

					let $input = $filter_window.find('input');

					Cookies.remove($input.data('cookie'), {'path': window.location.pathname});
					$input.val('');
					deactivateFilter($filter_icon, $filter_window);

					getLogs();

				});

			}

		});

		$apply_button.off('click');
		$apply_button.on('click', function() {

			if($filter_window_select.length) {

				$filter_window.slideUp('100', function() {

					ifFilterWithSelect($filter_icon, $filter_window, false);

					let option_selected = $filter_window_select.find('.filter-window-select-main').find('.text').html().trim();

					$.each($filter_window_select.find(".filter-window-select-box-options li"), function () {

	                	let option = $(this).text().trim();

		                if (option === option_selected) {

		                    Cookies.set('log_level', option_selected, {'path': window.location.pathname, 'expires': 365});
		                    $filter_icon.addClass('active');

		                }

	            	});

	            	$filter_window_select.find('.filter-window-select-box').removeClass('active');
	            	getLogs();

				});

			} else {

				$filter_window.slideUp('100', function() {

					let $input = $filter_window.find('input');

					// alert($input.val().trim());

					if($input.val().trim()) {

						Cookies.set($input.data('cookie'), $input.val(), {'path': window.location.pathname});
						$filter_icon.addClass('active');

					} else {

						$input.val('');
					
					}
					getLogs();
						
				});

			}

		});

	} else {

		if($filter_window_select.length) {

			ifFilterWithSelect($filter_icon, $filter_window, false);

		}

		$button_delete.off();
		$apply_button.off();

	}

}

function toggleFilter() {

	let $filter_icon = $('.filter-icon'),
		log_level_cookie = Cookies.get('log_level'),
		date_cookie = Cookies.get('date'),
		module_cookie = Cookies.get('module'),
		message_cookie = Cookies.get('message');

	if(log_level_cookie) {

		$('#filter-log-icon').addClass('active');
		$('#filter-log-select-main').find('.text').html(log_level_cookie);

		$.each($('#filter-log-select-box li'), function () {

                let option = $(this).text().trim();

                if (option === log_level_cookie) {

                	$('#filter-log-select-box li').removeClass('active');
                    $(this).addClass("active");

                }

            });

	} else if(date_cookie) {

		$('#filter-date-icon').addClass('active');
		$('#date_filter_input').val(date_cookie);

	} else if(module_cookie) {

		$('#filter-module-icon').addClass('active');
		$('#module_filter_input').val(module_cookie);

	} else if(message_cookie) {

		$('#filter-message-icon').addClass('active');
		$('#message_filter_input').val(message_cookie);

	}

	$filter_icon.click(function() {

		let $filter_window = $(this).siblings('.filter-window'),
			$filter_icon_clicked = $(this);

		$filter_window.slideToggle('300', function() {

			configureFilterOptions($filter_icon_clicked, $filter_window);

		});

	});

}