from django import conf

def settings(request):
    return {'SETTINGS': conf.settings}
