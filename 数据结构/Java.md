

java中 数组存储的是对象的地址 8个字节



toString == description

 Finalize == delloc



System.gc()   JVM垃圾回收

重写equals



java可以使用国内部类  最好用static修饰



对外接口一直  可以创建一个interface  只生命公共接口，不去实现， 类似于.h文件

如果想不是所有的都interface都实现， 使用abstract修饰

```java
public abstract class AbstractList<E> implements {
  
}
```



类后面添加  implements   去实现 



protected 子类可以调用



extend 继承





### 内存管理

gc root对象  如果对象不被gc root引用 就会被释放  



#####gc root 对象

* 被局部变量指向的对象



