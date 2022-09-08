from functools import wraps

def ensure_printable(func):

    @wraps(func)
    def inner(*args, **kwargs):
        args = [arg.replace("\x00", "") for arg in args]  or []
        if kwargs:
            for k, v in kwargs.items():
                kwargs[k] = v.replace("\x00", "")
        else:
            kwargs = {}
        func(*args, **kwargs)
    
    return inner

if __name__ == "__main__":
    @ensure_printable
    def testfunc(db, title, description, external_url, source):
        """
        testfunc doc
        """
        print(
            db, title, description, external_url, source
        )

    testfunc("the_db", "the_title\x00hhh", "thedescription1", external_url="url\x00m8", source="sauce")
