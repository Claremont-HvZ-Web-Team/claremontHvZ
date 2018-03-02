# -*- coding: utf-8 -*-
from django import forms

def build_form(Form, _request, *args, **kwargs):
    """
    Build the ``Form`` instance.

    If ``request.method`` is ``POST`` then build bound form else build unbound.

    Usage example::

        @login_required
        @render_to('blog/post_create.html')
        def post_create(request):
            post = Post(instance=request.user)
            form = build_form(PostForm, request, instance=post)
            if form.is_valid():
                obj = form.save()
                return redirect(obj)
            return {'form': form,
                    }
    """

    if 'POST' == _request.method:
        form = Form(_request.POST, _request.FILES, *args, **kwargs)
    else:
        form = Form(*args, **kwargs)
    return form


class DeleteForm(forms.Form):
    """
    This form could be used in conjunction with ``build_form`` on pages where user have to confirm some action.

    Typical example of such page is deletion the some object.

    Fields:
        :next: this is optional field. You can use it to store redirection URL.

    Usage example::

        @render_to('blog/post_delete.html')
        def post_delete(request, postid):
            post = get_object_or_404(Post, pk=postid)
            form = build_form(DeleteForm, request, initial={'next': request.GET.get('next')})
            if form.is_valid():
                post.delete()
                return redirect(form.cleaned_data['next'] or '/')
            return {'form': form,
                    'post': post,
                   }
    """

    next = forms.CharField(required=False, widget=forms.HiddenInput)
