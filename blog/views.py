# blog/views.py
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render

from .models import Category, Lesson, Resource


def lesson_list(request, category_slug=None):
    """Lista lekcji z filtrowaniem po kategorii i poziomie trudności"""

    current_category = None
    lessons = Lesson.objects.filter(status='published')

    # Filtrowanie po kategorii (z URL)
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        lessons = lessons.filter(category=current_category)

    # Filtrowanie po poziomie trudności (z query params)
    difficulty = request.GET.get('difficulty')
    if difficulty:
        lessons = lessons.filter(difficulty=difficulty)

    # Liczba lekcji po zastosowaniu filtrów
    total_lessons = lessons.count()

    # Paginacja
    paginator = Paginator(lessons, 12)  # 12 lekcji na stronę
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Kontekst
    context = {
        'lessons': page_obj,
        'categories': Category.objects.all(),
        'total_lessons': total_lessons,
        'page_obj': page_obj,  # dla templatek paginacji
        'is_paginated': page_obj.has_other_pages,  # dla templatek paginacji
        'category': current_category,  # aktualna kategoria dla filtra
    }

    return render(request, 'blog/lesson_list.html', context)


def lesson_detail(request, slug):
    """Szczegóły pojedynczej lekcji"""

    # Pobierz lekcję lub 404
    lesson = get_object_or_404(
        Lesson,
        slug=slug,
        status='published'
    )

    # Zwiększ licznik wyświetleń
    lesson.views_count += 1
    lesson.save(update_fields=['views_count'])

    context = {
        'lesson': lesson,
    }

    return render(request, 'blog/lesson_detail.html', context)


def home(request):
    """Landing page z wprowadzeniem"""
    # Pobierz statystyki
    total_lessons = Lesson.objects.filter(status='published').count()
    categories = Category.objects.all()

    # Najnowsze lekcje
    recent_lessons = Lesson.objects.filter(
        status='published'
    ).select_related('category').order_by('-created_at')[:4]

    # Lekcje dla początkujących
    beginner_lessons = Lesson.objects.filter(
        status='published',
        difficulty='beginner'
    ).select_related('category')[:3]

    context = {
        'total_lessons': total_lessons,
        'categories': categories,
        'recent_lessons': recent_lessons,
        'beginner_lessons': beginner_lessons,
    }

    return render(request, 'blog/home.html', context)


def about(request):
    """Strona O mnie"""
    return render(request, 'blog/about.html')


def resources(request):
    """Lista zasobów z filtrowaniem po typie"""

    # Pobierz wszystkie zasoby posortowane
    resources = Resource.objects.all().order_by('order', '-created_at')

    # Filtrowanie po typie (z query params)
    resource_type = request.GET.get('type')
    if resource_type:
        resources = resources.filter(resource_type=resource_type)

    # Grupowanie zasobów po typie dla wyświetlenia
    resources_by_type = {}
    for resource in resources:
        if resource.resource_type not in resources_by_type:
            resources_by_type[resource.resource_type] = []
        resources_by_type[resource.resource_type].append(resource)

    context = {
        'resources': resources,
        'resources_by_type': resources_by_type,
        'selected_type': resource_type,
    }

    return render(request, 'blog/resources.html', context)
