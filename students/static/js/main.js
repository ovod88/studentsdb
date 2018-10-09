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

function addHistoryEntry(dom_element, state_data=null) {
  // Change URL with browser address bar using the HTML5 History API.
  // if (History) {
    // Parameters: data, page title, URL
  // alert(dom_element.href);
  History.pushState({ data : state_data }, '', dom_element ? dom_element.href : null );
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

  //THIS HANDLER IS ONLY PARTIALLY WORKS BECAUSE NOT ALL PAGES ARE LOADED VIA AJAX,
  //SO 'statechange' IS NOT LAUNCHED ALWAYS. THUS NO 'no refresh' FUNCTIONALITY.
  //CHECK JOURNAL PAGE, GROUPS PAGE AND PUSH BACK BUTTON - BROWSER SENDS USUAL REQUEST
  //BECAUSE NO 'statechange' SINCE GROUPS ARE GET IN USUSAL WAY, SO history OBJECT NOT TOUCHED.
  //THUS NO 'statechange' event WHEN REMOVED THIS ENTRY (PRESSED BACK BUTTON)

  History.Adapter.bind(window,'statechange',function(e){

    var modal = $('#myModal'),
        State = History.getState();

    // console.log(State);
    // alert('State Changed');
    if(modal && modal.is(':visible')) {//IF IT IS STUDENTS PAGE AND ONLY MODEL IS ADDED

      modal.modal('hide');
      // History.back();
      return;
      // History.back();

    }

    if(State && State.hash.includes('journal')) {//IS ACTIVATED WHEN JOURNAL AJAX PAGE IS PRESSED

      // alert('Journal State here');
      // console.log(State.data.data);
      loadJournalContent(State.data.data);
      return;

    }

    if(State && State.hash.includes('groups')) {//JUST TO TEST ADDING STATE FOR GROUPS PAGE

      // alert('Groups State here');
      return;

    }
    if(State && State.hash === '/') {

      location.href = State.url;

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

function loadJournalContent(html) {

  // console.log('Journal Loader called');

  var $html = $(html),
      $body = $('body'),
      $scripts = $html.filter('#scripts').find('script').not('.common-script');

  $('#content-columns').html($html.find('#content-columns').html());
  $body.append($html.find('.pagination-nav'));

  $('link').not(".common").remove();
  $('head').append($html.filter('link').not(".common"));

  $body.find('#scripts script').not('.common-script').remove();
  $body.append($scripts);//jQuery will load the scripts but synchronously

}

function loadJournalPage() {

  $('#journal a').click(function(event){

    event.preventDefault();

    var $loader_wrapper = $('.loader-wrapper'),
        $link = $('#journal'),
        self = this;

    $('.main-nav li').removeClass('active');
    $link.addClass('active');

    $loader_wrapper.fadeIn('slow');

    setTimeout(function() {

      $.ajax({
        url      : $link.find('a').attr('href'),
        method   : "GET",
        dataType : "html"
      }).then(function(data, status, xhr) {

        // console.log(history.state);

        // console.log($html);
        // console.log($html.filter('#scripts').find('script'));

        if (status != 'success') {
          
          $loader_wrapper.fadeOut(100, function() {

            alert(gettext('Error on server'));
            return;
          }); 

        }

        $loader_wrapper.fadeOut(100, function() {

          addHistoryEntry(self, data);

        });

        // $('#content-columns').html($html.find('#content-columns').html());
        // $body.append($html.find('.pagination-nav'));

        // $('link').not(".common").remove();
        // $('head').append($html.filter('link').not(".common"));

        // $body.find('#scripts script').not('.common-script').remove();
        // $body.append($scripts);//jQuery will load the scripts but synchronously

        // initEditStudentPage();

      }, function(xhr, status, error) {

        $loader_wrapper.fadeOut(100, function() {

          alert(gettext('Error on server'));

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

   // $('#groups a').click(function(event){//JUST TO TEST GROUPS PAGE
   //    event.preventDefault();

   //    // console.log($(this).find('a')[0]);
   //    alert('Clicked');
   //    addHistoryEntry(this, 'test');

   // });
  // console.log(History);
});