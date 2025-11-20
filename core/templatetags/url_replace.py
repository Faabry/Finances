# your_app_name/templatetags/url_replace.py

from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """
    Replaces or adds given GET parameters to the current URL.
    Resets 'page' to 1 when 'sort' or 'order' changes.
    """
    request = context['request']
    url_params = request.GET.copy()
    
    # Check if a sort or order parameter is being changed/set
    sort_or_order_changed = 'sort' in kwargs or 'order' in kwargs

    for key, value in kwargs.items():
        if value is not None:
            url_params[key] = value

    # If the user clicks a sort link, we must ensure both 'sort' and 'order' are set,
    # and reset the page number.
    if sort_or_order_changed:
        # If 'order' is changing but 'sort' wasn't passed, use the current sort column
        if 'order' in kwargs and 'sort' not in kwargs and 'current_sort' in context:
            url_params['sort'] = context['current_sort']

        # Reset page number to 1 on sort/order change
        if 'page' in url_params:
            url_params['page'] = 1

    return f"{request.path}?{url_params.urlencode()}"