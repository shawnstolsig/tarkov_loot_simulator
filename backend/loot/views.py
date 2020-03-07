from django.shortcuts import render


# Create your views here.
def server_data_panel(request):
    context = {'message': 'hello world'}
    return render(request, 'panel.html', context)

# def load_containers(request):
#     context = {'message': 'hello world'}
#     return render(request, 'panel.html', context)

def load_containers(request):
    print("received containers file from frontend")
    print(request.__all__)

def load_tables(request):
    print("received table file from frontend ")