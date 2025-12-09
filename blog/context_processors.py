# blog/context_processors.py
from .models import Category


def categories(request):
    """Dodaj kategorie do wszystkich templates"""
    return {
        'categories': Category.objects.all()
    }