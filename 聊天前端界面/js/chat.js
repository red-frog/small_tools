/*发送消息*/
function send(headSrc,str){
	var html="<div class='send'><div class='msg'><img src="+headSrc+" />"+
	"<p><i class='msg_input'></i>"+str+"</p></div></div>";
	upView(html);
}
/*接受消息*/
function show(headSrc,str){
	var html="<div class='show'><div class='msg'><img src="+headSrc+" />"+
	"<p><i class='msg_input'></i>"+str+"</p></div></div>";
	upView(html);
}
/*更新视图*/
function upView(html){
	$('.message').append(html);
	var h = $('.message').outerHeight()-window.innerHeight;
    $(document).scrollTop(h);
}
function sj(){
	return parseInt(1)
}
$(function(){
	$('.footer').on('keyup','input',function(){

		if($(this).val().length>0){
			$(this).next().css('background','#87CEFA').prop('disabled',true);
		
		}else{
			$(this).next().css('background','#ddd').prop('disabled',false);
		}
	})
	$('.footer p').click(function(){
	    if($('.text').val() != ""){
		show("./images/touxiangm.png",$(this).prev().val());
		test();
		$('.text').val("")
		}
	})
	document.onkeydown = function(e){
        var ev = document.all ? window.event : e;
        if(ev.keyCode==13) {
        if($('.text').val() != ""){
            show("./images/touxiangm.png",$(".text").val());
            test();
            $('.text').val("")
            }
        }
    }

})

/*测试数据*/
var arr=['你好,我是小U!'];
var imgarr=['images/touxiang.png','images/touxiangm.png']

function test(){
	$(arr).each(function(i){
		setTimeout(function(){
			send("images/touxiang.png",arr[i])
		},sj()*500)
	})
}
