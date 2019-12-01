`pre`标签

显示代码中的文字格式

###### class 和id区别

```css
/*定义class*/
.font {
    font-size: 30px;
}
/*定义id*/
#customId {
    font-size: 40px;
}
/*通配符选择器*/
* {
    font-size: 40px;
}
```



* class可以多次使用

* id只能使用一次

  

###### font

综合写法

```css
/*fontt-style font-weight font-size font-family*/\
/*其他可以忽略 字体和大小不能忽略*/
font: italic 700 20px "微软雅黑";
```



###### 后代选择器

```css
div strong｛

｝
```



###### 子元素选择器

```css
div>strong｛

｝
```

###### 交集选择器 

```css
p.red {
  /*既是p标签  类名是.red*/
}
```

###### 并集选择器 

```css
p, 
span {
 /*p 和span标签*/ 
}
```

###### 伪类选择器

* a:link 未访问的连接
* a:visited 已访问的连接
* a:hover 鼠标移动到的连接
* a:active  选定的连接

##### 标签显示模式

###### 块级元素

```css
h1 - h6
div
ul
ol
li
```

特点：

* 独占一行
* 高度、宽度、内外边距可控制
* 宽度默认是容器的100%
* 是一个容器盒子，可以放行内元素或者块级元素

###### 行内元素

```css
a
strong
b
em
i
del
s
ins
u
span
```



特点

* 相邻元素放在一行上
* 无法直接设置高宽
* 默认宽度就是内容宽度
* 行内元素之鞥呢容纳文本或者其他行内元素
* 连接内不能再放连接
* 特殊情况a里面可以放块级元素，但是给a转换一下块级模式最安全

###### 行内块元素

```css
img
input
td
```

特点

* 在一行显示，会有空白缝隙
* 默认宽度就是本身宽度
* 高度，行高，内外边距都可以控制

###### 标签显示模式转换

```css
display: inline
display: block
display: inline-block
```



##### background

```css
background-attachment:fixed 背景固定
background-position:center 49px
background-repeat: no-repeat; 平铺方式
```

简写

```css
/*颜色 图片地址 平铺 滚动 位置*/  不强制顺序
background: 
```

##### css的继承

```
text-  font- line- 以及文字颜色可以继承
```

css优先级

权重计算公式

| 标签选择器         | 权重    |
| ------------------ | ------- |
| 继承和通配符       | 0,0,0,0 |
| 标签选择器         | 0,0,0,1 |
| 类选择器，伪类     | 0,0,1,0 |
| id                 | 0,1,0,0 |
| 行内样式表 style = | 1,0,0,0 |
|                    |         |





#### 