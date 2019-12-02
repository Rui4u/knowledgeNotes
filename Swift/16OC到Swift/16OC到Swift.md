```swift
// MARK:类似于#pragmat mark

// TODO:标记未完成的任务

// FIXME:用于标记待修复的问题

#warning("undo")
//可以在需要返回值的地方添加fatalError() 再组合上warning
```



## 条件编译

`swift compiler - custom`  自定义标记

![image-20191115171535562](编译相关1.png)

打印详细

```swift
print(#fine,#line,#function)  //文件名 行数 对象名称
```

系统版本检测

```swift
if #available(iOS 10,macOS 10.12, *) {

}

@available(iOS,deprecated:11)
func run() //run只在iOS 11前使用

@available(*, unavailable,renamed:"name2")
func name1()  //name1改名为name2
```



## iOS入口

```swift
AppDelegate ->@UIApplicationMain 
```

更改入口

```swift
import UIKit

class MyAppDelegate: UIApplication{}

UIApplicationMain(CommandLine.argc,
                  CommandLine.unsafeArgv,
                  NSStringFromClass(MyAppDelegate.self),
                  NSStringFromClass(AppDelegate.self))
```



### 桥接文件

#### Swift调用OC

```swift
{targetName}-Bridging-Header.h
target -> build setting ->bridging 添加文件目录
```

如果c语言定义的和swift定义的冲突 例如

```swift
func add(a: Int32, b: Int32) -> Int32 {
	 a - b
}
int add(int a, int b) {
  return a + b
}
//如果冲突了 优先使用swift
//处理
@_silgen_name("add")
func swift_add(a: Int32, b: Int32) -> Int32 {
	 a + b
}
// 将c语言的add更改为swift的swift_add
// 可以将底层的c替换 可以从github找源码

```



#### OC调用Swfit

```swift
{targetName}-Swift.h
target -> build setting ->generated interface
//如果swift项目想要暴露给Objective-C，首先要继承NSObject
// 需要@objc 暴露给OC
// 在类钱添加@objcMembers  所有成员都暴露给OC  swift的扩展也会暴露

@objcMembers class Car: NSObject {
	var band: String
  func test() {}
}
//或者
class Car: NSObject {
	@objc	var band: String
  @objc func test() {}
}
```

##### @objc

```swift
//可以通过@objc重命名Swift暴露给OC的符号名（类名，属性名，函数名）等
@objc(MJCar)
@objcMembers class Car: NSObject {
	@objc(name)
	var band: String
}
```



#### Swift依然可以使用选择器

```swift
#selector() //只有暴露给oc的方法名才可以使用选择器
```



### 底层实现

* OC调用swift  swift调用oc 都是走runtime 

* swift中调用swift不管什么环境 都走swift虚表 
  *  如果需要runtime的东西 前面加`@objc dynamic`修饰既可

### String

![String和SubString](String和SubString.png)

```swift
//例子1
let str = "123456"
var subStr = str[str.startIndex..<str.index(str.startIndex, offsetBy: 3)]
subStr.append(contentsOf: "999")  //添加后更改base  //如果截取字符串则不会更改base
print(String(subStr))  //123999
print(String(subStr.base))//123999
print(String(str))//123456

//例子2
let str = "123456"
var subStr = str[str.startIndex..<str.index(str.startIndex, offsetBy: 3)]
print(String(subStr))  //123
print(String(subStr.base))//123456  //base为str
print(String(str))//123456
```

#### 说明

系统会优化SubString，当和String值一样的时候，公用一块内存， 当SubString更改后，则自己新开辟内存

* 遵守这个协议 BidirectionalCollection

  三个双引号

  ```swift
  let str = """
  
  					1.13
  						13
  							3
  							
  					"""//以下面对齐
  print(str)
  ```

* String不能转换到NSMutableString 

* NSMutableString 可以桥接为String

* swift 中 `==` 等于 `isEqual`

![Swift、OC桥接转换表](Swift、OC桥接转换表.png)



### 如果Swift继承OC 结构会变

#### 纯swift

8：metaData

8：引用计数相关

成员变量

#### swift继承NSObject

8：isa

成员变量

使用kvc/kvo 必须继承与NSObject  添加的属性要`@objc dynamic`修饰



### Block的方式的KVO

```swift
class Person: NSObject {
    @objc dynamic var age: Int = 0
    var observation: NSKeyValueObservation?
    override init() {
        super.init()   //通过反斜线找到age
        observation = observe(\Person.age, options:.new, changeHandler: { (person, change) in
            print(change.newValue as Any)
        })
    }
}
var p = Person()
p.age = 20
```

### 关联对象

swift，class依然可以使用关联对象

```swift
extension Person {
	  //因为只取变量地址，所以bool值 更省内存
    private static var ISMAN_KEY = false
    var isMan: Bool {
        set{
            objc_setAssociatedObject(self,
                                     &Self.ISMAN_KEY,
                                     newValue,
                                     .OBJC_ASSOCIATION_ASSIGN)
        }
        get{
            objc_getAssociatedObject(self, &Self.ISMAN_KEY) as? Bool ?? false
        }
    }
}
var p = Person()
p.age = 20
p.isMan = true
print(p.isMan)
```

### 资源名管理

1. 仿安卓

   ```swift
   enum R {
     enum image: String {
         case listImg
   	    case homeImg
   	    case mineImg
     }
   }
   
   print(R.image.listImg)  
   ```

   在需要的分类中添加`Extension`,接收`R.image`类型,然后再转成通过`rawValue`转成`字符串`

2. 方式2

   ```swift
   enum R2 {
       enum image {
           static var listImg = Image(named:"logo")
       }
       enum font {
           static func arial(_ size: CGFloat) ->UIFont? {
               UIFont(name:"Arial",size:size)
           }
       }
   }
   
   let img = R2.image.listImg
   ```

   参考思路R.swift 和SwiftGen

### 多线程开发

1. 依赖 利用DispatchWorkItem

```swift
let item = DispatchWorkItem() {
    print("1")
}
DispatchQueue.global().async(execute: item)
item.notify(queue: DispatchQueue.main){
    //item做完 在输出2
    print("2")
}
```

2. 延迟

```swift
let time = DispatchTime.now() + 3
DispatchQueue.main.asyncAfter(deadline: time) {
    print("3秒后再主线程执行操作")
}
```

3. 异步延迟

```swift
typealias Task = () -> ()

@discardableResult
public static func delay(_ sencond: Double,
                        _ block: @escaping Task) -> DispatchWorkItem {
   _asyncDelay(sencond, block)
}
public static func delay(_ sencond: Double,
                        _ block: @escaping Task,
                        _ mainTask: Task?) -> DispatchWorkItem {
   _asyncDelay(sencond, block)
}

@discardableResult
private static func _asyncDelay(_ sencond: Double,
                               _ task: @escaping Task,
                               _ mainTask: Task? = nil) -> DispatchWorkItem {
   let item = DispatchWorkItem(block:task)
   DispatchQueue.main.asyncAfter(deadline: DispatchTime.now() + sencond, execute: item)
   if let main = mainTask {
       item.notify(queue: DispatchQueue.main, execute: main)
   }
   return item
}


class ViewController: UIViewController {
   var item: DispatchWorkItem?
   override func viewDidLoad() {
       super.viewDidLoad()
       print("begin")
       print("1")
       item = TheadTools.delay(3, {
           print("2")
       })
   }
   override func touchesBegan(_ touches: Set<UITouch>, with event: UIEvent?) {
       item?.cancel()
       print("end")
   }
}
```

4. Dispatch_once

swift中不提供dispatch_once  可以用一下集中方式代替

* 属性添加`static` 修饰， 用lldb bt查看调用栈指令  所调用方法被dispatch_once修饰

  ```swift
  static var age: Int = {
      print("todo")
      return 0
  }()
  ```

* 全局中可以用fileprivate修饰

  ```swift
  fileprivate var initTask: Void = {
    private("todo")
  }()
  ```

5. 加锁

   

