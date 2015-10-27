/**
 * Created by Arvin on 2015-10-22.
 */
/**
 * "{0},{1}".format("jack","tom") => "jack, tom"
 * @returns {String}
 */
String.prototype.format = function(){
 if(arguments.length==0) return this;
 for(var s=this, i=0; i<arguments.length; i++)
  s=s.replace(new RegExp("\\{"+i+"\\}","g"), arguments[i]);
 return s;
};
/**
 * load i18n file
 */
function loadProperties(){
	jQuery.i18n.properties({
		name:'strings', //source file prefix
		path:'/static/public/i18n/', //source file path
        language: 'en', //i18n language
		mode:'map' //use map type
	});
};
loadProperties();

$.ajax({
  dataFilter: function(data, dataType){
    var ret = data.ret;
    if(ret == 'timeout'){
      var login_url = data.url;
      window.location.href = login_url;
    }else{
      return data;
    }
  }
});