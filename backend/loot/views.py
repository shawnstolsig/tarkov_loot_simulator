from django.shortcuts import render


# Create your views here.
def server_data_panel(request):
    context = {'message': 'hello world'}
    return render(request, 'panel.html', context)

def load_containers(request):
    context = {'message': 'hello world'}
    return render(request, 'panel.html', context)
