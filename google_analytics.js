setTimeout(function(){
	document.title = "";
	var gaName = window.GoogleAnalyticsObject;
	if(!!gaName)
		gaName = "ga"
	if(window[gaName] && window[gaName].l){
		// fast track (thanks Augusto Zanellato)
		document.title = window[gaName].q[0][1];
		return;
	}
	var html = document.all[0].innerHTML;
	var test = html.match(/ga\(['"]create['"], ['"]([^'"]*)['"]/);
	if(!test){
		var test = html.match(/ga\('create', {[^}]*}/gm);
		if(test){
			objStr = test[0];
			objStr = objStr.replace ("ga('create', ", 'window.MonitoraPAObj = ');
			objStr = objStr.replace ('ga("create", ', 'window.MonitoraPAObj = ');
			eval(objStr);
			test[1] = window.MonitoraPAObj.trackingId;
		}
	}
	if(!test){
		test = html.match(/gtag\(['"]config['"], ['"]([^'"]*)['"]/);
	}
	if(!test){
		test = html.match(/push\(\[['"]_setAccount['"], ['"]([^'"]*)['"]\]/)
	}
	if(!test){
		for(var sc of document.getElementsByTagName('script'))
			if(sc.src.indexOf('googletagmanager') > -1) {
				var txtFile = new XMLHttpRequest();
				txtFile.open("GET", sc.src, true);
				txtFile.onreadystatechange = function(){  
					if (txtFile.readyState === 4) {
						var content = txtFile.responseText;
						var tId = content.match(/UA-[^'"]+/);
						if(tId){
							document.title = tId[0];
						}
					} 
				}
				txtFile.send()
			}
	}

	if(test){
		document.title = test[1];
	}
}, 2000)
