from datetime import*

def current_year(request):
    return {'current_year': datetime.now().year}

