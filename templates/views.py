from django.shortcuts import render

# Create your views here.
def templates(request):
    return render(request, 'templates/templates.html')

def template(request, str):
    if str == '1':
        return render(request, 'templates/template.html')
    elif str == '2':
        return render(request, 'templates/template2.html')
    elif str == '3':
        return render(request, 'templates/template3.html')
    else:
        return render(request, 'templates/templates.html')