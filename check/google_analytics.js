/**
 * This file is part of MonitoraPA
 *
 * Copyright (C) 2022 Giacomo Tesio <giacomo@tesio.it>
 *
 * MonitoraPA is a hack. You can use it according to the terms and
 * conditions of the Hacking License (see LICENSE.txt)
 */
setTimeout(function(){
    document.title = "";
    var gaName = window.GoogleAnalyticsObject;
    if(!gaName)
        gaName = "ga"
    if(window[gaName] && window[gaName].l){
        // fast track (thanks Augusto Zanellato)
        console.log("found in window[gaName].q[0][1]", window[gaName].q[0][1]);
        document.title = window[gaName].q[0][1];
        return;
    }
    var html = document.all[0].innerHTML;
    var test = html.match(/UA-[0-9-]+/);
    if(test){
        // simplest possible regex test.
        console.log("found in html.match(/UA-[0-9-]+/)", test);
        test[1] = test[0];
    } else {
        test = html.match(/ga\(['"]create['"], ['"]([^'"]*)['"]/);
    }
    if(test){
        console.log(`found in html.match(/ga\(['"]create['"], ['"]([^'"]*)['"]/)`, test);
    } else {
        var test = html.match(/ga\('create', {[^}]*}/gm);
        if(test){
            objStr = test[0];
            objStr = objStr.replace ("ga('create', ", 'window.MonitoraPAObj = ');
            objStr = objStr.replace ('ga("create", ', 'window.MonitoraPAObj = ');
            eval(objStr);
            test[1] = window.MonitoraPAObj.trackingId;
            console.log(`found in html.match(/ga\('create', {[^}]*}/gm);`, window.MonitoraPAObj);
        }
    }
    if(!test){
        test = html.match(/gtag\(['"]config['"], ['"]([^'"]*)['"]/);
        if(test){
            console.log(`found in html.match(/gtag\(['"]config['"], ['"]([^'"]*)['"]/)`, test);
        }
    }
    if(!test){
        test = html.match(/push\(\[['"]_setAccount['"], ['"]([^'"]*)['"]\]/);
        if(test){
            console.log(`found in html.match(/push\(\[['"]_setAccount['"], ['"]([^'"]*)['"]\]/)`, test);
        }
    }
    if(!test || test[1].match(/_ID/)){
        for(var sc of document.getElementsByTagName('script'))
            if(sc.src.indexOf('googletagmanager') > -1) {
                test = sc.src.match(/UA-[^&]+/);
                if(test){
                    console.log(`found in '${sc.src}'`, test);
                    test[1] = test[0]
                } else {
                    var txtFile = new XMLHttpRequest();
                    txtFile.open("GET", sc.src, true);
                    txtFile.onreadystatechange = function(){  
                        if (txtFile.readyState === 4) {
                            var content = txtFile.responseText;
                            var tId = content.match(/UA-[^'"]+/);
                            if(tId){
                                if(tId.indexOf('d') != -1){
                                    document.title = "GA PRESENT BUT MISCONFIGURED";
                                    console.log(`found inside '${sc.src}'`, document.title);
                                } else {
                                    document.title = tId[0];
                                    console.log(`found inside '${sc.src}'`, tId);
                                }
                            }
                        } 
                    }
                    txtFile.send();
                }
            }
    }

    if(test){
        document.title = test[1];
    }
}, 1000)
