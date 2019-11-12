### 自定义错误

swift可以通过Error协议 自定义错误信息

方法前用throws修饰

```swift
struct CustomError : Error {
  case error1(String)
  case error2(String)
  case error3(String)
}

func test(a:Int) throws -> Int {
  if a == 0 {
		throw CustomError.error1("0不能作为除数")
  }
  return 2/a
} 
```

1. 用`do catch` 来捕捉

```swift
func docatch {
  do {
    
    defer {
		 //无论是否抛出异常，都在执行完docatch前执行此处代码
    }
    defer {
			//如果有多个defer  先定义 后执行
    }
		// 发现异常后停止，走catch捕捉
  	try test(0)
    
	} catch let CustomError.error1(msg){
  
	} catch let CustomError.error2(msg){
  
	} catch let CustomError.error3(msg){
  
	} catch {
    //所有异常都可以捕捉
  }
}

func docatch {
  do {
		// 发现异常后停止，走catch捕捉
  	try test(0)
    
	} catch is CustomError{
    ...
  } catch {
    
  }
}

func docatch {
  do {
		// 发现异常后停止，走catch捕捉
  	try test(0)
    
	} catch let error as CustomError{
    ...
  } catch {
    
  }
}
```

2. 抛给上层函数

```swift
func docatch throws{
	try test(0)
}
```

   **如果没有人捕捉，程序将崩溃**



### try? try!

* 如果抛出错误则返回nil，否则返回值被包装成Optional
* try! 隐式解包

### rethrows

函数本身不会抛出错误，但调用闭包参数抛出错误，那么他会将错误向上抛

```swift
func exec(_ fn:(Int,Int) ->throw Int, _ num1: Int, _ num2: Int) rethrows -> void{
	print(try fn(num1,num2))
}	

try exec(fun1,20,0)
```

## 泛型（Generics）

 

泛型可以将类型参数化，提高代码复用率，减少代码量

```swift
var a = 10;
var b = 20
func swap<T> (_ a: inout Int, _ b: inout Int) {
  (a,b) = (b,a)
}

var fn:(inout Int, inout Int) -> void = swap
swap(&a,&b)
```



```swift
class Stack<E> {...}
```

泛型原理：通过`matadata`元信息来确定参数内容如何实现的

### 关联类型

```swift
protocol Stackable {
  associatedtype Element  // 泛型占位
	mutating func push(_ element Element)
  mutating func pop() ->Element
  func top() -> Element
  func size() ->Int
}
```

### 类型约束

```swift
func swap<T: Person & Runnable> {
  // 泛型必须是person并且遵循runnable协议
}
```



```swift
protocol Stackable {
  associatedtype Element: Equatable
}

class Stack<E: Equatable> :Stackable {
  typealias Element = E
}

func equal<S1: Stackable, S2: Stackable> (_ s1: S1, _s2: S2) -> Bool 
where S1.Element == S2.Element, S1.Element: Hashable  //添加复杂限定。S1和S2的类型必须相等。而且S1的类型必须可以被哈希
{
  return false
}
```

### some（不透明类型）只开放部分接口

`some`只能限制返回一种类型

如果协议中带有`associatedtype`，协议被当做返回值，会出现问题： 编译器在编译的时候不确定是返回那种类型，有两种解决方法

1. `some` 只返回一种类型， 这样编译器就知道了具体是哪种
2. 通过给方法设置泛型，然后再定义的时候确定泛型，这样编译器就知道返回哪种