function setGroupSelector() {

  $('#group-selector select').change(function(event){

      var group_id = $(this).val();
      group_id = group_id.replace(/\s/g, '')
      
      if (group_id) {

        Cookies.set('current_group', group_id, {'path': '/', 'expires': 365});

      } else {

        Cookies.remove('current_group', {'path': '/'});

      }

      location.reload(true);
    });

}

function changeBrowserURL(dom_element) {
  // Change URL with browser address bar using the HTML5 History API.
  // if (History) {
    // Parameters: data, page title, URL
  History.pushState(null, '', dom_element ? dom_element.href : null );
  // History.pushState(null, '', "?student=x" );
  // }
  // Fallback for non-supported browsers.
  // else {
  //   document.location.hash = dom_element.getAttribute("href");
  // }
}

function getPageHtml(url, callback) {
  
  var xhr = new XMLHttpRequest();
  xhr.open("GET", url, true);
  xhr.send();


  xhr.onreadystatechange = function() {

    if (xhr.readyState != 4) return;
      if (xhr.status != 200) {
        callback(xhr.status);
      } else {
        callback(null, xhr.responseText);
      }

    }

}

function popStateHandler() {

  // alert('h');

  // console.log(History);

  History.Adapter.bind(window,'statechange',function(e){

    var modal = $('#myModal');
    // alert('h');
    if(modal && modal.is(':visible')) {

      modal.modal('hide');
      // History.back();

    }
    // var State = History.getState();
    // location.href = State.url;
    // console.log(e);

  });
  // FF, Chrome, Safari, IE9.
  // if (history.pushState) {

    // window.onpopstate = function (){
    //     alert(location.href);
    // }

    // window.onpopstate = function(e) {
      // console.log(e.originalEvent);
      // alert('h');
      // console.log(e);
      // console.log(history);
      // alert('h');

      // location.href = location.href;

      // console.log(window.location);
      // console.log(document.referrer);
      // window.location = document.referrer;
      // if(e.state){

      //   location.href = e.state.prev_href;
      
      // } else {

      //   location.href = location.href;

      // }
      // getPageHtml(location.href, function(error, html) {

      //   if(error) {

      //     return;

      //   } else {

      //     var html_tag = document.getElementsByTagName("html")[0];
      //     html_tag.innerHTML = html;
      //     init();

      //   }

      // });

    // };
//   }
}

function loadJournalPage() {

  $('#journal').click(function(event){

    var $loader_wrapper = $('.loader-wrapper'),
        $link = $(this);

    $('.main-nav li').removeClass('active');
    $('#journal').addClass('active');

    event.preventDefault();

    $loader_wrapper.fadeIn('slow');

    setTimeout(function() {

      $.ajax({
        url      : $link.find('a').attr('href'),
        method   : "GET",
        dataType : "html"
      }).then(function(data, status, xhr) {

        changeBrowserURL($link.find('a')[0], current_href=location.href)

        // console.log(history.state);

        var $html = $(data),
            $body = $('body'),
            $scripts = $html.filter('#scripts').find('script').not('.common-script');



        $loader_wrapper.fadeOut('slow');

        // console.log($html);
        // console.log($html.filter('#scripts').find('script'));

        if (status != 'success') {
          
          $loader_wrapper.fadeOut(100, function() {

            alert('Error on server');
            return;
          }); 

        }

        $('#content-columns').html($html.find('#content-columns').html());
        $body.append($html.find('.pagination-nav'));

        $('link').not(".common").remove();
        $('head').append($html.filter('link').not(".common"));

        $body.find('#scripts script').not('.common-script').remove();
        $body.append($scripts);//jQuery will load the scripts but synchronously

        // initEditStudentPage();

      }, function(xhr, status, error) {

        $loader_wrapper.fadeOut(100, function() {

          alert('Error on server');

        }); 

      });

}, 3000);

  })


}

function init() {

  setGroupSelector();
  loadJournalPage();

}

$(function(){

  var History = window.History;
  popStateHandler();
  // History.replaceState(null, '', location.href );
  // initDatePicker();
  init();


  // console.log(History);
});