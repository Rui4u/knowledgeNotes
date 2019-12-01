###### 块级盒子水平居中满足下面条件

*  盒子必须指定了宽度
* 左右边距都设置为auto

###### 设置margin会产生塌陷

解决垂直塌陷方式

* 嵌套关系
  * 设置父元素设置上边框的border-top:1px solid transparent
  * 可以给父元素指定一个padding-top:1px
  * 给父元素添加overflow:hidden

