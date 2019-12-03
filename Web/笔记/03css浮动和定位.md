css 特性

标准流

浮点 float

定位



# 浮动float

float

因为浮动不记录高度 所以根据子空间的内容撑开父控件的高度需要清除高度

清除浮动

```css
clear:
left
right 
both 清除两侧浮动
```

* 额外标签法

  * 在子控件的最后一个控件后添加一个空控件（div）给这个空控件添加clear

* 父级添加`overflow: hidden`属性方法

  * 缺点：内容增多容易造成不会自动换行导致内容被隐藏掉，无法显示需要溢出的元素

* 使用after伪元素清除浮动

  ```css
  .clearfix:after {
    content: "";
    display: block;
    height: 0px;
    visibility: hidden;
    clear: both;
  }
  .clearfix {
    *zoom:1; //ie 6.7
  }
  ```

* 使用双伪元素

  ```css
  .clearfix:after,
  .clearfix:before {
    content:"";
    display:table;
  }
  .clearfix:after {
    clear:both;
  }
  .clearfix {
    *zoom:1; //ie 6.7
  }
  
  ```

  

# CSS属性书写顺序

布局定位属性

自身属性

文本属性 



其他属性



# 定位

定位 = 定位模式 + 边偏移

#### 定位模式

```css
position:
/*静态定位   none*/
static 
/* 相对定位 根据原来位置定位  原来的位置继续占有*/
relative
/* 绝对定位  完全脱标 原来位置不占有 以父元素定位 如果父元素无定位  则以body定位*/
absolute
/*固定定位 完全脱标 不随滚动条滚动 只根据浏览器窗口*/
fixed 
```

##### z轴

`z-index`  

浮动元素、绝对定位（固定定位）元素都不会触发外边距合并问题 之前用overflow解决