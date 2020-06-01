from collections import namedtuple


def animate(Parent, decorated_ttl=None):

    TTL_DEFAULT = 0

    def wrapper(animation):

        class Wrapped(Parent):
            def __init__(self, *args, ttl=decorated_ttl, **argv):
                super().__init__(*args, **argv)
                self.__ttl = ttl if ttl is not None else TTL_DEFAULT
                self.__original__ttl = self.__ttl

            def update(self, elapsed):
                self.__ttl -= elapsed
                if self.animated:
                    animation(self, elapsed, self.__ttl, self.__original__ttl)
                return self.animated

            @property
            def animated(self):
                return self.__ttl >= 0

        Wrapped.__name__ = f'Animated{Parent.__name__}'
        return Wrapped

    return wrapper
