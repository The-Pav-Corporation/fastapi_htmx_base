from functools import wraps
import logging

_logger = logging.getLogger("uvicorn.error")

def ensure_printable(func):

    @wraps(func)
    def inner(*args, **kwargs):
        new_args = []
        if args:
            for arg in args:
                if isinstance(arg, str) and "\x00" in arg:
                    new_args.append(arg.replace("\x00", ""))
                    _logger.debug(f"found dirty input: {arg}")
                else:
                    new_args.append(arg)
        if kwargs:
            for k, v in kwargs.items():
                kwargs[k] = v.replace("\x00", "") if isinstance(kwargs[k], str) else v
        return func(*new_args, **kwargs)
    
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

    testfunc(4, "the_title\x00hhh", "thedescription1", external_url="url\x00m8", source="sauce")
