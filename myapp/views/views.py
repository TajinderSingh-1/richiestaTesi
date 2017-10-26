from myapp.views.views_accesso import *

def index(request):
    return render(request, 'myapp/index.html')
