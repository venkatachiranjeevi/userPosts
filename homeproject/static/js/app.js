/**
 * Created by customfurnish on 21/11/16.
 */
$(document).ready(function () {
   $('#nav-point')[0].scrollIntoView();

});
function validatePostData() {
        var postTitle = $("#post-title").val();
        var postDes = $("#post-des").val();
        if(postDes!= ' ' && postDes != undefined && postTitle!= ' ' && postTitle != undefined) {
            submitPostDetails(postTitle, postDes)
        }
    }
    function submitPostDetails(postTitle, postDes) {
        var formData = new FormData();
        formData.append("postTitle", postTitle);
        formData.append("postDes", postDes);
        $.ajax({
             url: "/add-post/",
             method: "POST",
             processData: false,
             data: formData,
             contentType: false,
             headers: {
                'X-CSRFToken': $("#csrf").val()
            },
             success: function(data){
                 console.log(data);
                 var b = data['createdAt'].split(/\D/);
                $("#post-details")[0].reset();
                 $("#posts").append('<div class="post" id="list"> ' +
                 '<li id="posts-list" class = "posts-list last-item"> ' +
                 '<p class="post-title">'+data['postTitle']+'</p>' +
                 '<p class="post-meta">'+new Date(b[0], b[1]-1, b[2], b[3], b[4], b[5])+'</p> ' +
                 '<p class="post-content">' + data['postDes']+ '</p>' +
                 '</li> </div>');
                 $('#nav-point')[0].scrollIntoView();
             },
             error : function(){
                alert("Unable to add your post");
            }
        });

    }

function googleSignIn(token) {
        var data = {};
        data['token'] = token;
         $.ajax({
             url: '/google-login/',
             method: "POST",
             data: JSON.stringify(data),
             dataType: "json",
             contentType: "application/json",
             success: function(data){
                console.log(data);
                window.location.href = '/get-posts/?id=' +data['userId']
             },
             error : function(){
                alert("unable to login");
            }
        });


}
