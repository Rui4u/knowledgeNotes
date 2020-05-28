 #### @Property包含修饰符分为4类

1. 原子性： `atomic`

2. 读写权限： `readlyonly`

3. 内存管理：`copy` `strong` `assgin` `weak`

4. 方法名：`getter` `setter`方法
5. 不常用的：`nonnull`,`null_resettable`,`nullable`

如果重写getter,setter方法时候， kvc可能会找不到。

##### 不建议重写setter方法，除非后台返回字段为init开头，防止生成getter的时候，误认为是构造方法。



### 利用runtime做过什么

1. 模型转化, 类分析
2. 捕捉消息转发
3. 序列化、copy 协议等
4. 访问私有变量 例如TextFile的placeholder颜色
5. 关联对象
6. Method Swizzling 问题：检查父类是否存在该类，是否交换过。



### Block 

* `_NSConcreteStackBlock`： 只用到外部局部变量、成员属性变量，且没有强指针引用的block都是StackBlock。 StackBlock的生命周期由系统控制的，一旦返回之后，就被系统销毁了。

* `_NSConcreteMallocBlock`： 有强指针引用或copy修饰的成员属性引用的block会被复制一份到堆中成为MallocBlock，没有强指针引用即销毁，生命周期由程序员控制

* `_NSConcreteGlobalBlock`： 没有用到外界变量或只用到全局变量、静态变量的block为_NSConcreteGlobalBlock，生命周期从创建到应用程序结束。



##### 以上4种情况，系统都会默认调用copy方法把Block赋复制

1. 手动调用copy
2.  Block是函数的返回值 
3. Block被强引用Block被赋值给__strong或者id类型 
4. 调用系统API入参中含有usingBlcok的方法





全局定时器。 NSHashTable弱持有控件的方案;
