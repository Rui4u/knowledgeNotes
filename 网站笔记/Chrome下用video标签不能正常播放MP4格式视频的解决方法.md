# Chrome下用video标签不能正常播放MP4格式视频的解决方法



```html
<video
  src="https://sharui-oss.oss-cn-beijing.aliyuncs.com/Atlantis%201080p%20with%20ENG%20Ending.mp4"
  controls="controls"
  frameborder="0"
  type="video/mp4"
  allow="autoplay;encrypted-media"
  style="height:200px"
>
  您的浏览器不支持 video 标签。
</video>
```

Safari 可以播放 chrome 只有声音

### 问题出在哪

video只能播放H264的编码格式MP4 

### 解决方法

转码

#### 安装并 ffmpeg

```shell
brew install ffmpeg
```

```shell
ffmpeg -i 本地.mp4 -vcodec h264 输出.mp4
```



