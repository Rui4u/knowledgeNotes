AutoreleasePoolPage的结构



每个AutoreleasePoolPage对象占用4096字节的内存，除了用来存放内部成员变量,剩下的空间来存放autorealse对象的地址

  所有的AutoreleasePoolPage是通过双向链表的形式链接在一起





Autoreleasepool  查看源码



RunLoop