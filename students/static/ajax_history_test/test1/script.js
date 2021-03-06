var readyStateCheckInterval = self.setInterval(function() {
    // Check if DOM ready.
    if (document.readyState === "complete") {
        // When DOM ready, destroy timer and execute setupLinks() function.
        clearInterval(readyStateCheckInterval);
        // alert('Hello');
        setupLinks();

        popStateHandler();
    }
}, 10);

function setupLinks() {
  // Send our predefined link elements to ajaxify_link() function.
  ajaxify_link(document.getElementById("home-link"));
  ajaxify_link(document.getElementById("contact-link"));
  ajaxify_link(document.getElementById("about-link"));
}

function ajaxify_link(link_element) {
 
  // Destroy any currently bound click events to this element.
  link_element.onclick = null;
 
  // IE8
  if (!link_element.addEventListener) {
    link_element.attachEvent("onclick", function(e) {
      // Prevent default browser action on click.
      // This will stop the browser redirecting to  the HREF value.
      e.returnValue = false;
 		
 	  changeBrowserURL(link_element);
      // Get page and replace current content.
      getPage(link_element.href);
      // alert('Clicked');
    }, false);
  }
  
  // FF, Chrome, Safari, IE9.
  else {
    link_element.addEventListener("click", function(e) {
      // Prevent default browser action on click.
      // This will stop the browser redirecting to  the HREF value.
      e.preventDefault();
 	  

 	  changeBrowserURL(link_element);
      // Get page and replace current content.
      getPage(link_element.href);
      // alert('Clicked');
    }, false);
  }
}

function getPage(link_url) {
    // Get content using XMLHttpRequest object.
    XMLHttp = new XMLHttpRequest();
    
    // Set the request type, URL and disable asynchronous mode,
    // as we don't care about the script hanging waiting for the reply.
    XMLHttp.open("GET", link_url, false);
    
    // Send the request to the server.
    XMLHttp.send();
    
    // The response we receive is not in XML format. So we cannot 
    // use the DOM to extract what we need directly.
    // Thus we assign it to a new element first.
    var dom_response_holder = document.createElement('div');
    
    // Remember to use 'responseText' instead of 'response', as this won't work in IE.
    dom_response_holder.innerHTML = XMLHttp.responseText;
 
    // Now extract what we need using the DOM.
    var new_container_element = dom_response_holder.getElementsByTagName("DIV");
    
    // getElementsByTagName() returns an array. We are only interested in the first element.
    new_container_element = new_container_element[0].innerHTML;
        
    // Replace current content.
   document.getElementById("container").innerHTML = new_container_element;
 
    // Rebuild links, to ensure all links are bound correctly.
    setupLinks();
}


function changeBrowserURL(dom_element) {
  // Change URL with browser address bar using the HTML5 History API.
  if (history.pushState) {
    // Parameters: data, page title, URL
    history.pushState(null, null, dom_element.href);
  }
  // Fallback for non-supported browsers.
  else {
    document.location.hash = dom_element.getAttribute("href");
  }
}


function popStateHandler() {
  // FF, Chrome, Safari, IE9.
  if (history.pushState) {
    // Event listener to capture when user pressing the back and forward buttons within the browser.
    window.addEventListener("popstate", function(e) {
      // Get the URL from the address bar and fetch the page.
      getPage(document.URL);
      // alert('Clicked button');
    });
  }
  
  // IE8.
  else {
    // Event listener to cature address bar updates with hashes.
    window.attachEvent("onhashchange", function(e) {
      // Extract the hash
      location_url = window.location.hash;
 
      // Remove the # symbol.
      location_url = location_url.substring(1);
      
      // Fetch page using the constructed URL.
      getPage(location_url);
      // alert('Clicked button');
    });
  }
}