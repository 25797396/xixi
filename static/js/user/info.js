$(function(){
    var token = window.localStorage.getItem('travel_token');
    var url = document.location.toString();
    var arrUrl = url.split("//");
    //当前访问的博客博主
    console.log(arrUrl)
    var username = arrUrl[1].split('/')[3];
    console.log('要访问的用户:'+username)
    var url = 'http://127.0.0.1:8000/user/info/'+username
    $.ajax({
        url: url,
        type: 'POST',
        beforeSend: function(request) {
            request.setRequestHeader("Authorization", token);
        },
        success: function(res){
            if(res.code==200){
                $('title').text(res.data.nickname+'的个人主页')
                $('#avatar').attr('src', '/static/media/'+res.data.avatar);
                $('#nickname').html(res.data.nickname);
                $('#username').html(res.data.username);
                $('#email').html(res.data.email);
                $('#info').html(res.data.info);
                if(res.data.username == res.data.vistor){
                    $('#change_info').css("display","inline");
                    // $('#change_info').attr("href",'/user/change_info/'+res.data.username);
                }
            }else{
                alert(res.error)
                window.location.href = '/index'
            }
        }
    })
})

function change(){
    div = $('#change_form');
    html_body = ' <div style="text-align:center"><h1>个人信息修改</h1></div>'
    html_body +='<p style="font-size: 20px;">头像：</p>'
    html_body += '<form action=""  method="post" enctype="multipart/form-data" class="avatar_form">';
    html_body += '<p class="avatar"> <div class="imgDiv"><img src=' +$('#avatar').attr('src')+ ' alt="" width="100%" height="100%"> </div></p>';
    html_body += '<p>';
    html_body += '&nbsp;<input type="file" name="avatar" id="avatar">';
    html_body += '</br>'
    html_body += '<input id="submit-btn" type="button" value="修改头像" onclick="upload()">';
    html_body += '</p>';
    html_body += '</form><hr>';
    html_body += '<span style="font-size: 20px;">昵称:</span> <input id="new_nickname" value="'+$('#nickname').text()+'"><br><hr>'
    html_body +=' <span style="font-size: 20px;">info:</span><textarea id="new_info">'+$('#info').text()+'</textarea><br>'
    html_body +='<input type="button" value="保存" id="save_btn" onclick="save_info()">'
    div.html(html_body)
}

function upload(){
    var token = window.localStorage.getItem('travel_token');
    var username = window.localStorage.getItem('travel_user');
    var url = 'http://127.0.0.1:8000/user/upload_avatar/' + username
    formdata = new FormData();
    formdata.append("avatar",$("#avatar")[0].files[0]);
    console.log($("#avatar")[0].files[0])
    if($("#avatar")[0].files[0]== null){
        alert('未选择图片')
        return
    }
    $.ajax({
            processData: false,
            contentType: false,
            url: url,
            type: 'post',
            data: formdata,
            beforeSend: function(request) {
                request.setRequestHeader("Authorization", token);
            },
            success: function(arg) {
                if (arg.code == 200) {
                    alert('成功！')
                    window.location.reload()
                } else {
                    alert(arg.error)
                    window.location.href = '/user/login'
                }
            }
    })
}

function save_info(){
    var token = window.localStorage.getItem('travel_token');
    var username = window.localStorage.getItem('travel_user');
    new_nickname = $('#new_nickname').val();
    new_info = $('#new_info').val();
    $.ajax({
        url: 'http://127.0.0.1:8000/user/info/'+username,
        data: JSON.stringify({"nickname": new_nickname,"info":new_info}),
        type:'put',
        beforeSend: function(request) {
                request.setRequestHeader("Authorization", token);
        },
        success: function(res){
            if(res.code==200){
                alert('修改成功')
                window.location.href= '/user/info/'+username
            }else{
                alert(res.error)
            }
        }
    })

}

function ccc(obj){
    $(obj).addClass('act')
}

function ccc2(obj){
    if($(obj).children(":first").text()=='我'){
        return
    }
    $(obj).removeClass('act')
}


