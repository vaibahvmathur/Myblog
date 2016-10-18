$(document).ready(function(){
    $(".delete_btn").on("click",function(){
        var id = $(this).attr('id');
        $('#confirm_delete').modal('show');
        $('#delete_blog').on('click', function(){
            $.ajax({
                type : 'POST',
                url : "deleteblog",
                data : { 'id' : id },
                dataType : 'json'
            }).done(function(json){
                var result = json.message;
                if(result == "success"){
                    $('#confirm_delete').modal('hide');
                    location.href = '/home'
                }
                else if( result == "error" ){
                    $('#confirm_delete').modal('hide');
                    alert('error while deleting');
                }
                else{
                    $('#confirm_delete').modal('hide');
                    alert('error while deleting')
                }
            }).fail(function(){
                $('#confirm_delete').modal('hide');
                alert("failed while deleting")
            });
        });
    });
});