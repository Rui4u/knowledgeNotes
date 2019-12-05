;
window.addEventListener('load', function() {

    var titleArray = ["航班信息", "行程安排", "出行须知", "景点介绍", "酒店信息", "奇幻之夜", "退税说明", "趣味活动", "精彩瞬间"];
    $(".contains div").children("span").each(function(index, element) {
        $(element).children("label").html(titleArray[index]);
        $(element).find("img").prop("src", "img/list/item_image_" + index + ".png ");
    });



    // var spanArray = $(".contains div");

    // spanArray = spanArray.children("span")


    // for (let index = 0; index < spanArray.length; index++) {

    //     var item = spanArray[index];
    //     $(item).children("label").html(titleArray[index]);
    //     // label[0].innerText = titleArray[index];

    //     var img = $(item).find("img");

    //     img.prop("src", "img/list/item_image_" + index + ".png ");
    // }


});