
var local={
	get:function(name){
		var o=localStorage.getItem(name)||"";
		if( (o==="") || (o.indexOf("{")<0) && (o.indexOf("[")<0) ){ return o; }else{ return JSON.parse(o); }
	},
	set:function(name,val){
		val=typeof(val)==="object"?JSON.stringify(val):val; localStorage.setItem(name,val);
	},
	clear:function(name){
		localStorage.removeItem(name);
	}
};

/*退出登录*/
function outlog(obj){
   $.ajax({
       url:'/logout/',
       type:'get',
       success:function(data){
           local.clear('userInfo');
           window.location.href="/jumplogin/"
       },
       error:function(){
           alert('请求错误，请稍后后重试！')
       }

   })
}
// if(local.get('userInfo')){
//     $(".logname span").html(local.get('userInfo').userName);
// }else{
//     $(".logname span").html('游客');
// }




