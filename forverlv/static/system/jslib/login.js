/**
 * Created by Arvin on 2015-10-22.
 */
(function($){
   function login_callback(callback){
      var ret = callback.ret;
      if(ret == "success"){
        var redirect_to = callback.redirect_to;
        window.location.href = redirect_to;
      };
      if(ret == "failed"){
        var message = callback.message;
        for(var key in message){
          $('.alert').html(message[key][0].message);
        }
      };
   };
   function server_error(XMLHttpRequest, textStatus, errorThrown){
      $('.alert').html($.i18n.prop('Server error login failed.'));
   }
   document.onkeydown = function(event){
      if(event && event.keyCode==13)
      {
          $("#login_btn").click();
          return false;
      }
   };
   $("#login_btn").click(function(){
     var authentication = '{0} <img src="/static/public/imgs/authentication.gif" alt=""/>'.format($.i18n.prop('Login Authentication'));
     $('.alert').html(authentication);
    var form = $("#login_form");
    var login_url = "/accounts/login/";
    $.ajax({
      url:login_url,
      type: "POST",
      dataType: "json",
      data: $(form).serialize(),
      success: login_callback,
      error: server_error
    });
  });
})(jQuery);