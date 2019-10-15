## initialize

### 1.initialize 原理

1. objc-class.mm

2. `class_getClassMethod`  内部直接调用  `class_getInstanceMethod`

   ```objc
   Method class_getInstanceMethod(Class cls, SEL sel)
   {
       if (!cls  ||  !sel) return nil;
   
       // This deliberately avoids +initialize because it historically did so.
   
       // This implementation is a bit weird because it's the only place that 
       // wants a Method instead of an IMP.
   
   #warning fixme build and search caches
           
       // Search method lists, try method resolver, etc.
     	// 3. 查找是否为检查imp
       lookUpImpOrNil(cls, sel, nil, 
                      NO/*initialize*/, NO/*cache*/, YES/*resolver*/);
   
   #warning fixme build and search caches
   
       return _class_getMethod(cls, sel);
   }
   ```

   

3. `lookUpImpOrNil`

   ```objc
   IMP lookUpImpOrNil(Class cls, SEL sel, id inst, 
                      bool initialize, bool cache, bool resolver)
   {
   	  // 检查
       IMP imp = lookUpImpOrForward(cls, sel, inst, initialize, cache, resolver);
       if (imp == _objc_msgForward_impcache) return nil;
       else return imp;
   }
   ```

   

4. `lookUpImpOrForward` 检查

   ```objc
   IMP lookUpImpOrForward(Class cls, SEL sel, id inst, 
                          bool initialize, bool cache, bool resolver)
   {
     	// 简化代码
   		// 如果需要初始化 并且 对象没有被初始化
       if (initialize  &&  !cls->isInitialized()) {
           runtimeLock.unlock();
         // 5.初始化
           _class_initialize (_class_getNonMetaClass(cls, inst));
           runtimeLock.lock();
           // If sel == initialize, _class_initialize will send +initialize and 
           // then the messenger will send +initialize again after this 
           // procedure finishes. Of course, if this is not being called 
           // from the messenger then it won't happen. 2778172
       }
       return imp;
   }
   ```

   

5. `void _class_initialize(Class cls)`

   ```objc
   void _class_initialize(Class cls)
   {
       assert(!cls->isMetaClass());
   
       Class supercls;
       bool reallyInitialize = NO;
   
       // Make sure super is done initializing BEFORE beginning to initialize cls.
       // See note about deadlock above.
       supercls = cls->superclass;
   	  // 递归父类
       if (supercls  &&  !supercls->isInitialized()) {
           _class_initialize(supercls);
       }
       
       // Try to atomically set CLS_INITIALIZING.
       {
           monitor_locker_t lock(classInitLock);
           if (!cls->isInitialized() && !cls->isInitializing()) {
             // 设置已经初始化
               cls->setInitializing();
               reallyInitialize = YES;
           }
       }
       
       if (reallyInitialize) {
           // We successfully set the CLS_INITIALIZING bit. Initialize the class.
           
           // Record that we're initializing this class so we can message it.
           _setThisThreadIsInitializingClass(cls);
   
           if (MultithreadedForkChild) {
               // LOL JK we don't really call +initialize methods after fork().
               performForkChildInitialize(cls, supercls);
               return;
           }
           
           // Send the +initialize message.
           // Note that +initialize is sent to the superclass (again) if 
           // this class doesn't implement +initialize. 2157218
           if (PrintInitializing) {
               _objc_inform("INITIALIZE: thread %p: calling +[%s initialize]",
                            pthread_self(), cls->nameForLogging());
           }
   
           // Exceptions: A +initialize call that throws an exception 
           // is deemed to be a complete and successful +initialize.
           //
           // Only __OBJC2__ adds these handlers. !__OBJC2__ has a
           // bootstrapping problem of this versus CF's call to
           // objc_exception_set_functions().
   #if __OBJC2__
           @try
   #endif
           {
             /// 6. 调用方法
               callInitialize(cls);
   
               if (PrintInitializing) {
                   _objc_inform("INITIALIZE: thread %p: finished +[%s initialize]",
                                pthread_self(), cls->nameForLogging());
               }
           }
   #if __OBJC2__
           @catch (...) {
               if (PrintInitializing) {
                   _objc_inform("INITIALIZE: thread %p: +[%s initialize] "
                                "threw an exception",
                                pthread_self(), cls->nameForLogging());
               }
               @throw;
           }
           @finally
   #endif
           {
               // Done initializing.
               lockAndFinishInitializing(cls, supercls);
           }
           return;
       }
       
       else if (cls->isInitializing()) {
           // We couldn't set INITIALIZING because INITIALIZING was already set.
           // If this thread set it earlier, continue normally.
           // If some other thread set it, block until initialize is done.
           // It's ok if INITIALIZING changes to INITIALIZED while we're here, 
           //   because we safely check for INITIALIZED inside the lock 
           //   before blocking.
           if (_thisThreadIsInitializingClass(cls)) {
               return;
           } else if (!MultithreadedForkChild) {
               waitForInitializeToComplete(cls);
               return;
           } else {
               // We're on the child side of fork(), facing a class that
               // was initializing by some other thread when fork() was called.
               _setThisThreadIsInitializingClass(cls);
               performForkChildInitialize(cls, supercls);
           }
       }
       
       else if (cls->isInitialized()) {
           // Set CLS_INITIALIZING failed because someone else already 
           //   initialized the class. Continue normally.
           // NOTE this check must come AFTER the ISINITIALIZING case.
           // Otherwise: Another thread is initializing this class. ISINITIALIZED 
           //   is false. Skip this clause. Then the other thread finishes 
           //   initialization and sets INITIALIZING=no and INITIALIZED=yes. 
           //   Skip the ISINITIALIZING clause. Die horribly.
           return;
       }
       
       else {
           // We shouldn't be here. 
           _objc_fatal("thread-safe class init in objc runtime is buggy!");
       }
   }
   ```

   

6. `void callInitialize(Class cls)`

   ```objc
   void callInitialize(Class cls)
   {
   	  // msgSend  走msgSend逻辑
       ((void(*)(Class, SEL))objc_msgSend)(cls, SEL_initialize); 
       asm("");
   }
   ```

### 2.initialize总结

上面为查找方法入口的逻辑,最终要的是第4步的检查，递归父类，调用方法方式。 

递归决定了 调用子类的时候会先调用父类

调用方式（`msgSend`） 决定了当子类没有实现`initialize`的时候 会调用父类的`initialize` 会造成父类`initialize`多次调用，但是父类并没有多次初始化， 每个类只初始化一次 ，是因为msgSend在当前类招不到方法时，调用父类方法，仅此而已。

