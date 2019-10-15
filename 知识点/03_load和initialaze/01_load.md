## load

### 1. load 方法调用以及说明

1. `_objc_init`  ` _dyld_objc_notify_register(&map_images,load_images, unmap_image);` 
2. `load_images`   load 镜像
   1. `prepare_load_methods((const headerType *)mh);`  加载前准备
      1. `static void schedule_class_load(Class cls)` 装载原类load 进行准备
         1. `add_class_to_loadable_list` 将load方法添加到loadable_classes中 
      2. `add_category_to_loadable_list`   将分类load方法添加到loadable_categories中
   2. `call_load_methods();`
      1.  `call_class_loads`  遍历loadable_classes 直接获取函数指针调用load
      2. ` call_category_loads(void)` 遍历loadable_categories 直接获取函数指针调用load



### 2. load原理

1. `_objc_init `  $\rightarrow$ ` _dyld_objc_notify_register(&map_images,load_images, unmap_image);`  找到`load_images`方法
2. `load_images` 

```objc
load_images(const char *path __unused, const struct mach_header *mh)
{
    // Return without taking locks if there are no +load methods here.
    if (!hasLoadMethods((const headerType *)mh)) return;

    recursive_mutex_locker_t lock(loadMethodLock);

    // Discover load methods
    {
        mutex_locker_t lock2(runtimeLock);
	      //2.1
        prepare_load_methods((const headerType *)mh);
    }

    // Call +load methods (without runtimeLock - re-entrant)
  	// 2.2
    call_load_methods();
}
```

2.1	prepare_load_methods `   <!--// load前准备 -->

```objc
void prepare_load_methods(const headerType *mhdr)
{
    size_t count, i;

    runtimeLock.assertLocked();
		//装载类列表
    classref_t *classlist = 
        _getObjc2NonlazyClassList(mhdr, &count);
    for (i = 0; i < count; i++) {
       //2.1.1
        schedule_class_load(remapClass(classlist[i]));
    }
		//获取分类列表
    category_t **categorylist = _getObjc2NonlazyCategoryList(mhdr, &count);
	  // 按照装载顺序添加到列表中
    for (i = 0; i < count; i++) {
        category_t *cat = categorylist[i];
        Class cls = remapClass(cat->cls);
        if (!cls) continue;  // category for ignored weak-linked class
        realizeClass(cls);
        assert(cls->ISA()->isRealized());
	     // 2.1.2 
        add_category_to_loadable_list(cat);
    }
}
```

2.1.1	定制load

```objc
static void schedule_class_load(Class cls)
{
    if (!cls) return;
    assert(cls->isRealized());  // _read_images should realize

    if (cls->data()->flags & RW_LOADED) return;

    // Ensure superclass-first ordering
    // 递归找到父类load
    schedule_class_load(cls->superclass);
		// 添加到列表中 根据递归可以看出 先添加父类 后添加子类
  	// 2.1.1.1
    add_class_to_loadable_list(cls);
    cls->setInfo(RW_LOADED); 
}
```

2.1.1.1	将找到的类 添加到列表中

```objc
void add_class_to_loadable_list(Class cls)
{
    IMP method;

    loadMethodLock.assertLocked();

    method = cls->getLoadMethod();
    if (!method) return;  // Don't bother if cls has no +load method
    
    if (PrintLoading) {
        _objc_inform("LOAD: class '%s' scheduled for +load", 
                     cls->nameForLogging());
    }
    
    if (loadable_classes_used == loadable_classes_allocated) {
        loadable_classes_allocated = loadable_classes_allocated*2 + 16;
        loadable_classes = (struct loadable_class *)
            realloc(loadable_classes,
                              loadable_classes_allocated *
                              sizeof(struct loadable_class));
    }
    // 顺序添加 尾插
    loadable_classes[loadable_classes_used].cls = cls;
    loadable_classes[loadable_classes_used].method = method;
    loadable_classes_used++;
}
```

2.1.2	添加到分类load列表中

```objc
void add_category_to_loadable_list(Category cat)
{
    IMP method;

    loadMethodLock.assertLocked();

    method = _category_getLoadMethod(cat);

    // Don't bother if cat has no +load method
    if (!method) return;

    if (PrintLoading) {
        _objc_inform("LOAD: category '%s(%s)' scheduled for +load", 
                     _category_getClassName(cat), _category_getName(cat));
    }
    
    if (loadable_categories_used == loadable_categories_allocated) {
        loadable_categories_allocated = loadable_categories_allocated*2 + 16;
        loadable_categories = (struct loadable_category *)
            realloc(loadable_categories,
                              loadable_categories_allocated *
                              sizeof(struct loadable_category));
    }
		// 顺序添加 尾插
    loadable_categories[loadable_categories_used].cat = cat;
    loadable_categories[loadable_categories_used].method = method;
    loadable_categories_used++;
}
```

2.2	 `call_load_methods` 调用load方法

```objc
void call_load_methods(void)
{
    static bool loading = NO;
    bool more_categories;

    loadMethodLock.assertLocked();

    // Re-entrant calls do nothing; the outermost call will finish the job.
    if (loading) return;
    loading = YES;

    void *pool = objc_autoreleasePoolPush();

    do {
        // 1. Repeatedly call class +loads until there aren't any more
        while (loadable_classes_used > 0) {
	          // 2.2.1 调用原类的load
            call_class_loads();
        }

        // 2. Call category +loads ONCE
      	// 2.2.2 调用分类 +load
        more_categories = call_category_loads();

        // 3. Run more +loads if there are classes OR more untried categories
    } while (loadable_classes_used > 0  ||  more_categories);

    objc_autoreleasePoolPop(pool);

    loading = NO;
}
```

2.2.1 `call_class_loads` 调用原类的load     

```objc
static void call_class_loads(void)
{
    int i;
    
    // Detach current loadable list.
  // 在2.1.1.1 中准备好的load_classes 列表
    struct loadable_class *classes = loadable_classes;
    int used = loadable_classes_used;
    loadable_classes = nil;
    loadable_classes_allocated = 0;
    loadable_classes_used = 0;
    
    // Call all +loads for the detached list.
  	/// 遍历列表
    for (i = 0; i < used; i++) {
        Class cls = classes[i].cls;
	      // 拿到类的函数指针  参考下方标注：load_method_t、loadable_class
        load_method_t load_method = (load_method_t)classes[i].method;
        if (!cls) continue; 

        if (PrintLoading) {
            _objc_inform("LOAD: +[%s load]\n", cls->nameForLogging());
        }
      	// 直接调用load函数
        (*load_method)(cls, SEL_load);
    }
    
    // Destroy the detached list.
    if (classes) free(classes);
}
```

​       标注：

```c
struct loadable_class {
    Class cls;  // may be nil
  	// 实际为load方法
    IMP method;
};	
```

```c
typedef void(*load_method_t)(id, SEL); //方法函数指针
```

2.2.2 调用分类 +load

```objc
static bool call_category_loads(void)
{
    int i, shift;
    bool new_categories_added = NO;
    
    // Detach current loadable list.
		//  2.1.2	准备好装载分类方法列表
    struct loadable_category *cats = loadable_categories;
    int used = loadable_categories_used;
    int allocated = loadable_categories_allocated;
    loadable_categories = nil;
    loadable_categories_allocated = 0;
    loadable_categories_used = 0;

    // Call all +loads for the detached list.
	  //遍历
    for (i = 0; i < used; i++) {
        Category cat = cats[i].cat;
    	  // 获取函数指针
        load_method_t load_method = (load_method_t)cats[i].method;
        Class cls;
        if (!cat) continue;

        cls = _category_getClass(cat);
        if (cls  &&  cls->isLoadable()) {
            if (PrintLoading) {
                _objc_inform("LOAD: +[%s(%s) load]\n", 
                             cls->nameForLogging(), 
                             _category_getName(cat));
            }
	          // 调用分类load函数
            (*load_method)(cls, SEL_load);
            cats[i].cat = nil;
        }
    }

    // Compact detached list (order-preserving)
    shift = 0;
    for (i = 0; i < used; i++) {
        if (cats[i].cat) {
            cats[i-shift] = cats[i];
        } else {
            shift++;
        }
    }
    used -= shift;

    // Copy any new +load candidates from the new list to the detached list.
    new_categories_added = (loadable_categories_used > 0);
    for (i = 0; i < loadable_categories_used; i++) {
        if (used == allocated) {
            allocated = allocated*2 + 16;
            cats = (struct loadable_category *)
                realloc(cats, allocated *
                                  sizeof(struct loadable_category));
        }
        cats[used++] = loadable_categories[i];
    }

    // Destroy the new list.
    if (loadable_categories) free(loadable_categories);

    // Reattach the (now augmented) detached list. 
    // But if there's nothing left to load, destroy the list.
    if (used) {
        loadable_categories = cats;
        loadable_categories_used = used;
        loadable_categories_allocated = allocated;
    } else {
        if (cats) free(cats);
        loadable_categories = nil;
        loadable_categories_used = 0;
        loadable_categories_allocated = 0;
    }

    if (PrintLoading) {
        if (loadable_categories_used != 0) {
            _objc_inform("LOAD: %d categories still waiting for +load\n",
                         loadable_categories_used);
        }
    }

    return new_categories_added;
}
```

### 3. load 总结

1. 通过源码分析,我们可以知道系统在初始化的时候,会先生成一个原类load方法数组和分类load方法数组。
2. 装载load方法列表：通过递归 先装载父类，后装载子类。
3. 装载分类方法列表：通过编译顺序装载。
4. 在调用时优先调用原类load方法列表，并且通过获取函数指针进行直接函数调用。
5. 在调用时后调用分类load方法列表，并且通过获取函数指针进行直接函数调用。





