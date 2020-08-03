function ccc(obj){
    $(obj).addClass('act')
}

function ccc2(obj){
    if($(obj).children(":first").text()=='旅游攻略'){
        return
    }
    $(obj).removeClass('act')
}

function write(){
    windows.location.href = '/strategy/writestrategy'
}

$(function(){

    var page_id = window.location.href.replace('http://127.0.0.1:8000/strategy/','');
    $.ajax({
        url: '/strategy/get_info?page_id='+page_id,
        type: 'get',
        success: function(res){
            if(res.code==200){
                s_html = $('#strategy_div').html()
                //alert('请求成功')
                console.log(res.data)
                sum_page = res.sum_page
                current_page = res.current_page
                for(let i=0;i<res.data.length; i++){
                    id = res.data[i].id
                    title = res.data[i].title
                    introduce = res.data[i].introduce+'...'
                    author = res.data[i].author
                    avatar = res.data[i].avatar
                    browse_nums = res.data[i].browse_nums
                    good = res.data[i].good
                    create_time = res.data[i].create_time
                    comment_count = res.data[i].comment_count
                    s_html+='<div class="s_div1"><div  class="s_div2"><div class="s_div_img"> '
                    s_html+='<img src="/static/media/'+avatar+'" style="width: 160px;height: 160px;"></div>'
                    s_html+='<div class="s_div_content"><p><h3>'+title+'</h3></p>'
                    s_html+='<p style="font-size: 15px;">'+create_time
                    s_html+='<span style="font-size: 15px;margin-left:30%">浏览：'+browse_nums+'&nbsp&nbsp&nbsp</span>'
                    s_html+='<span style="font-size: 15px;">评论：'+comment_count+'&nbsp&nbsp&nbsp</span>'+'</p>'
                    s_html+='<p style="margin-top: 15px;font-size: 13px;">'+introduce+'</p></div>'
                    s_html+='<a href="/strategy/'+author+'/detail?s_id='+id
                    s_html+='" class="aaa"><button style="border:none" class="xx" >阅读</button></a></div></div>'
                    s_html+='<div style="border-bottom:1px solid rgba(102,102,102,0.2)"></div>'
                }
                s_html +='<div class="pagination-bar">'
                if(current_page==1){
                    s_html += '<a class="page-prev">上一页</a>'
                }else{
                    s_html += '<a href="/strategy/'+(current_page-1)+'" class="page-prev disabled">上一页</a>'
                }
                for(let i=1; i<=sum_page; i++){
                    if(i==current_page){
                        s_html +='<a style="margin-left:20px" href="/strategy/'+i+'" class="disabled">'+i+'</a>'
                        continue;
                    }
                    s_html +='<a style="margin-left:20px" href="/strategy/'+i+'" class="">'+i+'</a>'
                }
                if(current_page==sum_page){
                    s_html += '<a style="margin-left:20px" class="page-next">下一页</a>'
                }else{
                    s_html += '<a style="margin-left:20px" href="/strategy/'+(current_page+1)+'" class="page-next disabled">下一页</a></div>'
                }


                $('#strategy_div').html(s_html)

            }
        }

    })

})