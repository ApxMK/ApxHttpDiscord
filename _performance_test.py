import msgspec

class InnerTest(msgspec.Struct):
    second_name : str | None = None

class Test(msgspec.Struct):
    class TestUrls():
        CREATE_WEBHOOK = "/channels/webhooks"

    name : InnerTest | None = None
    age : int | None = None

i=Test(name=InnerTest(second_name="Lee"), age=9)
print(i.TestUrls.CREATE_WEBHOOK)

# TestString = "This is my test string: {name.second_name}"
# print(TestString.format(nam=i.name, name=9))

tup1 = (1,2,3)
tup2 = ("Michael", "Lee", "Glasgow")
seq12 = zip(tup1, tup2)

def test_func(*args, **kwargs):
    print(args, kwargs)

test_func(dict1 = "HELLO")