from django.shortcuts import redirect

def get_next(request):
    if request.method == 'POST':
        return request.POST.get('next')
    elif request.method == 'GET':
        return request.GET.get('next')
    else:
        return None

def next_or_dashboard(request):
    next = get_next(request)
    if next is not None and next != "":
        return redirect(next)
    else:
        return redirect('main:dashboard')

        
