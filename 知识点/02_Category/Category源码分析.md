  指定真机

```
xcrun -sdk iphoneos clang -rewrite-objc objcet.m
```

指定模拟器

```
xcrun -sdk iphonesimulator clang -rewrite-objc objcet.m
```

指定SDK版本

```
xcrun -sdk iphonesimulator10.3 clang -rewrite-objc  objcet.m
```

如果出现下面错误  要指定sdk

```
main.m:9:9: fatal error: 'Foundation/Foundation.h' file not found
#import <Foundation/Foundation.h>
```

```objc
clang -x objective-c -rewrite-objc -isysroot /Applications/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator.sdk main.m 
```

clanng. oc转为c++代码时 `__weak` 遇到的问题 可以通过以下方式解决

`xcrun -sdk iphoneos clang -arch arm64 -rewrite-objc -fobjc-arc -fobjc-rumtime=ios-10.0.0 main.m`

Category 编译时会生成以下类型结构体

```objc
struct _category_t {
	const char *name;
	struct _class_t *cls;
	const struct _method_list_t *instance_methods;
	const struct _method_list_t *class_methods;
	const struct _protocol_list_t *protocols;
	const struct _prop_list_t *properties;
};
```



通过一下结构体赋值

```objc
static struct _category_t _OBJC_$_CATEGORY_People_$_SRExtension __attribute__ ((used, section ("__DATA,__objc_const"))) = 
{
	"People",
	0, // &OBJC_CLASS_$_People,
	(const struct _method_list_t *)&_OBJC_$_CATEGORY_INSTANCE_METHODS_People_$_SRExtension,
	0,
	(const struct _protocol_list_t *)&_OBJC_CATEGORY_PROTOCOLS_$_People_$_SRExtension,
	0,
};
```



我们对对应两个结构体的参数

* "People" 对应  const char *name;
* 第二个默认参数为0
* 第三个 对象方法
* 第四个 因为没有添加类方法，所以为0
* 第五个 协议列表
* 第六个 没有添加属性 所以为0



目前我们添加了两个对象方法  在编译的源码中 找到以下结构体  _method_list_t

```objc
static struct /*_method_list_t*/ {
	unsigned int entsize;  // sizeof(struct _objc_method)
	unsigned int method_count;
	struct _objc_method method_list[2];
} _OBJC_$_CATEGORY_INSTANCE_METHODS_People_$_SRExtension __attribute__ ((used, section                                                                       ("__DATA,__objc_const"))) = {
	sizeof(_objc_method),
	2,
	{{(struct objc_selector *)"food", "v16@0:8", (void *)_I_People_SRExtension_food},
	{(struct objc_selector *)"eat", "v16@0:8", (void *)_I_People_SRExtension_eat}}
};
```



从上面的源码我们一一对应赋值 

*  大小
*  个数
* 方法列表

可以看出，在编译的时候这些结构体就已经赋值。但是并没有合并到主类中



>  我们知道 类的属性，对象方法，协议，成员变量信息都存在class 中

>  类的类方法 存在类的meta-class 中

何时将到分类的信息添加到类中呢  有兴趣的同学可以一下顺序 看一下obj4的源码

`objc-os.mm`

_objc_init～map_images（镜像）_

_ map_images_nolock

`objc-runtime-new.mm`

_read_images 

remethodizeClass(重新方法化)

attachCategories(方法附加)

attachLists



Lsit 操作中有下面两个参数

realloc、memmove、 memcpy

> memcpy是从内存左侧一个字节一个字节的复制拷贝
>
> memmove是将需要拷贝的内容一次性移动拷贝。



我们看一下重要的代码

```objc
static void 
attachCategories(Class cls, category_list *cats, bool flush_caches)
{
    if (!cats) return;
    if (PrintReplacedMethods) printReplacements(cls, cats);

    bool isMeta = cls->isMetaClass();

    // fixme rearrange to remove these intermediate allocations
    method_list_t **mlists = (method_list_t **)
        malloc(cats->count * sizeof(*mlists));
    property_list_t **proplists = (property_list_t **)
        malloc(cats->count * sizeof(*proplists));
    protocol_list_t **protolists = (protocol_list_t **)
        malloc(cats->count * sizeof(*protolists));

    // Count backwards through cats to get newest categories first
    int mcount = 0;
    int propcount = 0;
    int protocount = 0;
    int i = cats->count;
    bool fromBundle = NO;
    while (i--) {
        auto& entry = cats->list[i];

        method_list_t *mlist = entry.cat->methodsForMeta(isMeta);
        if (mlist) {
            mlists[mcount++] = mlist;
            fromBundle |= entry.hi->isBundle();
        }

        property_list_t *proplist = 
            entry.cat->propertiesForMeta(isMeta, entry.hi);
        if (proplist) {
            proplists[propcount++] = proplist;
        }

        protocol_list_t *protolist = entry.cat->protocols;
        if (protolist) {
            protolists[protocount++] = protolist;
        }
    }

    auto rw = cls->data();

    prepareMethodLists(cls, mlists, mcount, NO, fromBundle);
    rw->methods.attachLists(mlists, mcount);
    free(mlists);
    if (flush_caches  &&  mcount > 0) flushCaches(cls);

    rw->properties.attachLists(proplists, propcount);
    free(proplists);

    rw->protocols.attachLists(protolists, protocount);
    free(protolists);
}
```

我们重点看一下这个代码

```objc
property_list_t **proplists = (property_list_t **)
        malloc(cats->count * sizeof(*proplists));
int i = cats->count;
    while (i--) {
        auto& entry = cats->list[i];

        method_list_t *mlist = entry.cat->methodsForMeta(isMeta);
        if (mlist) {
            mlists[mcount++] = mlist;
            fromBundle |= entry.hi->isBundle();
        }

        property_list_t *proplist = 
            entry.cat->propertiesForMeta(isMeta, entry.hi);
        if (proplist) {
            proplists[propcount++] = proplist;
        }

        protocol_list_t *protolist = entry.cat->protocols;
        if (protolist) {
            protolists[protocount++] = protolist;
        }
    }
```

注意下i的赋值  以及i--

将所有该类的分类进行组装， 按照装载顺序的逆序 开始组装

```objc
void attachLists(List* const * addedLists, uint32_t addedCount) {
        if (addedCount == 0) return;

        if (hasArray()) {
            // many lists -> many lists
            uint32_t oldCount = array()->count;
            uint32_t newCount = oldCount + addedCount;
            setArray((array_t *)realloc(array(), array_t::byteSize(newCount)));
            array()->count = newCount;
            memmove(array()->lists + addedCount, array()->lists, 
                    oldCount * sizeof(array()->lists[0]));
            memcpy(array()->lists, addedLists, 
                   addedCount * sizeof(array()->lists[0]));
        }
        else if (!list  &&  addedCount == 1) {
            // 0 lists -> 1 list
            list = addedLists[0];
        } 
        else {
            // 1 list -> many lists
            List* oldList = list;
            uint32_t oldCount = oldList ? 1 : 0;
            uint32_t newCount = oldCount + addedCount;
            setArray((array_t *)malloc(array_t::byteSize(newCount)));
            array()->count = newCount;
            if (oldList) array()->lists[addedCount] = oldList;
            memcpy(array()->lists, addedLists, 
                   addedCount * sizeof(array()->lists[0]));
        }
    }
```

``memmove` 将类中的原方法放置到列表尾部

`memcpy` ： 将 `addedLists` 中的所有 `Category` 的方法列表放置到原有方法前



所以。当我们从分类中 重写父类方法的时候。会调用分类中的方法。 这个不是覆盖原方法，而是分类方法在原方法的前面被查询到。从而调用分类方法。 不推荐此方法覆盖分类方法。



