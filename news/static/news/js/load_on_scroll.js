$(document).ready(function(){
   $(window).on('scroll', loadOnScroll);
});

// Scroll globals
var pageNum = 1; // The latest page loaded
var hasNextPage = true; // Indicates whether to expect another page after this one

// loadOnScroll handler
var loadOnScroll = function() {
   // If the current scroll position is past out cutoff point...
    if ($(window).scrollTop() > $(document).height() - ($(window).height()*2)) {
        // temporarily unhook the scroll event watcher so we don't call a bunch of times in a row
        $(window).off('scroll');
        // execute the load function below that will visit the JSON feed and stuff data into the HTML
        console.log("Success!")
        //loadItems();
    }
};

var loadItems = function() {
    // If the next page doesn't exist, just quit now
    if (hasNextPage === false) {
        return false
    }
    // Update the page number
    pageNum = pageNum + 1;
    // Configure the url we're about to hit
    $.ajax({
        url: 'news/newyorker/66/',
        data: {page_number: pageNum},
        dataType: 'json',
        success: function(data) {
            // Update global next page variable
            hasNextPage = true;//.hasNext;
            // Loop through all items
            for (i in data) {
                $("#more-articles").before(
                // Do something with your json object response
                "<h1>Nice</h1>"
              )
            }
        },
        error: function(data) {
            // When I get a 400 back, fail safely
            hasNextPage = false
        },
        complete: function(data, textStatus){
            // Turn the scroll monitor back on
            $(window).bind('scroll', loadOnScroll);
        }
    });
};
