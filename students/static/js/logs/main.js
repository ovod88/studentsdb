$(function(){

	logSizeHandler();
	toggleFilter();
	
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

function getLogs() {

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

				console.log($new_navigation);

				if($cur_navigation.length && $new_navigation.length) {

					$cur_navigation.hide().html($new_navigation.html()).fadeIn('slow');

				} else if($cur_navigation && !$new_navigation.length) {

					// alert('HERE');

					$cur_navigation.remove();
 
				} else {

					// alert('HERE2');
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

function activateSelectFilter($filter_window, run) {

	let $filter_window_select = $filter_window.find('.filter-window-select'), 
		$filter_window_select_main = $filter_window_select.find('.filter-window-select-main'),
		$filter_window_select_list = $filter_window_select.find('.filter-window-select-box'),
		$filter_window_select_options = $filter_window_select_list.find(".filter-window-select-box-options li"),
		$document = $(document);

	if(run) {

		$filter_window_select_main.on("click", function () {

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

	            let option_selected = $(this).find('.text').text().trim();

	            $.each($filter_window_select_options, function () {

	                let option = $(this).text().trim();

	                if (option === option_selected)

	                    $(this).addClass("active");

	                else

	                    $(this).removeClass("active");

	            });
			}

			$filter_window_select_list.toggleClass("active");

		});

		$filter_window_select_options.on("click", function () {

			var option = $(this).html();

			$filter_window_select_main.find('.text').html(option);
			$filter_window_select_list.removeClass("active");

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

function configureFilterOptions($filter_window) {

	let $filter_window_select = $filter_window.find('.filter-window-select'),
		$button_delete = $filter_window.find('.button-delete'),
		$apply_button = $filter_window.find('.apply-button');

	if($filter_window.is(':visible')) {

		if($filter_window_select.length) {

			activateSelectFilter($filter_window, true);

		}

		$button_delete.on('click', function() {

			alert('DELETE');

		});

		$apply_button.on('click', function() {

			alert('APPLY');

		});

	} else {

		if($filter_window_select.length) {

			activateSelectFilter($filter_window, false);

		}

		$button_delete.off();
		$apply_button.off();

	}

}

function toggleFilter() {

	let $filter_icon = $('.filter-icon'),
		$filter_window_select_main = $('.filter-window-select-main');

	$filter_icon.click(function() {

		let $filter_window = $(this).siblings('.filter-window');

		$filter_window.slideToggle('300', function() {

			configureFilterOptions($filter_window);

		});

	});

}