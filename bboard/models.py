from django.db import models
from django.utils import timezone
from django.urls import reverse
from slugify import slugify

class Bb(models.Model):
    title = models.CharField(max_length=50, verbose_name='Товар')
    content = models.TextField(null=True, blank=True, verbose_name='Описание')
    price = models.FloatField(null=True, blank=True, verbose_name='Цена')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    image = models.ImageField(upload_to='postings/', null=True, verbose_name='Изображение')
    # slug = models.SlugField(max_length=200, unique=True, editable=False, null=True)

    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, verbose_name='Рубрика')

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.title)
    #     super().save(*args, **kwargs)
    #
    # def get_absolute_url(self):
    #     return reverse('bboard:read_bb', kwargs={'slug': self.slug})

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-published']

class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['name']