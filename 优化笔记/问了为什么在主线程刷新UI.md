问了为什么在主线程刷新UI









isa是怎么回事儿
分类为什么不能添加属性
afn是怎么实现常驻线程的。 为什么afn3.0取消了
苹果推送原理
runloop 是怎么被唤醒的
自旋锁
互斥锁
tableview上面放了一个tap手势  点击手势   有哪些响应事件
分类里面的有哪些属性。runtime（分类底层  有哪些结构体）
hash算法 除数留余法  字符串数值哈希法  开链法





### 本地缓存

*  本地Manager   负责从本地获取

*  内存Manager  负责从内存中获取

app初始化的时候调用查找本地数据， 本地Manager查到数据的时候往单例`memoryManager` 中存， 下一次查找从`moneryManager`中查找。

存储的对象是一张自定义hash表。 key是userid  value个人信息   序列化， coding协议， 用到runtime

##### 读写锁方案

1. pthread_rwlock 读写锁

2. gcd 自定义的并发队列 async 读操作   +   dispatch_barrier_async（写操作）



### 持久化方案

1. plist文件:属性列表
2. preference:偏好设置
3. NSKeyedArchiver:归档
4. keychain:钥匙串

#### 沙盒

在介绍存储方法之前,先说下沙盒机制.iOS程序默认情况下只能访问程序的目录,这个目录就是沙盒。 沙盒的目录结构如下：

- `应用程序包：`存放的是应用程序的源文件：资源文件和可执行文件

```
NSString *path = [[NSBundle mainBundle] bundlePath];
复制代码
```

- `Documents:`比较常用的目录，itune同步会同步这个文件夹的内容，适合存储重要的数据

```
NSString *path = NSSearchPathForDirectoriesInDomains(NSDocumentDirectory, NSUserDomainMask, YES).firstObject;
复制代码
```

- `Library：`
  1.Caches:tunes不会同步此文件夹，设个存储体积大，不需要备份的重要数据

```
NSString *path  = NSSearchPathForDirectoriesInDomains(NSCachesDirectory, NSUserDomainMask, YES).firstObject;
复制代码
```

- `tmp`itunes不会同步，系统可能在应用没运行时就删除该目录的文件，适合存临时文件，用完就删除：





### NSProxy

##### NSObject寻找方法顺序：本类->父类->动态方法解析-> 消息转发；

##### NSproxy顺序：本类->消息转发；



### 启动优化

```
动态库加载越多，启动越慢。 
ObjC类越多，函数越多，启动越慢。 
可执行文件越大启动越慢。 
C的constructor函数越多，启动越慢。
C++静态对象越多，启动越慢。 
ObjC的+load越多，启动越慢。
```

##### 整体上**pre-main**阶段的优化有：

```
①减少依赖不必要的库，不管是动态库还是静态库；如果可以的话，把动态库改造成静态库； 如果必须依赖动态库，则把多个非系统的动态库合并成一个动态库； ②检查下 framework应当设为optional和required， 如果该framework在当前App支持的所有iOS系统版本都存在，那么就设为required，否则就设为optional， 因为optional会有些额外的检查；  ③合并或者删减一些OC类和函数； 关于清理项目中没用到的类，使用工具AppCode代码检查功能，查到当前项目中没有用到的类（也可以用根据linkmap文件来分析，但是准确度不算很高）； 有一个叫做[FUI](https://github.com/dblock/fui)的开源项目能很好的分析出不再使用的类，准确率非常高，唯一的问题是它处理不了动态库和静态库里提供的类，也处理不了C++的类模板。 ④删减一些无用的静态变量， ⑤删减没有被调用到或者已经废弃的方法， 方法见http://stackoverflow.com/questions/35233564/how-to-find-unused-code-in-xcode-7 和https://developer.Apple.com/library/ios/documentation/ToolsLanguages/Conceptual/Xcode_Overview/CheckingCodeCoverage.html。 ⑥将不必须在+load方法中做的事情延迟到+initialize中，尽量不要用C++虚函数(创建虚函数表有开销) ⑦类和方法名不要太长：iOS每个类和方法名都在__cstring段里都存了相应的字符串值，所以类和方法名的长短也是对可执行文件大小是有影响的； 因还是object-c的动态特性，因为需要通过类/方法名反射找到这个类/方法进行调用，object-c对象模型会把类/方法名字符串都保存下来； ⑧用dispatch_once()代替所有的 attribute((constructor)) 函数、C++静态对象初始化、ObjC的+load函数； ⑨在设计师可接受的范围内压缩图片的大小，会有意外收获。 压缩图片为什么能加快启动速度呢？因为启动的时候大大小小的图片加载个十来二十个是很正常的， 图片小了，IO操作量就小了，启动当然就会快了，比较靠谱的压缩算法是TinyPNG。
```



冷启动 **1200**  热启动**600**

冷启动 **800**  热启动**565**



遇到的问题   父类初始化属性调用子类set方法