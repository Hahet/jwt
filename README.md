JWT(json web tokens) 跨域身份验证解决方案

JWT是一种token存储的格式
分为三部分组成
结构如下
Header.Payload.Signature
Header和Payload都是json格式数据的base64url编码的数据(由于JWT数据可能会在url中)。

JWT一般做三件事情

1. encode 编码
这部分用于用户发送请求到服务器，服务器把要存储在客户端的数据编码，并进行签名后发送到客户端存储。

    Key = b'my-secret' # 存储在服务器
    Header = {
            "typ": "JWT",
            "alg": "HS256"
        }
    Payload = {
            "sub": "1234567890",
            "name": "John Doe",
            "iat": 1516239022
    }
    base64url_encode(Header) + b'.' + base64url_encode(Payload)
    把Header和Payload序列化成json字符串(注意不同的序列化的空格会有差异)，
    然后进行base64url然后用“.”连接，称为JWT的前两部分
    第三部分是由Hmac算法进行签名
    digest = hmac.new(key, Header.Payload, digestmod=hashlib.sha256).digest()
    sign = base64url_encode(digest())
    至此得到三部分然后以'.'进行连接即可得到JWT token

eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.j7vwW1sfcOmnR4tTCVMZfJCFVjwnQh0ajARTY2Q9nMw


2. validate

这部分用于验证数据是否被修改，例如客户端发送数据到服务器，服务
器首先对数据进行验证是否被修改，如果被修改则抛弃。
signature(Header.Payload) == Signature

3. decode
    Key = b'my-secret' # 存储在服务器
    header = base64url_encode(Header)
    payload = base64url_encode(Payload)

数据通过验证之后就可以对header和payload两部分进行解码，解码后的数据可以用来鉴定用户。



参考页面
https://jwt.io/