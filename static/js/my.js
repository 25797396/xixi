$(document).scroll(function() {
           var scroH = $(document).scrollTop(); //滚动高度
           var viewH = $(window).height(); //可见高度
           var contentH = $(document).height(); //内容高度

            if(scroH >50){ //距离顶部大于100px时

                $('.navbra').addClass('navh')
                $('.navbra').css('top',scroH)
                $('.navbra').css('background-color','rgba(255,255,255,0.9)')

            }else{
                $('.navbra').removeClass('navh')
            }
            if (contentH - (scroH + viewH) <= 100){ //距离底部高度小于100px

            }
            if (contentH = (scroH + viewH)){ //滚动条滑到底部啦

            }

        });

function check(){
    var t_token = window.localStorage.getItem('travel_token');
    var t_user = window.localStorage.getItem('travel_user');
    if(t_token==null || t_user==null){
        $('#gif_login').css("display","none");
        $('#li_login').css("display","inline");
        return false;
    }
    data = {"t_token":t_token, "t_user": t_user};
    $.ajax({
        url: 'http://127.0.0.1:8000/islogin',
        data: JSON.stringify(data),
        type: 'POST',
        contentType: 'application/json',
        success: function(res){
            if(res.code == 200){
                $('#li_login').css("display","none");
                $('#gif_login').css("display","none");
                $('.dropdown').css("display","inline");
                $('#user_profile').attr("href",'/user/info/'+res.username);
                $('#my_strategy').attr("href",'/strategy/'+res.username);
                if(document.location.toString().indexOf("/user/login") != -1){
                    top.location.href = '/index'
                }
            }else{
                $('#gif_login').css("display","none");
                $('#li_login').css("display","inline");
            }
        }
    })
    return true;
}

function logout(){
    var t_token = window.localStorage.getItem('travel_token');
    var t_user = window.localStorage.getItem('travel_user');

    if(t_token!='' && t_user!=''){
        window.localStorage.removeItem('travel_token');
        window.localStorage.removeItem('travel_user');
    }
}

$(function(){
      is_login = check()
})

