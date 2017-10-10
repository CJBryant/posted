$(window).on('load', function() {
  $('#loading').fadeOut();
});

var csrftoken = Cookies.get('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$('.follow-btn').hover(function(){
  if ($(this).hasClass('unfollow-btn')) {
    $(this).text('Unfollow');
  } else {
    $(this).text('Follow');
  }
}, function(){
  if ($(this).hasClass('unfollow-btn')) {
    $(this).text('Following');
  } else {
    $(this).text('Follow');
  }
});

$(document).on('click', '.follow-btn', function(){
  if ($(this).hasClass('unfollow-btn')) {
    $(this).toggleClass('unfollow-btn');
    $(this).text('Follow');
    if ($(this).hasClass('followlist')){
      $(this).closest('.panel').slideToggle(400, 'swing');
    }
    $.ajax({
      type:"POST",
      data: { feed: $(this).attr('id'),
              action: 'unfollow',
            },
      error: function(){
        alert("Something went wrong.");
      },
    });
  } else {
    $(this).toggleClass('unfollow-btn');
    $(this).text('Following');
    $.ajax({
      type:"POST",
      data: { feed: $(this).attr('id'),
              action: 'follow',
            },
      error: function(){
        alert("Something went wrong.");
      },
    });
  }
});

$(document).on('click', '.add-btn', function(){
  if ($(this).hasClass('remove-btn')) {
    $(this).toggleClass('remove-btn');
    $('span', this).removeClass('glyphicon-minus');
    $('span', this).addClass('glyphicon-plus');
    if ($(this).hasClass('mylist')) {
      $(this).closest('.panel').slideToggle(400, 'swing');
    }
    $.ajax({
     type:"POST",
     data: { article: $(this).attr('id'),
             action: 'remove',
           },
     error: function(){
       alert("Something went wrong.");
     },
    });
  } else {
    $(this).toggleClass('remove-btn');
    $('span', this).removeClass('glyphicon-plus');
    $('span', this).addClass('glyphicon-minus');
    $.ajax({
     type:"POST",
     data: { article: $(this).attr('id'),
             action: 'add',
           },
     error: function(){
       alert("Something went wrong.");
     },
    });
  }
});
