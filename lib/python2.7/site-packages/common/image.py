import time
from random import randint
from hashlib import sha1
from tempfile import NamedTemporaryFile
import os
import Image
import ImageDraw

from django.core.files import File

def random_color():
    return 'rgb(%d, %d, %d)' % (randint(0, 255), randint(0, 255), randint(0, 255))


def generate_image(size, bgcolor='#ffffff'):
    img = Image.new('RGBA', size=size)
    draw = ImageDraw.Draw(img)
    draw.rectangle(((0, 0), size), fill=bgcolor)
    for x in xrange(30):
        diameter = int(min(*size) / float(randint(4, 8)))
        topleft = (0 + randint(0, size[0]),
                   0 + randint(0, size[1]))
        bottomright = (topleft[0] + diameter,
                       topleft[1] + diameter)
        draw.pieslice((topleft + bottomright), 0, 360, fill=random_color())
    return img


def random_image(size=(200, 200), bgcolor='#ffffff'):
    source = '%d%d' % (time.time(), id({}))
    hashname = sha1(source).hexdigest() + '.jpg'
    tmpfile = NamedTemporaryFile()
    img = generate_image(size, bgcolor)
    img.save(tmpfile, 'JPEG')
    tmpfile.seek(0)
    return File(tmpfile, name=hashname)
