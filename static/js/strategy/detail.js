var url = document.location.toString();
var arrUrl = url.split("//");
var getkeys = arrUrl[1].split('/')[3].split('?')[1]
var username = arrUrl[1].split('/')[2]
var touser = ''

// 打开回复区
function open_reply(obj){
    $(obj).css('display','none')
    $(obj).next().css('display','inline-block')
    $(obj).parent().parent().next().slideDown("slow");
    $(obj).parent().parent().next().next().css('display','inline')
    //$(obj).parent().parent().next().css('display','inline-block')
    $(obj).parent().parent().next().find("textarea").css('margin-top',)
}

// 关闭回复区
function close_reply(obj){
    $(obj).parent().parent().next().slideUp("slow")
    $(obj).parent().parent().next().next().css('display','none')
    $(obj).css('display','none')
    $(obj).prev().css('display','inline-block')
    //$(obj).parent().parent().next().css('display','none')
}

// 回复
function send_reply(obj){
    comment_id = $(obj).parent().parent().attr('id')
    content = $(obj).prev().val()
    s = content
    console.log(s)
    if(content.length==0){
        alert('请输入内容')
        return
    }
    $(obj).parent().prev().attr('height', ''+$('.rrr').length*100+'px')
    u = window.localStorage.getItem('travel_user');
    token = window.localStorage.getItem('travel_token');
    if(touser!=''){
        content = $(obj).prev().val().replace("回复>>>"+touser+":","")
        data = {'comment_id':comment_id,'content': content,'touser':touser}
    }else{
         data = {'comment_id':comment_id,'content': content}
    }

    $.ajax({
        url: 'http://127.0.0.1:8000/strategy/'+u+'/message'+'?'+getkeys,
        type: 'post',
        data: JSON.stringify(data),
        beforeSend: function(request){
            request.setRequestHeader("Authorization", token);
        },
        success: function(res){
            alert('评论成功')
            $('#plcount').text((parseInt($('#plcount').text())+1))
            touser = ''
            r = $(obj).parent().prev()
            r_html = r.html()
            r_html += '<div class="rrr" style="height:120px"><div class="left_reply"><a href="/user/info/'+res.data.reply_user+'">'+
                            '<img  width="80px" height="80px" src="/static/media/'+res.data.reply_avatar+'" ></a>'
            r_html+= '<p style="margin-top:0px;text-align:center"><a href="/user/info/'+res.data.reply_user+'">'+res.data.reply_user+'</a></p></div>'
            if(res.data.reply_touser!=null){
                r_html+='<div class="right_reply"><p>回复>>><a href="/user/info/'+res.data.reply_touser+'">'+res.data.reply_touser+'</a>:'+res.data.reply_content+'</p>'
            }else{
                r_html+='<div class="right_reply"><p>'+res.data.reply_content+'</p>'
            }

            r_html+='<div class="send_time" style="padding-top:38px"><p>'+res.data.reply_send_time
            //+'</p></div></div></div>'
            r_html+='&nbsp;&nbsp;&nbsp;<span class="reply_touser"'
            r_html+='onclick="send_reply_touser(this)">回复</span></p></div></div></div>'
            r.html(r_html)
            content = $(obj).prev().val("")
        }
    })
}

function send_reply_touser(obj){
    touser = $(obj).parent().parent().parent().prev().find("p").find("a").text()
    $(obj).parent().parent().parent().parent().parent().next().children(":first").val('回复>>>'+touser+':')

    return
    //send_reply(obj, touser=touser)
}

$(function(){
    var token = window.localStorage.getItem('travel_token');
    var url = document.location.toString();
    var arrUrl = url.split("//");
    var getkeys = arrUrl[1].split('/')[3].split('?')[1]
    var username = arrUrl[1].split('/')[2]

    $.ajax({
        url: 'http://127.0.0.1:8000/strategy/strategy/'+username+'?'+getkeys,
        type: 'get',
        beforeSend: function(request) {
            request.setRequestHeader("Authorization", token);
        },
        success: function(res){
            if(res.code==200){
                // console.log('要访问的用户'+username)
                // console.log('自己'+res.username)
                $('title').text(res.data[0].title)
                if(username==res.username){
                    $('#update_s').css('display','inline');
                    $('#del_s').css('display','inline');
                }
                $('#title').html('<h1>'+res.data[0].title+'</h1>')
                $('#usernameaa').attr('href','/user/info/'+res.author)
                $('#usernameaa').text(res.author)
                $('#content').html(res.data[0].content)
                if(res.pre_strategy != ''){
                    $('#pre_s').text("上一篇："+res.pre_strategy.title)
                    $('#pre_s').attr('href','/strategy/'+username+'/detail?s_id='+res.pre_strategy.id)
                    $('#pre_s').css('display','inline')
                }else{
                    $('#pre_s').css('display','none')
                }
                if(res.next_strategy != ''){
                    $('#next_s').text("下一篇："+res.next_strategy.title)
                    $('#next_s').attr('href','/strategy/'+username+'/detail?s_id='+res.next_strategy.id)
                    $('#next_s').css('display','inline')
                }else{
                    $('#next_s').css('display','none')
                }
                $('#col').css('display','inline-block')
                $('#time').css('display','inline-block')
                $('#time').text(res.data[0].create_time)
                $('#ppinlun').css('display','inline-block')
                $('#plcount').text(res.comment_count)
                $('#liulan').css('display','inline-block')
                $('#llcount').text(res.data[0].browse_nums)
                comments = res.data[0].comment
                comment_html = ''
                for(let i=0; i<comments.length; i++){
                    c_avatar = '<div class="left_comment"><a href="/user/info/'+comments[i].c_user+'">'+
                                            '<img  width="80px" height="80px" src="/static/media/'+comments[i].c_avatar+'" ></a>'
                    //c_name =  '<p>'+comments[i].c_user+'</p></div>'
                    c_name =  '<p style="margin-top:10px"><a href="/user/info/'+comments[i].c_user+'">'+comments[i].c_user+'</a></p></div>'
                    c_left = c_avatar + c_name
                    c_content = '<div class="right_comment"><p>'+comments[i].c_content+'</p></div>'
                    if(comments[i].c_count==0){
                        c_count = ''
                    }else{
                        c_count = '('+comments[i].c_count+')'
                    }
                    c_send_time =  '<div class="send_time"><p>'+comments[i].c_send_time+'&nbsp;&nbsp;&nbsp;'+
                                                    '<span  class="open_reply" onclick="open_reply(this)">回复'+c_count+'</span>'+
                                                    '<span  class="close_reply"  onclick="close_reply(this)">收起回复</span></p></div>'
                    c_reply =  '<div class="reply" style="height:'+(comments[i].c_replys.length*120+'px')+'">'
                    for(let j=0; j<comments[i].c_replys.length;j++){
                        reply = comments[i].c_replys[j]
                        r = '<div class="rrr" style="height:120px"><div class="left_reply"><a href="/user/info/'+reply.r_replyuser+'">'
                        r+='<img  width="80px" height="80px" src="/static/media/'+reply.r_avatar+'" ></a>'
                        r+= '<p style="margin-top:0px;text-align:center"><a href="/user/info/'+reply.r_replyuser+'">'+reply.r_replyuser+'</a></p></div>'
                        if(reply.r_touser!=""){
                            r+='<div class="right_reply"><p>回复>>><a href="/user/info/'+reply.r_touser+'">'+reply.r_touser+'</a>:'+reply.r_content+'</p>'
                        }else{
                            r+='<div class="right_reply"><p>'+reply.r_content+'</p>'
                        }
                        //r+='<div class="right_reply"><p>'+reply.r_content+'</p>'
                        r+='<div class="send_time" style="padding-top:38px"><p>'+reply.r_send_time
                        r+='&nbsp;&nbsp;&nbsp;<span class="reply_touser"'
                        r+='onclick="send_reply_touser(this)">回复</span></p></div></div></div>'
                        c_reply+=r
                    }
                    c_reply+= '</div>'
                    c_reply+= '<div style="display:none"><textarea style="width: 80%;height: 35px;resize:none;margin-left:12%"></textarea>'
                    c_reply+=  '<button style="float:right"  onclick="send_reply(this)">发布</button></div>'
                    c_right = c_content + c_send_time+c_reply
                    comment_html += '<div class="comment"  id="comment'+comments[i].c_id+'">'+c_left + c_right +'</div><hr>'
                    $('#editor').css('display','inline-block')
                    $('#send_comment').css('display','inline')
                }
                if(comments.length==0){
                    $('#editor').css('display','inline-block')
                    $('#send_comment').css('display','inline')
                }
                $('#comment_area').html(comment_html)
            }else{
                alert('失败')
            }
        }

    })
    $('#del_s').click(function(){

        $.ajax({
            url: 'http://127.0.0.1:8000/strategy/strategy/'+username+'?'+getkeys,
            type: 'delete',
            beforeSend: function(request) {
                request.setRequestHeader("Authorization", token);
            },
            success: function(res){
                if(res.code==200){
                    alert('删除成功!')
                    window.location.href = '/strategy/'+ username
                }else{
                    alert(res.error)
                }
            }
        })
    })

    var E = window.wangEditor
    var editor = new E('#editor')
    editor.customConfig.uploadImgHeaders = {
        'Authorization': window.localStorage.getItem('travel_token')
    }

    editor.customConfig.uploadImgServer = '/strategy/upload'
    editor.create()

    // 发送评论
    $('#send_comment').click(function(){
        var u = window.localStorage.getItem('travel_user');
        var content = editor.txt.text()
        var html = $('#comment_area').html()
        $.ajax({
            url: 'http://127.0.0.1:8000/strategy/'+u+'/message'+'?'+getkeys,
            type: 'post',
            data: JSON.stringify({'content': content}),
            beforeSend: function(request) {
                request.setRequestHeader("Authorization", token);
            },
            success: function(res){
                if(res.code==200){
                    alert('评论成功')
                    $('#plcount').text((parseInt($('#plcount').text())+1))
                    c_avatar = '<div class="left_comment"><img width="80px" height="80px" src="/static/media/'+res.data.avatar+'">'
                    c_name =  '<p><a href="/user/info/'+res.data.username+'">'+res.data.username+'</a></p></div>'
                    c_left = c_avatar + c_name
                    c_content = '<div class="right_comment"><p>'+res.data.content+'</p></div>'
                    c_send_time =  '<div class="send_time"><p>'+res.data.create_time+'&nbsp;&nbsp;&nbsp;<span class="open_reply" onclick="open_reply(this)">回复</span></p></div>'
                    c_right = c_content + c_send_time
                    html += '<div class="comment">'+c_left + c_right +'</div>'
                    // html +=''
                    // html += '<div><img src="/static/media/'+res.data.avatar+'"width="80px" height="80px"><p>'+res.data.username+'</p></div>'
                    // html += '<div><p>'+res.data.content+'</p></div>'
                    // html += '<div><p>'+res.data.create_time+'</p></div>'
                    $('#comment_area').html(html)
                }
            }
        })
    })
})

function ccc(obj){
    $(obj).addClass('act')
}

function ccc2(obj){
    if($(obj).children(":first").text()=='我'){
        return
    }
    $(obj).removeClass('act')
}