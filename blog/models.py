# blog/models.py
from django.db import models
from django.utils.text import slugify
from markdownx.models import MarkdownxField


class Category(models.Model):
    """Kategorie: Python, Django, etc."""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=10, default='📚', help_text="Emoji jako ikona")
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.icon} {self.name}"


class Lesson(models.Model):
    """Lekcje/artykuły"""

    DIFFICULTY_CHOICES = [
        ('beginner', '⭐ Początkujący'),
        ('intermediate', '⭐⭐ Średniozaawansowany'),
        ('advanced', '⭐⭐⭐ Zaawansowany'),
    ]

    STATUS_CHOICES = [
        ('draft', 'Szkic'),
        ('published', 'Opublikowany'),
    ]

    # Podstawowe
    title = models.CharField('Tytuł', max_length=200)
    slug = models.SlugField('Slug', unique=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='lessons',
        verbose_name='Kategoria'
    )

    # Treść
    content = MarkdownxField('Treść')
    excerpt = models.TextField(
        'Krótki opis',
        max_length=300,
        blank=True,
        help_text='Wyświetlany na listach'
    )

    # Metadane
    difficulty = models.CharField(
        'Poziom trudności',
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default='beginner'
    )
    status = models.CharField(
        'Status',
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft'
    )

    # Daty
    created_at = models.DateTimeField('Utworzono', auto_now_add=True)
    updated_at = models.DateTimeField('Zaktualizowano', auto_now=True)
    published_at = models.DateTimeField('Opublikowano', null=True, blank=True)

    # Statystyki
    views_count = models.IntegerField('Liczba wyświetleń', default=0)

    class Meta:
        ordering = ['-published_at', '-created_at']
        verbose_name = 'Lekcja'
        verbose_name_plural = 'Lekcje'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Resource(models.Model):
    """Zasoby - linki do dokumentacji, tutoriali, narzędzi"""

    TYPE_CHOICES = [
        ('documentation', '📖 Dokumentacja'),
        ('tutorial', '🎥 Tutoriale'),
        ('tool', '🛠️ Narzędzia'),
        ('article', '📄 Artykuły'),
        ('course', '🎓 Kursy'),
        ('other', '🔗 Inne'),
    ]

    title = models.CharField('Tytuł', max_length=150)
    description = models.TextField(
        'Opis',
        max_length=200,
        help_text='Krótki opis zasobu (max 200 znaków)'
    )
    url = models.URLField('Link', max_length=500)
    resource_type = models.CharField(
        'Typ zasobu',
        max_length=20,
        choices=TYPE_CHOICES,
        default='other'
    )

    # Dodatkowe pola
    is_external = models.BooleanField(
        'Zewnętrzny link',
        default=True,
        help_text='Czy link prowadzi na zewnętrzną stronę'
    )
    order = models.IntegerField('Kolejność', default=0)

    # Daty
    created_at = models.DateTimeField('Dodano', auto_now_add=True)
    updated_at = models.DateTimeField('Zaktualizowano', auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = 'Zasób'
        verbose_name_plural = 'Zasoby'

    def __str__(self):
        return f"{self.get_resource_type_display()} {self.title}"