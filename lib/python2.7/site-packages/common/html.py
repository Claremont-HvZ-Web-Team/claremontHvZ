from BeautifulSoup import BeautifulSoup

from django.template.defaultfilters import urlize as django_urlize

def urlize(data):
    """
    Urlize plain text links in the HTML contents.

    Do not urlize content of A and CODE tags.
    """

    soup = BeautifulSoup(data)
    for chunk in soup.findAll(text=True):
        islink = False
        ptr = chunk.parent
        while ptr.parent:
            if ptr.name == 'a' or ptr.name == 'code':
                islink = True
                break
            ptr = ptr.parent

        if not islink:
            chunk = chunk.replaceWith(django_urlize(unicode(chunk)))

    return unicode(soup)
