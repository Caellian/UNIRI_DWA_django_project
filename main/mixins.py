from django.http import HttpResponseNotFound
from django.utils.translation import gettext as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404

from .models import *

class MultiSlugMixin:
    # Source: https://stackoverflow.com/questions/62211927/in-django-class-based-views-how-i-do-i-use-multiple-slugs-with-slug-url-kwarg

    pk_url_kwarg = 'pk'
    slug_url_kwargs = {'slug': 'slug'}  # {field: url_kwarg}
    query_pk_and_slug = False

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.kwargs.get(self.pk_url_kwarg)
        slugs = {
            field: self.kwargs[url_kwarg]
            for field, url_kwarg in self.slug_url_kwargs.items()
        }
        if pk is not None:
            queryset = queryset.filter(pk=pk)

        if slugs and (pk is None or self.query_pk_and_slug):
            queryset = queryset.filter(**slugs)

        if pk is None and not slugs:
            raise AttributeError(
                "Generic detail view %s must be called with either an object "
                "pk or a slug in the URLconf." % self.__class__.__name__
            )

        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise HttpResponseNotFound(_("No %(verbose_name)s found matching the query") %
                                       {'verbose_name': queryset.model._meta.verbose_name})
        return obj


class TeamRequiredMixin(LoginRequiredMixin):
    team_model = Team

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        if "team_namespace" in kwargs:
            team = get_object_or_404(self.team_model, namespace=kwargs.get('team_namespace'))

            if not team.members.filter(id=request.user.id).exists():
                return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
