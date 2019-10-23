//: [Previous](@previous)

import Foundation

var str = "Hello, playground"

//基础数据类型
var b :Int = 8
var c :Bool = false
// 类型
print(type(of: b),str)
// 拼接字符串"\()"
print("\(b)" + "\(c)")


// 类型别名
typealias SR = Int
let d :SR
print(type(of: d))

print(String(12))
print(String(true))
//强制转换类型为Optional
print(Int("123"))  //Optional(123)
print(Int("hello"))  // nil


var a = "hello"
var e = Double(a) ?? 0
print(e)  // nil
//--------------------------------------------------------------------------------
// 元祖  将不同类型的元素包装到一起
var f = (1,2,3,"4",true)
var g :(Int, Float) = (1, 1.2)


print(f.0)
print(f.1)
print(f)

var h = f; // 值传递
print("h = "+"\(h)")
f.0 = 2
print("ｆ = "+"\(f)")

var i:(name:String ,name2 :String) = (name: "1",name2:"2")
print(i.name + i.name2)


var (name3,name4) = ("swift","name4")
print(name3)
print(name4)

var (_,name5) = (1,"name5") // _忽略
print(name5)


