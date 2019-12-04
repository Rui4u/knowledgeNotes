;
window.addEventListener('load', function() {
    var contain = this.document.querySelector('.contains');
    var itemdiv = contain.querySelector('div')

    var titleArray = ["航班信息", "行程安排", "出行须知", "景点介绍", "酒店信息", "奇幻之夜", "退税说明", "趣味活动", "精彩瞬间"];
    for (let index = 0; index < itemdiv.children.length; index++) {

        var item = itemdiv.children[index];
        var label = item.children[1];

        label.innerText = titleArray[index];
        this.console.log(label)
    }


});