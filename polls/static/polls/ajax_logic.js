$('#active-tags-container').on('click', 'a[id^=remove-tag-]', function(){

    var tag_primary_key = $(this).attr('id').split('-')[2];
    var tag_name = $(this).children('button').text();

    remove_tag(tag_primary_key, tag_name);

    $("#active-tags-container:only-child").fadeOut();
    console.log($("#active-tags-container:only-child"));
    $(this).fadeOut(300, function () {$(this).remove();});
});

function remove_tag(tag_primary_key, tag_name){
    $.ajax({
        url : "/polls/remove_tag/",
        type : "POST",
        data: {
            tagpk : tag_primary_key
        },
        success : function (tag_id) {
            $('#add-tag-' + tag_id).fadeIn();
        },
        error : function(xhr, errmsg, err) {
            // Show an error
            $('#results').html("<div class='alert-box alert radius' data-alert>"+ "Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}


$('#tags-container').on('click', 'a[id^=add-tag-]', function(e){
    e.preventDefault();
    var tag_primary_key = $(this).attr('id').split('-')[2];
    var tag_name = $(this).text();

    console.log(tag_name);

    add_tag(tag_primary_key, tag_name);

    $('#remove-all-tags').fadeIn();
    $(this).fadeOut();
});

function add_tag(tag_primary_key, tag_name){
    $.ajax({
        url : "/polls/add_tag/",
        type : "POST",
        data: {
            tagpk : tag_primary_key
        },
        success : function (tag_id) {
            var html = "<a id='remove-tag-" + tag_primary_key + "'><button class='btn btn-default btn-success btn-sm'>" +
                    tag_name + "<i class='glyphicon glyphicon-remove'></i></button></a>";

            $(html).hide().prependTo("#active-tags-container").fadeIn();
        },
        error : function(xhr, errmsg, err) {
            // Show an error
            $('#results').html("<div class='alert-box alert radius' data-alert>"+ "Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}




$("div[id^=question-]").on('click', 'a[id^=edit-question-]', function(){
    form = $(this).siblings('.question-edit-form');
    var textarea = form.find('#question-text');
    var input = form.find('#id_header');
    var current_question_details = form.prev();
    var current_question_header = current_question_details.prev();

    //if(textarea.val() == "")
    input.val(current_question_header.text().trim());
    textarea.val(current_question_details.text().trim());

    current_question_details.slideToggle();
    current_question_header.slideToggle();
    form.slideToggle();

    var question_primary_key = $(this).attr('id').split('-')[2];

    form.on('submit', function(event){
        event.preventDefault();
        console.log(input.val());
            update_question(question_primary_key, textarea.val(), input.val(),
                               current_question_details, current_question_header);
        current_question_details.slideDown();
        current_question_header.slideDown();
        form.slideUp();
    });
});

function update_question(question_primary_key, new_content, new_header, current_text,  current_header){
    console.log(new_header);
    $.ajax({
        url : "edit_question/",
        type : "POST",
        data: {
            questionpk : question_primary_key,
            new_content : new_content,
            new_header : new_header
        },
        success : function (json) {
            current_text.text(json.content);
            current_header.text(json.header);
        },
        error : function(xhr, errmsg, err) {
            // Show an error
            $('#results').html("<div class='alert-box alert radius' data-alert>"+ "Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

$('div[id^=question-]').on('click', 'a[id^=approve-question-]', function(){
    var question_primary_key = $(this).attr('id').split('-')[2];
    console.log(question_primary_key); // sanity check
    $(this).children('button').toggleClass('btn-success');
    $(this).next().next().children('button').removeClass('btn-danger');
    approve_question(question_primary_key, this);
});


function approve_question(question_primary_key,  btn_clicked) {
    $.ajax({
        url: '/polls/approve_question/',
        type: 'post',
        data: {questionpk: question_primary_key},
        success: function(new_rating) {
            $(btn_clicked).next().text(new_rating);
        },
        error : function(xhr, errmsg, err) {
            // Show an error
            $('#results').html("<div class='alert-box alert radius' data-alert>"+ "Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    })
}

$('div[id^=question-]').on('click', 'a[id^=disapprove-question-]', function(){
    var question_primary_key = $(this).attr('id').split('-')[2];
    console.log(question_primary_key); // sanity check
    $(this).children('button').toggleClass('btn-danger');
    $(this).prev().prev().children('button').removeClass('btn-success');
    disapprove_question(question_primary_key, this);
});


function disapprove_question(question_primary_key, btn_clicked){
    $.ajax({
        url: '/polls/disapprove_question/',
        type: 'post',
        data: {questionpk: question_primary_key},
        success : function(new_rating){
            $(btn_clicked).prev().text(new_rating);
        },
        error : function(xhr, errmsg, err) {
            // Show an error
            $('#results').html("<div class='alert-box alert radius' data-alert>"+ "Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

$("#answers").on('click', 'a[id^=is-right-]', function(){
    var answer_primary_key = $(this).attr('id').split('-')[2];
    console.log(answer_primary_key); // sanity check
    $(this).children('button').toggleClass('btn-success');
    check_answer(answer_primary_key);
});

function check_answer(answer_primary_key){
    $.ajax({
        url: 'check_answer/',
        type: 'post',
        data: {answerpk: answer_primary_key},
        success: function(){

        },
        error : function(xhr, errmsg, err) {
            // Show an error
            $('#results').html("<div class='alert-box alert radius' data-alert>"+ "Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    })
}

$("#answers").on('click', 'a[id^=disapprove-answer-]', function(){
    var answer_primary_key = $(this).attr('id').split('-')[2];
    console.log(answer_primary_key); // sanity check
    $(this).children('button').toggleClass('btn-danger');
    $(this).prev().prev().children('button').removeClass('btn-success');
    disapprove_answer(answer_primary_key, this);
});

function disapprove_answer(answer_primary_key, btn_clicked){
    $.ajax({
        url: 'disapprove_answer/',
        type: 'post',
        data: {answerpk: answer_primary_key},
        success : function(new_rating){
            $(btn_clicked).prev().text(new_rating);
        },
        error : function(xhr, errmsg, err) {
            // Show an error
            $('#results').html("<div class='alert-box alert radius' data-alert>"+ "Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

$("#answers").on('click', 'a[id^=approve-answer-]', function(){
    var answer_primary_key = $(this).attr('id').split('-')[2];
    console.log(answer_primary_key); // sanity check
    $(this).children('button').toggleClass('btn-success');
    $(this).next().next().children('button').removeClass('btn-danger');
    approve_answer(answer_primary_key, this);
});

function approve_answer(answer_primary_key, btn_clicked){
    $.ajax({
        url: 'approve_answer/',
        type: 'post',
        data: {answerpk: answer_primary_key},
        success : function(new_rating){
            console.log(btn_clicked);
            $(btn_clicked).next().text(new_rating);
        },
        error : function(xhr, errmsg, err) {
            // Show an error
            $('#results').html("<div class='alert-box alert radius' data-alert>"+ "Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

$("#answers").on('click', 'a[id^=delete-answer-]', function(){
    var answer_primary_key = $(this).attr('id').split('-')[2];
    console.log(answer_primary_key); // sanity check
    delete_post(answer_primary_key);
});

$("#answers").on('click', 'a[id^=edit-answer-]', function(){
    form = $(this).siblings('.answer-edit-form');
    var textarea = form.find('textarea');
    var current_answer = form.prev();

    //if(textarea.val() == "")
    textarea.val(current_answer.text().trim());

    current_answer.slideToggle();
    form.slideToggle();

    var answer_primary_key = $(this).attr('id').split('-')[2];

    form.on('submit', function(event){
        event.preventDefault();
        if(current_answer.text().trim() != textarea.val())
            update_answer(answer_primary_key, textarea.val(), current_answer);
        current_answer.slideDown();
        form.slideUp();
    });
});

function update_answer(answer_primary_key, new_text, current_text){
    $.ajax({
        url : "edit_answer/",
        type : "POST",
        data: {
            answerpk : answer_primary_key,
            new_text : new_text
        },
        success : function (text) {
            current_text.text(text);
        },
        error : function(xhr, errmsg, err) {
            // Show an error
            $('#results').html("<div class='alert-box alert radius' data-alert>"+ "Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

function delete_post(answer_primary_key){
    if (confirm('are you sure you want to remove this post?')==true){
        $.ajax({
            url : "delete_answer/", // the endpoint
            type : "DELETE", // http method
            data : { answerpk : answer_primary_key }, // data sent with the delete request
            success : function(json) {
                // hide the post
              $('#answer-' + answer_primary_key).slideUp(); // hide the post on success
              console.log("post deletion successful");
            },

            error : function(xhr, errmsg, err) {
                // Show an error
                $('#results').html("<div class='alert-box alert radius' data-alert>"+
                "Oops! We have encountered an error. <a href='#' class='close'>&times;</a></div>"); // add error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    } else {
        return false;
    }
}

$('#answer-add-form').on('submit', function(event){
    event.preventDefault();
    add_answer();
});

function add_answer() {
    $.ajax({
        url : "add_answer/", // the endpoint
        type : "POST", // http method
        data : { the_answer : $('#answer-add-form #answer-text').val() }, // data sent with the post request

        // handle a successful response
        success : function(html) {
            $('#answer-add-form #answer-text').val(''); // remove the value from the input
            console.log(html); // log the returned json to the console
            $(html).hide().prependTo("#answers").slideDown();
            console.log("success"); // another sanity check
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

$(function() {


    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});
