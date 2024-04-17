from django.db import models
from django.utils.translation import gettext_lazy as _

from .model_mixins import StatisticResultBusinessLogicMixin


class StatisticResult(StatisticResultBusinessLogicMixin, models.Model):
    # Translators: 'Slug' refers to the URL valid ID of the statistic
    # More info: https://docs.djangoproject.com/en/1.7/glossary/#term-slug
    slug = models.SlugField(
        unique=True, verbose_name=_(message='Slug')
    )
    datetime = models.DateTimeField(
        auto_now=True, verbose_name=_(message='Date time')
    )
    serialize_data = models.TextField(
        blank=True, verbose_name=_(message='Data')
    )

    class Meta:
        verbose_name = _(message='Statistics result')
        verbose_name_plural = _(message='Statistics results')

    def __str__(self):
        return self.slug
