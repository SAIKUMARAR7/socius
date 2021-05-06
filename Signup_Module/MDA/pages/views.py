from django.shortcuts import render

def aboutPageView(request):
    return render(request, 'main/about.html', {'current_user': request.user})

def searchView(request):
    return render(request, 'main/search.html', {'current_user': request.user})