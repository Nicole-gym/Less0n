var cur = 0;
var all_profs = null;
var color_pool = ['success', 'primary', 'info', 'danger', 'warning'];

function changeProf(index, all_profs) {
    var current_prof = all_profs[index];
    $('#prof-pic').attr('src', current_prof['avatar']);
    $('#faculty_choice h4').text(current_prof['name']);

    $('#tag_list .tags').empty();
    for (var i = 0; i < current_prof['tags'].length; i++) {
        var color = i%5;
        $('#tag_list .tags').append('<a class="' + color_pool[color] + '">' + current_prof['tags'][i] + '</a>');
    }

    $('#rating_progress_bar').css('width', current_prof['rating'] / 5 * 100 + '%');
    $('#rating_progress_bar').removeClass();
    $('#rating_progress_bar').addClass('progress_bar');
    $('#rating_progress_bar').addClass(rating_to_color(current_prof['rating']));
    $('#rating_numerical').text(current_prof['rating']);
    $('#grade_progress_bar').css('width', current_prof['grade'] / 4.33 * 100 + '%');
    $('#grade_progress_bar').removeClass();
    $('#grade_progress_bar').addClass('progress_bar');
    $('#grade_progress_bar').addClass(gpa_to_color(current_prof['grade']))
    $('#grade_numerical').text(current_prof['grade']);
    $('#workload_progress_bar').css('width', current_prof['workload'] / 5 * 100 + '%');
    $('#workload_progress_bar').removeClass();
    $('#workload_progress_bar').addClass('progress_bar');
    $('#workload_progress_bar').addClass(workload_to_color(current_prof['workload']));
    $('#workload_numerical').text(current_prof['workload']);

    // Load comments
    $('.container.card-columns').empty();
    for (var i = 0; i < current_prof['comments'].length; i++) {
        var current_comment = current_prof['comments'][i];

        var rating_html = '';
        var workload_html = '';
        for (var j = 0; j < current_comment['rating']; j++)
            rating_html += '<i class="fa fa-star"></i>';
        for (var j = 0; j < current_comment['workload']; j++)
            workload_html += '<i class="fa fa-pencil"></i>';

        $('.container.card-columns').append(
            '<div class="card">' +
                '<div class="card-body ' + rating_to_color(current_comment['rating']) + '">' +
                    '<h5 class="card-title">' + current_comment['title'] + '</h5>' +
                    '<p class="card-text">' + current_comment['content'] + '</p>' +
                    '<a class="btn btn-light" data-toggle="collapse" href="#c' + i + '" role="button" aria-expanded="false" aria-controls="c' + i + '">Show Details <i class="fa fa-caret-down"></i></a>' +
                    '<div class="collapse" id="c' + i + '">' +
                        '<ul class="list-group">' +
                            '<li class="list-group-item">Term: ' + current_comment['term'] + '</li>' +
                            '<li class="list-group-item">Instructor: ' + current_prof['name'] + '</li>' +
                            '<li class="list-group-item">Rating: ' + rating_html + '</li>' +
                            '<li class="list-group-item">Workload: ' + workload_html + '</li>' +
                            '<li class="list-group-item">Grade: '  + current_comment['grade'] +  '</li>' +
                            '<li class="list-group-item">'  + current_comment['timestamp'] +  '</li>' +
                        '</ul>' +
                    '</div>' +
                '</div>' +
            '</div>');
    }
}

$('#left i').click(function() {
    cur--;
    if (cur < 0)
        cur = all_profs.length - 1;
    changeProf(cur, all_profs);
});

$('#right i').click(function() {
    cur++;
    if (cur >= all_profs.length)
        cur = 0;
    changeProf(cur, all_profs);
});



// Star effect
// hover
$('#stars li').on('mouseover', function() {
    var onStar = parseInt($(this).data('value'));
    $(this).parent().children('li.star').each(function(e) {
        if (e < onStar) {
            $(this).addClass('hover');
        }
        else {
            $(this).removeClass('hover');
        }
    });
}).on('mouseout', function() {
    $(this).parent().children('li.star').each(function(e) {
        $(this).removeClass('hover');
    });
});

// click
$('#stars li').on('click', function() {
    var onStar = parseInt($(this).data('value'), 10);
    var stars = $(this).parent().children('li.star');

    for (i = 0; i < stars.length; i++) {
        $(stars[i]).removeClass('selected');
    }

    for (i = 0; i < onStar; i++) {
        $(stars[i]).addClass('selected');
    }

    // response
    var ratingValue = parseInt($('#stars li.selected').last().data('value'));
    $('#rating').val(ratingValue);
});

// Pen effect
// hover
$('#pens li').on('mouseover', function() {
    var onPen = parseInt($(this).data('value'));
    $(this).parent().children('li.pen').each(function(e) {
        if (e < onPen) {
            $(this).addClass('hover');
        }
        else {
            $(this).removeClass('hover');
        }
    });
}).on('mouseout', function() {
    $(this).parent().children('li.pen').each(function(e) {
        $(this).removeClass('hover');
    });
});

// click
$('#pens li').on('click', function() {
    var onPen = parseInt($(this).data('value'), 10);
    var pens = $(this).parent().children('li.pen');

    for (i = 0; i < pens.length; i++) {
        $(pens[i]).removeClass('selected');
    }

    for (i = 0; i < onPen; i++) {
        $(pens[i]).addClass('selected');
    }

    // response
    var workloadValue = parseInt($('#pens li.selected').last().data('value'));
    $('#workload').val(workloadValue);
});

// Alert notify
$('#add-comment').on('click', function () {
    $.notify({
        message: 'Please <a id="notif" href="">sign in</a> with your Lionmail before leaving a comment.'
    },{
        element: 'body',
        position: 'fixed',
        type: "danger",
        allow_dismiss: true,
        placement: {
            from: "top",
            align: "center"
        },
        offset: 60,
        spacing: 10,
        z_index: 1031,
        delay: 3000,
        timer: 1000,
        url_target: '_blank',
        animate: {
            enter: 'animated fadeInDown',
            exit: 'animated fadeOutUp'
        },
        onShow: null,
        onShown: null,
        onClose: null,
        onClosed: null,
        icon_type: 'class',
        template: '<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert">' +
            '<span data-notify="icon"></span> ' +
            '<span data-notify="title">{1}</span> ' +
            '<span data-notify="message">{2}</span>' +
            '<div class="progress" data-notify="progressbar">' +
                '<div class="progress-bar progress-bar-{0}" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>' +
            '</div>' +
            '<a href="{3}" target="{4}" data-notify="url"></a>' +
        '</div>'
    });
});