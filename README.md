# S3-Content_Type-Autotag
自动检测和标记AWS S3文件对象内容类型


### 1. 背景
客户有一个应用需要上传用户图片，出于资源保护和安全需要,代码中没有对图片进行格式化。上传的图片只有一个随机生成的文件名，没有扩展名，所以上传到S3或Cloudfront，S3/Cloudfront无法通过对象的MIME和Content-Type字段判断文件类型，导致当基于 Http的访问请求发出时，图片被视为用于下载的二进制未知文件。
目前类似七牛CDN提供了智能判断内容类型的功能。对于上传的文件，它会自动判断并标记content-type，避免在访问过程中直接下载。
### 2. 解决方案
经过调查S3文档，S3本身并没有提供检测Content-Type的功能。对象的Content-Type主要依赖于Metadata中的MIME判断。如果文件没有配置扩展名，默认情况下该文件将被标记为 binary/*。为此，您需要使用对象处理方法来自定义上传对象的内容类型。

**部署**
使用 Python-magic 包来识别文件对象的 Content-Type。 python-magic 是 libmagic 文件类型识别库的 Python 接口。 libmagic 通过对照预定义的文件类型列表检查文件头来识别文件类型 https://pypi.org/project/python-magic/

- **实现逻辑**
1. 创建一个 Lambda 来监控 S3 文件的上传行为
2. 对象上传行为触发python-magic库检查对象类型
3. 将magic lib判断的文件类型（Content-Type）并写入对象的Metadata