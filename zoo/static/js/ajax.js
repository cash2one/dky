function alertError(message){
    html =  '<div class="alert alert-danger alert-dismissible" role="alert">'+
                 '<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>'+
                        '<strong>'+
                        message +
                        '</strong>'+
                    '</div>'
    $("#flash-div").append(html);
}

$(document).ready(function(){
    $(":input[class='ai']").each(function(){
        switch($(this).attr('type')){
            case 'checkbox':
                $(this).on('switchChange.bootstrapSwitch', function(event, state) {
                    var $checkbox = $(this)
                    data = {};
                    data[$checkbox.attr('name')] = state;
                    $.post($checkbox.data('url'), data, function(response) {
                        $($checkbox.data('amsid')).html(response.msg).fadeIn(1500,function(){
                            $(this).fadeOut(1500);
                        });

                    }, 'json');
                });
        };
    });
    /**
        ajax btn change self
    **/
    $(".abcs").each(function(){
        $(this).click(function(){
            var $btn = $(this);
            $.post($btn.data('url'), data=$btn.data(),function(response){
                if(response["status"] == 200){
                    $btn.data("url",response["newurl"]);
                    $btn.html(response["message"]);
                }else if(response["status"] == 500){
                    alertError(response["message"]);
                }
            });
        });
    });


});