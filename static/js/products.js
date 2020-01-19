var domain = 'http://127.0.0.1:8000/'

window.onload = function () {
    var id = document.getElementById('id');
    var title = document.getElementById('title');
    var brand = document.getElementById('brand');

    var productLoader = new XMLHttlRequest()
    productLoader.onreadystatechange = function() {
        if (productLoader.readyState == 4) {
            if (productLoader.status == 200) {
                var data = JSON.parse(productLoader.responseText);
                id.value = data.id;
                title.value = data.title;
                brand.value = data.brand;
            } else {
                window.alter(productLoader.statusText);
            }
        }
    }

    function productLoad(evt) {
        evt.preventDefault();
        var url = evt.target.href;
        productLoader.open('GET', url, true);
        productLoader.send();
    }
    var list = document.getElementById('list');

    var productListLoader = new XMLHttpRequest()
    productListLoader.onreadystatechange = function () {
        if (productListLoader.readyState == 4) {
            if (productListLoader.status == 200) {
                var data = JSON.parse(productListLoader.responseText);
                var s = '<ul>';
                for (i = 0; i < data.length; i++) {
                    d = data[i];
                    detail_url = '<a href="' + domain + 'api/products/' +
                        d.id + '/" class="detail">Вывести</a>';
                    s += '<li>' + d.title + ' (' + d.brand + ')  [' +
                    detail_url + ']</li>';
                }
                s += '</ul>'
                list.innerHTML = s;
                links = list.querySelectorAll('ul li a.detail');
                for (var i = 0; i < links.length; i++) {
                    links[i].addEventListener('click', productLoad);
                }
            }
        }

    }
    function productListLoad() {
        productListLoader.open('GET', domain + 'api/products/', true);
        productListLoader.send();
    }
    productListLoad();
}