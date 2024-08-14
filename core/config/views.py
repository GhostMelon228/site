from django.shortcuts import render


def bad_request_400_view(request, exception):
    """
    Обработка ошибки 400
    """
    return render(request, 'general/400.html', status=400)

def http_forbidden_403_view(request, exception):
    """
    Обработка ошибки 403
    """
    return render(request, 'general/403.html', status=403)

def page_not_found_404_view(request, exception):
    """
    Обработка ошибки 404
    """
    return render(request, 'general/404.html', status=404)

def server_error_500_view(request):
    """
    Обработка ошибки 500
    """
    return render(request, 'general/500.html', status=500)