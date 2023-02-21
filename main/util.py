from django.shortcuts import redirect

def get_next(request):
    if request.method == 'POST':
        return request.POST.get('next') or ""
    elif request.method == 'GET':
        return request.GET.get('next') or ""
    else:
        return ""

def next_or_redirect(request, to):
    next = get_next(request)
    if next is not None and isinstance(next, str) and next != "" and '://' not in next:
        return redirect(next)
    else:
        return redirect(to)

def next_or_dashboard(request):
    return next_or_redirect(request, 'main:dashboard')
