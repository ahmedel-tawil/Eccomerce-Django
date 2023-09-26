from django import template

register = template.Library()


@register.simple_tag
def url_replace_diff(request, field, value):
    """
    Give a field and a value and it's update the post parameter for the url accordly
    """
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()
