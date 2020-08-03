$(function(){
        $('#l_username').focus(function(){
            $('#login_error').text('')
        });

        $('#l_password').focus(function(){
            $('#login_error').text('')
        });
    })

// 登录
function login(){
    var username = $('#l_username').val()
    var password = $('#l_password').val()
    var data = {"username": username, "password": password}

    if(username== '' || password==''){
        alert('请输入完整信息')
        return
    }

    $.ajax({
        url: 'http://127.0.0.1:8000/user/login_check',
        data: JSON.stringify(data),
        type: 'POST',
        contentType: 'application/json',
        success: function(res){
                if(res.code == 200){
                    alert('登录成功')
                    window.localStorage.setItem('travel_token', res.data.token);
                    window.localStorage.setItem('travel_user', res.username);
                    top.location.href = '/index'
                }else{
                    console.log(1)
                    $('#login_error').text(res.error)
                }
        }

    })
}

// 注册
function regist(){
      var username = $('#r_username').val();
      var password = $('#r_password').val();
      var password2 = $('#r_password2').val();
      var email = $('#r_email').val();
      var phone = $('#r_phone').val();
      var code = $('#r_code').val();
      var data = {"username": username, "password": password, "password2": password2, "email": email,"phone":phone, "code": code}

      if(username == ''){
        alert('请输入用户名')
        return
      }

      if(username.indexOf(" ")>0){
        alert('用户名不能有空格')
        return
      }

      if(password == '' || password2 == ''){
        alert('请输入密码')
        return
      }
      if(password != password2){
        alert('两次密码不一致')
        return
      }

      if(phone == ''){
        alert('请输入手机号')
        return
      }

      if(code == ''){
        alert('请输入验证码')
        return
      }

      var reg_email =  /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
      if(!reg_email.test(email)){
            alert('邮箱格式错误')
            return
      }

      if(!(/^1[3456789]\d{9}$/.test(phone))){
        alert("手机号码有误");
        return
      }

      $.ajax({
              url: 'http://127.0.0.1:8000/user/register',
              data: JSON.stringify(data),
              type: 'POST',
              contentType: 'application/json',

              success: function(res){
                      if(res.code == 200){
                          alert('注册成功')
                          top.location.href = '/user/login'
                      }else{
                          alert(res.error)
                      }
              }
      })
 }

var countdown=60;
function settime(obj) {
    phone = $('#r_phone').val()
    if(phone==''){
      return;
    }
    if (countdown == 0) {
        obj.removeAttribute("disabled");
        obj.innerText="获取验证码";
        countdown = 60;
        $('#send_xx').removeClass('dissend_xx')
        return;
    } else {
        obj.setAttribute("disabled", true);
        obj.innerText="重新发送(" + countdown + ")";
        countdown--;
    }
    setTimeout(function() {
        settime(obj) }
    ,1000)
}

function addD(){
  phone = $('#r_phone').val()
  if(phone==''){
      return;
  }
  $('#send_xx').addClass('dissend_xx')
}

// 发送验证码
function sendSMS(){
    console.log('发送验证码')
    //获取 phone框的值
    //发送ajax  POST  请求，让后端发送短信
    //url: http://127.0.0.1:8000/v1/users/sms
    // alert('短信已发送')

    phone = $('#r_phone').val()
    if(phone==''){
      alert('请输入手机号');
      return;
    }
    $.ajax({
        url: 'http://127.0.0.1:8000/user/sms',
        type: 'POST',
        data:	JSON.stringify({"phone":phone}),
        contentType: "application/json",
        dataType: "json",
        success: function(res){
                if(res.code==200){
                    alert('发送成功')
                }else{
                    alert(res.error)
                }
        }

    })

}

