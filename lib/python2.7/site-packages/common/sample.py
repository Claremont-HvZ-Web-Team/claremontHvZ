import string
from random import choice, randint
import itertools

LOREM = "Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat. Duis autem vel eum iriure dolor in hendrerit in vulputate velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait nulla facilisi."""
LOREM_ITER = itertools.cycle(LOREM.split(' '))


def random_ip():
    "Generate random ip address."

    x = lambda: randint(1, 255)
    return '%d.%d.%d.%d' % (x(), x(), x(), x())


def random_string(minlen=5, maxlen=8):
    """
    Generate random string of length between ``minlen`` and ``maxlen``.
    """

    length = randint(minlen, maxlen)
    return ''.join(choice(string.lowercase) for x in xrange(length))


def random_text(count):
    """
    Generate random text of ``count`` length.
    """

    text = ' '.join(LOREM_ITER.next() for x in xrange(count))
    return text[0].upper() + text[1:]


def random_html(count):
    """
    Generate random HTML of ``count`` tokens length.
    """

    def tag(word):
        var = randint(0, 20)
        if var == 0:
            return '<b>%s</b>' % word
        elif var == 1:
            return '<i>%s</i>' % word
        elif var == 2:
            return '<a href="http://yandex.ru">%s</a>' % word
        else:
            return word
    text = ' '.join(tag(LOREM_ITER.next()) for x in xrange(count))
    return text[0].upper() + text[1:]


def random_phone():
    def number(size):
        return ''.join(choice(string.digits) for x in xrange(size))
    return '+%s %s %s' % (number(1), number(3), number(7))
