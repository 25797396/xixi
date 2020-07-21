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
