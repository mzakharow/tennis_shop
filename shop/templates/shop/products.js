var domain = 'http://127.0.0.1:8000/'

window.onload = function () {
    var list = document.getElementById('list');
    list.innerText = "1";

    var productListLoader = new XMLHttpRequest()
    productListLoader.onreadystatechange = function () {
        if (productListLoader.readyState == 4) {
            if (productListLoader.status == 200) {
                var data = JSON.parse(productListLoader.responseText);
                var s = '<ul>';
                for (i = 0; i < data.length; i++) {
                    s += '<li>' + data[i].name + '</li>';
                }
                s += '</ul>'
                list.innerHTML = s;
            }
        }

    }
    list.innerText = "1";
    function productListLoad() {
        productListLoader.open('GET', domain + '/api/products/', true);
        productListLoader.send();
    }
    productListLoad();
}