function start_ci_deployment() {
    var inputfields = $('#createform').find('input');
    var emptyfields = false;
    for (var i = 0; i < inputfields.length; i++) {
        if (inputfields[i].value.length === 0) {
            $('label[for=' + inputfields[i].id + ']').addClass('error');
            emptyfields = true;
        }
        else {
            $('label[for=' + inputfields[i].id + ']').removeClass('error');
        }
    }
    if (emptyfields) {
        $('#empty_fields_error').removeClass('hidden');
        return;
    }
    $('#empty_fields_error').addClass('hidden');
    $('.progress-bar').css('width', '0%').attr('aria-valuenow', 0).removeClass('progress-bar-success').removeClass('progress-bar-danger').addClass('progress-bar-info progress-bar-striped active');
    $('.progress-value').text('').css('color', 'black');
    $.ajax({
        type: 'POST',
        url: '/deploy-ci',
        data: $('#createform').serialize(),
        success: function (data, status, request) {
            status_url = request.getResponseHeader('status_url');
            $('#start-deployment-button').attr("disabled", true);
            $('.progress').removeClass('hidden');
            $('.progress-bar')[0].scrollIntoView();
            update_progress(status_url);
        }
    });
}
$(function () {
    $('#start-deployment-button').click(start_ci_deployment);
});
$(function () {
    $('.selectbox').click(function () {
        $(this).focus();
        $(this).select();
    });
});

function update_progress(status_url) {
    $.getJSON(status_url, function (data) {
        var percent;
        if (data.current === 0 && data.total > 1) { // First step
            percent = parseInt(100 / (2 * data.total ));
        }
        else {
            percent = parseInt(data.current * 100 / data.total);
        }
        $('.progress-bar').css('width', percent + '%').attr('aria-valuenow', percent);
        $('.progress-value').text(data.message);
        if ($('.ci_pubkey').text.length < 10) {
            $('.ci_pubkey').text(data.ci_pubkey);
        }
        var state = data.state;
        if (state !== 'SUCCESS' && state !== 'FAILURE') {
            setTimeout(function () {
                update_progress(status_url);
            }, 2000);
        }
        else {
            $('#start-deployment-button').attr("disabled", false);
            $('.progress-bar').removeClass('').removeClass('progress-bar-info progress-bar-striped active');
            if (state === 'SUCCESS') {
                $('.progress-bar').addClass('progress-bar-success');
            }
            else if (state === 'FAILURE') {
                $('.progress-bar').addClass('progress-bar-danger');
                $('.progress-value').css('color', 'white');
            }

        }
    });
}
