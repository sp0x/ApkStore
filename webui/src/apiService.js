export const apiService = {
    get,
    post,
    del
};

let API_ADDR = "/";
if(window && window.location && window.location.href.indexOf("localhost:")!=-1){
    //Uncomment this if you're testing
    API_ADDR = "localhost:8006/";
}

//Uncomment this if you're testing
//API_ADDR = "vaskovasilev.eu:81/";
function getUrl(route){
    let scheme = window.location.protocol + "//";
    let base = API_ADDR;
    //let base = API_ADDR;
    if(base[base.length-1]!='/' && route[0]!='/'){
        route = '/' + route;
    }else if(base[base.length-1]=='/' && route[0]=='/'){
        route = route.substring(1)
    }
    if(base=="/"){
        return base + route;
    }else{
        return scheme + base + route;
    }

}

function get(route, options){
    let url = getUrl(route)
    if(!options) options = {
        credentials: 'include'
    };
    return fetch(url, options);
}
function del(route){
    let url = getUrl(route)
    let conf = {
        'method': 'DELETE'
    };
    return fetch(url, conf)
}
function post(route, data, options){
    let url = getUrl(route)
    if(!data && options){
        options.credentials = 'include'
        if(!options.headers['Accept']){
            options.headers['Accept'] = 'application/json, text/plain, */*';
        }
        return fetch(url, options);
    }else{
        var config = {
            method: 'POST'
        }
        var isjson = typeof data == 'object';
        var headers = null;
        if(isjson){
            headers = {};
            headers['Accept']= 'application/json, text/plain, */*';
            headers['Content-Type'] = 'application/json;charset=UTF-8';
        }
        if(options) config = options;
        if(!config['method'] || config['method']!='POST') config['method'] = 'POST';
        if(headers) config['headers'] = headers;
        if(options.asForm){
            delete headers['Content-Type'];
            config['body'] = data
        }else{
            config['body'] = isjson ? JSON.stringify(data) : data;
        }
        config.credentials = 'include';
        return fetch(url, config);
    }
}
