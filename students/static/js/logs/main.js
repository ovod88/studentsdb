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

function toggleFilter() {

	let $filter_icon = $('.filter-icon'),
		$filter_window_select_main = $('.filter-window-select-main');

	$filter_icon.click(function() {

		let $filter_window = $(this).next('.filter-window'),
			$filter_window_select_main = $filter_window.find('.filter-window-select-main'),
			$filter_window_select_list = $filter_window.find('.filter-window-select-box'),
			$filter_log_level_options = $("#filter-log-level li");

		$filter_window.slideToggle('300', function() {

			if($filter_window.is(':visible')) {

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

			            var level_selected = $(this).find('text').text().trim();

			            $.each($filter_log_level_options, function () {

			                var level = $(this).text().trim();

			                if (level === level_selected)

			                    $(this).addClass("active");

			                else

			                    $(this).removeClass("active");

			            });
        			}

        			$filter_window_select_list.toggleClass("active");

				});

				$filter_log_level_options.on("click", function () {

        			var level = $(this).html();

        			$("span.text").html(level);
        			$filter_window_select_list.removeClass("active");

    			});

    			$filter_log_level_options.hover(function () {

        			$filter_log_level_options.removeClass("acti ve");

    			});

    			$(document).click(function (event) {

   					if (!($(event.target).is($filter_window) || 
   						$filter_window.find(event.target).length == 1)) {

            			$filter_window_select_list.removeClass("active");

        			}

    			});

			} else {



			}

		});

	});

}