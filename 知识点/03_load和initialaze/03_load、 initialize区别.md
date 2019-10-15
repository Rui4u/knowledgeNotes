## load、 initialize区别

#### load、 initialize区别

1. 调用方式的区别

   1. load 获取函数指针地址直接调用。

   2. msgSend调用。

2. 调用时刻

   1. runtime加载类、分类的时候调用。
   2. initialize是类第一次接受消息的时候调用。



#### load、 initialize 调用顺序

1. load
   1. 先调用类的load。
      1. 先调用先编译的类的load。
      2. 调用子类前先调用父类的load。
   2. 在调用分类的load。
      1. 先调用先编译的分类的load。
2. initialize
   1. 调用子类的initialize时，先初始化父类，后初始化子类。

