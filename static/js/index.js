$(function(){

    $('#pre_img').hover(function(){
        $('#pre_img').css('opacity',1)
    },function(){
        $('#pre_img').css('opacity',0.5)
    });

    $('#next_img').hover(function(){
        $('#next_img').css('opacity',1)
    },function(){
        $('#next_img').css('opacity',0.5)
    });

    var lunbDiv = $('#lunbotu')
    $.ajax({
        url: 'http://127.0.0.1:8000/get_index_data',
        type: 'get',
        success: function(res){
            if(res.code==200){

            }

            }
        })


    // 左侧按钮
    var left_btn = document.getElementById('pre_img');
    // 右侧按钮
    var right_btn = document.getElementById('next_img');

    // 默认显示的第一张
    var i = 0
    // 找图片
    var items = document.getElementsByClassName('item');
    var b_items = document.getElementsByClassName('b_item');

    b_items[0].onclick = function(){
        if(i==0){
            return
        }else{
            items[i].className = 'item';//去掉当前的图片的active
            b_items[i].className = 'b_item'

            items[0].className = 'item active';//将找到的图片添加active
            b_items[0].className = 'b_item active';
            i=0
        }
    }
    b_items[1].onclick = function(){
        if(i==1){
            return
        }else{
            items[i].className = 'item';//去掉当前的图片的active
            b_items[i].className = 'b_item'
            items[1].className = 'item active';//将找到的图片添加active
            b_items[1].className = 'b_item active';
            i=1
        }
    }
    b_items[2].onclick = function(){
        if(i==2){
            return
        }else{
            items[i].className = 'item';//去掉当前的图片的active
            b_items[i].className = 'b_item'
            items[2].className = 'item active';//将找到的图片添加active
            b_items[2].className = 'b_item active';
            i=2
        }
    }
    b_items[3].onclick = function(){
        if(i==3){
            return
        }else{
            items[i].className = 'item';//去掉当前的图片的active
            b_items[i].className = 'b_item'
            items[3].className = 'item active';//将找到的图片添加active
            b_items[3].className = 'b_item active';
            i=3
        }
    }

    left_btn.onclick = function(){
        items[i].className = 'item';//去掉当前的图片的active
        b_items[i].className = 'b_item'
        i--;//找下一个图片的索引
        if(i<0){
            i = items.length-1;//最后一张图的索引值
        }
        items[i].className = 'item active';//将找到的图片添加active
        b_items[i].className = 'b_item active';
    }

    right_btn.onclick = function(){
        items[i].className = 'item';//去掉当前的图片的active
        b_items[i].className = 'b_item'
        i++;//找下一个图片的索引
        if(i==items.length){//最后一张图递增变成第一张图
            i = 0;
        }
        items[i].className = 'item active';//将找到的图片添加active
        b_items[i].className = 'b_item active';
    }

    // 将右侧按钮点击功能直接交给定时器执行
    var timer = setInterval(right_btn.onclick,3000);
    var silder = document.getElementById('silder');
    // 当鼠标移入到silder上 停止定时器
    silder.onmouseover = function(){
    
        clearInterval(timer);
        $(".item").css({
            height:"105%",
            width:"105%",
        })
    }

    // 当鼠标移出silder 启动定时器
    silder.onmouseout = function(){
        // 新启动的定时器的id要保存在全局 供停止定时器函数使用
        timer = setInterval(right_btn.onclick,3000);
        $(".item").css({
            height:"100%",
            width:"100%",
        })
    }

    var imgs = document.getElementById('imgs');
    imgs.onclick = function(){
        switch(i){
            case 0:
                alert('这是第1张图')
                break
            case 1:
                alert('这是第2张图')
                break
            case 2:
                alert('这是第3张图')
                break
            case 3:
                alert('这是第4张图')
                break
            default:
                break

        }
    }

    $.ajax({
        url: 'http://127.0.0.1:8000/recommend/all',
        type: 'get',
        success: function(res){
            if(res.code==200){
                s_html = ''
                for(var i=0; i< res.strategys.length;i++){
                    id =res.strategys[i].id
                    introduce = res.strategys[i].introduce+'...'
                    username = res.strategys[i].username
                    title = res.strategys[i].title
                    avatar = res.strategys[i].avatar
                    create_time = res.strategys[i].create_time
                    content = res.strategys[i].content
                    
                    s_html+='<div class="s_div1"><div  class="s_div2"><div class="s_div_img"> ' 
                    s_html+='<img src="/static/media/'+avatar+'" style="width: 240px;height: 220px;"></div>'
                    s_html+='<div class="s_div_content"><p><h3>'+title+'</h3></p>'
                    s_html+='<p style="font-size: 15px;">'+create_time+'</p>'
                    s_html+='<p style="margin-top: 15px;font-size: 13px;">'+introduce+'</p></div>'
                    s_html+='<a href="/strategy/'+username+'/detail?s_id='+id
                    s_html+='" class="aaa"><button class="xx" >阅读</button></a></div></div>'
                }
                $('#stuijian').html(s_html)
            }

            }

    })

})

function ccc(obj){
    $(obj).addClass('act')
}

function ccc2(obj){
    if($(obj).children(":first").text()=='首页'){
        return
    }
    $(obj).removeClass('act')
}

