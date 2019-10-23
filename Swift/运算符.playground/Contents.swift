import UIKit

var str = "Hello, playground"

// 区间运算符

// 合并空值运算符
func test1 () {
    var a :Int? = nil
    // 可以看做为三元运算符的简写  a != nil ? a! : 10
    var value = a ?? 10
    print(value)
}

//if
//和其他语言一样

//可选项绑定
func option() {
    let a:Int? = nil
    if let value = a { // value的生命周期在这个括号里
        print("value的值为" + "\(value)")
    }else {
        print("value不存在")
    }
}

//option()


//隐式展开
func test3() {
    func test(){
        let a:Int! = 10;// 定义Int! 是确保优值,可以在后面设成nil  如果定义为Int 无法为nil
        //    let b:Int = a // 输出为10
        let b = a // 输出为Optional(10)  需要指定类型
        print(b)
    }
    
    var a: Int! = 10
    a = nil
    print(a)
}

//test3()

// switch语句 // 默认后面有break  如果想穿透添加fallthrough
func test4() {
    func test5() {
        var a = 10
        switch a {
        case 10:
            print("10")
        //        fallthrough
        default:
            print("default")
        }
    }
    
    func test6() {
        var b = (10,true)
        switch b {
        case let (10 ,name2) where name2 == false: //两个都匹配 有限上面这个
            print("情况1")
            print(name2)
            
        case let (name ,name2):  //先匹配这个 如果这个不匹配 在匹配下面这个
            print("情况2")
            print(name)
            print(name2)
            
        case (10,true):
            print("20")
        //        fallthrough
        default:
            print("default")
        }
    }
    test6()
}
test4()
