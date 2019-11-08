//
//  main.swift
//  汇编分析枚举内存分布
//
//  Created by iOS on 2019/11/4.
//  Copyright © 2019 iOS. All rights reserved.
//

enum TestEnum {
    case test1(Int,Int,Int)
    case test2(Int)
    case test3(Bool)
}

var t = TestEnum.test1(1,2,3)
t = .test2(20)



print(MemoryLayout<TestEnum>.size) //实际用多少
print(MemoryLayout<TestEnum>.stride) //分配多少
print(MemoryLayout<TestEnum>.alignment) //对齐
/**
 25 // test1最大占24个字节。所以取最大 +1  1是标记是哪个case（成员值）
 32 // 因为对齐为8 所以补充到32
 8  //对齐方式
 */
enum TestEnum2 {
    case test1(Int)
}
print(MemoryLayout<TestEnum2>.size) //8
print(MemoryLayout<TestEnum2>.stride) //8 只有一个枚举对象，不用区分所以不多分配
print(MemoryLayout<TestEnum2>.alignment) //8


enum TestEnum3 {
    case test1
}
print(MemoryLayout<TestEnum3>.size) //0 ，唯一确定，不用分配内存
print(MemoryLayout<TestEnum3>.stride) //1
print(MemoryLayout<TestEnum3>.alignment) //1


enum TestEnum4 {
    case test1
    case test2
    case test3
}
print(MemoryLayout<TestEnum3>.size) //1
print(MemoryLayout<TestEnum3>.stride) //1
print(MemoryLayout<TestEnum3>.alignment) //1


/**
 ## 汇编指令
 // 将%rbp - 0x18地址对应的数据，赋值给rax
 movq -0x18(%rbp) , %rax
 
 // 将%rbp - 0x18地址，赋值给rax
 leaq - 0x18(%rbp), %rax
 */
