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

	let $filter_icon = $('.filter-icon');

	$filter_icon.click(function() {

		$(this).next('.filter-window').slideToggle('300');

	});

}