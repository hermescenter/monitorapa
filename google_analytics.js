setTimeout(function(){
	var html = document.all[0].innerHTML;
	var test = html.match(/ga\('create', '([^']*)'/);
	if(!test){
		var test = html.match(/ga\('create', {[^}]*}/gm);
		if(test){
			objStr = test[0].replace ("ga('create', ", 'window.MonitoraPAObj = ');
			eval(objStr);
			test[1] = window.MonitoraPAObj.trackingId;
		}
	}
	if(!test){
		test = html.match(/gtag\('config', '([^']*)'/);
	}


	if(test){
		document.title = test[1];
	} else {
		document.title = "";
	}
}, 0)
