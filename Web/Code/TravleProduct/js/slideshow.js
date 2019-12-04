window.addEventListener('load', function() {

    var allow_l = this.document.querySelector(".arrow-l");
    var allow_r = this.document.querySelector(".arrow-r");

    var num = 0;
    var circle = 0;

    var focus = this.document.querySelector('.focus');
    var ul = focus.querySelector('ul');


    var ol = focus.querySelector('.circle');
    this.console.dir(ol)
        // 底部slider
    for (let index = 0; index < ul.children.length; index++) {
        var li = this.document.createElement('li');
        li.setAttribute('data-index', index);
        li.addEventListener('click', function() {
            for (let index = 0; index < ol.children.length; index++) {
                ol.children[index].className = '';
            }
            this.className = 'current';

            var focusWidth = focus.offsetWidth;
            var currentIndex = this.getAttribute('data-index');
            // 修改索引好
            circle = num = currentIndex;


            console.log(currentIndex);
            animate(ul, -currentIndex * focusWidth);

        })
        ol.appendChild(li)
    }

    ol.children[0].className = 'current';

    var first = ul.children[0].cloneNode(true);
    ul.appendChild(first);

    var focusWidth = focus.offsetWidth;
    allow_l.addEventListener('click', function() {

        if (num == 0) {
            num = ul.children.length - 1;
            ul.style.left = -num * focusWidth + 'px';
        }
        console.log(num);
        num--;
        circle--;
        if (circle < 0) {
            circle = ol.children.length - 1;
        }
        animate(ul, -num * focusWidth);
        circleRun();

    });

    allow_r.addEventListener('click', function() {

        if (num == ol.children.length) {
            ul.style.left = 0;
            num = 0;
        }
        num++;
        circle++;
        circle = (circle == ol.children.length) ? 0 : circle;
        animate(ul, -num * focusWidth);
        circleRun();
    });


    function circleRun() {
        console.log(circle);

        for (let index = 0; index < ol.children.length; index++) {
            ol.children[index].className = '';
        }
        ol.children[circle].className = 'current';
    }

    var timer = this.setInterval(function() {
        allow_r.click();
    }, 1500);

});