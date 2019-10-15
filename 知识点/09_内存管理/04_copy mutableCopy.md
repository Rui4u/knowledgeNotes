####Copy和MutableCopy



#### 拷贝的目的

拷贝出一个和原对象的相同的副本，互不影响



#### 举个例子

```objc
    NSString *a = [NSString stringWithFormat:@"abcabcabc"];
    NSString *b = [a copy];
    NSString *c = [a mutableCopy];
    
    NSLog(@"%@,%@,%@",a,b,c);
    NSLog(@"%p,%p,%p",a,b,c);	
```

输出结果：

```objc
abcabcabc,abcabcabc,abcabcabc
0xf9f7789ebc9c00cc,0xf9f7789ebc9c00cc,0x6000011f7090
```

#### 疑问

* 为什么a 和b 地址一样
  * 我们思考一下，由于a 为不可变字符串，本身就是不可以改变的。所以只需要拷贝一个新的指针去指向a指向的地址就可以了。  而c是a `mutableCopy`得来的。因为变成`NSMutableString` 而且不影响之前的对象，所以要拷贝出一个新的内存空间。

所以这里就引出一个概念

- 深拷贝  
  - 内容拷贝 
  - 创建新对象

- 浅拷贝 
  -  指针拷贝
  - 引用计数+1

*  为什么浅拷贝要引入计数+1 因为a 和 b 指向同一个内存地址。 如果不引用计数+1，会造成[a release]的时候 a对应的空间引用计数为0，造成释放。而此时b 还在引用释放的内存空间，就会产生坏内存访问的崩溃现象



#### 其他拷贝对象同理

不可变copy 为浅拷贝



#### 注意

Tagged Pointer对象比较特殊。不用管理引用计数。

```objc
  NSString *a = [NSString stringWithFormat:@"abc"];
  NSLog(@"a retainCount = %ld",[a retainCount]);

  NSString *b = [a copy];
  NSLog(@"a retainCount = %ld",[a retainCount]);

  NSString *c = [a mutableCopy];

  NSLog(@"%@,%@,%@",a,b,c);
  NSLog(@"%p,%p,%p",a,b,c);
```

结果

```objc
2019-09-12 13:54:58.109757+0800 Copy MutableCopy[13700:49429440] a retainCount = -1
2019-09-12 13:54:58.109876+0800 Copy MutableCopy[13700:49429440] a retainCount = -1
2019-09-12 13:54:58.109989+0800 Copy MutableCopy[13700:49429440] abc,abc,abc
2019-09-12 13:54:58.110062+0800 Copy MutableCopy[13700:49429440] 0xd5e0520931336344,0xd5e0520931336344,0x6000038d3330
```

由[Tagged Pointed](/02_Tagged Pointer.md) 可以知道a b 为Tagged Pointer 对象  想深入了解的的可以看一下。



#### 总结

|             | NSString | NSMutableString | NSArray | NSMutableArray | NSDictionary | NSMutableDictionary |
| ----------- | -------- | --------------- | ------- | -------------- | ------------ | ------------------- |
| copy        | 浅拷贝   | 深拷贝          | 浅拷贝  | 深拷贝         | 浅拷贝       | 深拷贝              |
| mutableCopy | 深拷贝   | 深拷贝          | 深拷贝  | 深拷贝         | 深拷贝       | 深拷贝              |

