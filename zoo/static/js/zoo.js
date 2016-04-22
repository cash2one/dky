 $(document).ready(function(){

    $(".acl").each(function(){
        $(this).load($(this).data("url"));
    });

    $(".submitBtn").click(function(){
        var form = $(this).data("form");
        $(form).submit();
    });

    $(".accordion-trigger").click(function(){
       $(this).parents('.accordion-wrap').toggle();
       $(this).parents('.accordion-wrap').next().toggle();
    });
    $(".accordion-dismiss").click(function(){
        $(this).parents(".accordion-content").toggle();
        $(this).parents(".accordion-content").prev().toggle();
    });
    $(".fake-file").click(function(){
        $($(this).data("file")).click();
    });
    $(".auto-file").on('change', function(){
        $(this).parent("form").submit();
    })
    $(".ams").hide();

    $(".toggle").click(function(){
        $($(this).data("toggle")).toggle();
    })

    $(".modal-btn").click(function(){
        $($(this).data("modal")).modal('show');
    })
    $(".remote-modal-btn").click(function(){
        $this = $(this);
        $("#remote-modal-container").load( $this.data("url"), function(){
             $(".submitBtn").click(function(){
                $($(this).data("form")).submit();
             });
            $('.datetimepicker').datetimepicker();
            $("#remote-modal-container .modal").modal('show');
        })
    })
    $('.datetimepicker').datetimepicker();

 });
