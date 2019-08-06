import jwt2
import jwt


def ensure_equal(a, b, log):
    if a != b:
        print('expect:', a)
        print('result:', b)
        print('log', log)
        assert False


def test1():
    key = b'my-secret'
    # 默认使用此header
    # 默认使用sha256算法
    header = {
        "typ": "JWT",
        "alg": "HS256"
    }
    payload = {
        "sub": "1234567890",
        "name": "John Doe",
        "iat": 1516239022
    }
    j2 = jwt2.JWT(key)
    r = j2.encode(header, payload)
    e = jwt.encode(payload, headers=header, key=key)
    log = 'log\nr {}\n e{}'.format(r, e)
    ensure_equal(r, e, log)


def test2():
    header_payload = b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ'
    signature = b'j7vwW1sfcOmnR4tTCVMZfJCFVjwnQh0ajARTY2Q9nMw'
    key = b'my-secret'
    jw = jwt2.JWT(key)
    v = jw.validate(header_payload, signature)
    assert v, v


def test3():
    jwt_str = b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.j7vwW1sfcOmnR4tTCVMZfJCFVjwnQh0ajARTY2Q9nMw'
    key = b'my-secret'
    jw = jwt2.JWT(key)
    v, data = jw.decode(jwt_str)
    assert v, data


def test4():
    jwt_str = b'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.j7vwW1sfcOmnR4tTCVMZfJCFVjwnQh0ajARTY2Q9nM'
    key = b'my-secret'
    jw = jwt2.JWT(key)
    v, data = jw.decode(jwt_str)
    assert not v, data
