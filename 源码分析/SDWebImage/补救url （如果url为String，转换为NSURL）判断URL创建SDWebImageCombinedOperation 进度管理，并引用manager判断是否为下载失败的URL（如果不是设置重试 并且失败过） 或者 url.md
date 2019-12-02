1. 补救url （如果url为String，转换为NSURL）
2. 判断URL
3. 创建SDWebImageCombinedOperation 进度管理，并引用manager
4. 判断是否为下载失败的URL
5. （如果不是设置重试 并且失败过） 或者 url.length == 0  返回失败
6. 添加operation到runningOperations





requestImageWithURL

SD_LOCK 用的是信号量

