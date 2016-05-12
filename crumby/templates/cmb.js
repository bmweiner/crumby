(function() {
  function readCookie(name) {
  	var nameEQ = name + "=";
  	var ca = document.cookie.split(';');
  	for(var i=0;i < ca.length;i++) {
      var c = ca[i];
  		while (c.charAt(0)==' '){
        c = c.substring(1,c.length);
      }
  		if (c.indexOf(nameEQ) == 0){
        return c.substring(nameEQ.length,c.length);
      };
  	}
	 return null;
  }
  var cid = readCookie('cid');
  if(!cid){
    cid = Math.round(2147483647 * Math.random());
    document.cookie = 'cid='+cid;
  };
  var props = {v:1,
               cid:cid,
               ul:window.navigator.userLanguage || window.navigator.language,
               sd:screen.colorDepth+'-bit',
               sr:screen.width+'x'+screen.height,
               de:document.characterSet,
               dl:document.location.href,
               dt:document.title,
               dr:document.referrer};
  var qstr = '';
  for (var prop in props) {
    qstr += prop+"="+encodeURIComponent(props[prop])+'&';
  }
  qstr = qstr.substring(0, qstr.length - 1);
  var img = new Image;
  var gif_id = Math.round(2147483647 * Math.random());
  img.src = window.location.protocol + '//%s/'+gif_id+'.gif?'+qstr;
})();
