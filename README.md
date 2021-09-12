# S3-Content_Type-Autotag
Automatically detect and tag AWS S3 object content type


### 1. Background
There is currently an application that needs to upload user pictures, but for resource protection, the picture is not formatted in the code. The uploaded picture has only a randomly generated file name and no extension, so upload it to S3 or Cloudfront, S3/ Cloudfront cannot determine the file type through the MIME and Content-Type fields of the object, which causes the image to be regarded as a binary unknown file for downloading when the Http-based access request is made.
At present, a similar Qiniu CDN provides the function of intelligently judging the content-type. For uploaded files, it will automatically determine and mark the content-type to avoid downloading during access.I hope that AWS S3 will also provide similar functions.

### 2. Solution
After investigating the S3 document, S3 itself does not provide the function of detecting Content-Type. The Content-Type of the object mainly relies on the MIME judgment in Metadata. If the file is not configured with an extension, the file will be marked as binary/* by default. For this, you need to use the object processing method to customize the content-type of the uploaded object.

**Implement**
Use the Python-magic package to identify the Content-Type of the file object. python-magic is the Python interface of the libmagic file type recognition library. libmagic recognizes the file type by checking the file header against a predefined list of file types. For specific introduction, please refer to https://pypi.org/project/python-magic/

- **Implementation logic**
1. Create a Lambda to monitor the upload behavior of S3 files
2. The object upload behavior triggers the python-magic library to check the object type
3. Write the file type (Content-Type) judged by magic to the uploaded object