//
//  ViewController.m
//  调用栈测试
//
//  Created by iOS on 2020/5/9.
//  Copyright © 2020 iOS. All rights reserved.
//

#import "ViewController.h"
#import "BSBacktraceLogger.h"
#import "MonitorTimer.h"
@interface ViewController ()
@property(nonatomic, assign,setter=abc:, getter=bbb) int a;
@end

@implementation ViewController


- (void)viewDidLoad {
    [super viewDidLoad];
//    [MonitorTimer.shared beginMontior];
    
    _Block_copy
    self.a = 10;
    
}
+ (BOOL)accessInstanceVariablesDirectly {
    return false;
}

- (void)setA:(int)a {
    _a = a;
}

- (void)abc:(int)a {
    _a = a;
}
- (void)touchesBegan:(NSSet<UITouch *> *)touches withEvent:(UIEvent *)event {
//    NSLog(@"开始");
//    for (int i = 0; i < 200000000; i++) {
//        NSString *a = @"123";
//    }
//    NSLog(@"结束");
     [self setValue:@2 forKey:@"a"];
}
- (void)foo {
    [self bar];
}

- (void)bar {
    while (true) {
        ;
    }
}


@end
