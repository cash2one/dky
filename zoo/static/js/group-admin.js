$(document).ready(function(){
    $(".ga-m2a-btn").click(function(){
        var $this = $(this);
        $.post("/group/admin/m2a/"+ $this.data("groupid") +"/"+ $this.data("userid"), function(data){
            console.log(data);
            if(data.msg == "success"){
                window.location.reload();
            }
        });
    });

    $(".ga-a2m-btn").click(function(){
        var $this = $(this);
        $.post("/group/admin/a2m/"+ $this.data("groupid") + "/" + $this.data("userid"), function(data){
            console.log(data);
            if(data.msg == "success"){
                window.location.reload();
            }
        });
    });

    $(".ga-d-m-btn").click(function(){
        var $this = $(this);
        $.post("/group/admin/dm/" + $this.data("groupid") + "/" + $this.data("userid"), function(data){
            if(data.msg == "success"){
                window.location.reload();
            }
        });
    });
});