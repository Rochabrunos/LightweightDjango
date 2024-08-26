from django_filters import FilterSet, BooleanFilter, DateFromToRangeFilter
from django.contrib.auth import get_user_model

from .models import Task, Sprint

User = get_user_model()

class NullFilter(BooleanFilter):
    """Filter on a field set as null or not."""

    def filter(self, qs, value):
        if value is not None:
            return qs.filter(**{'%s__isnull' % self.name: value})
        return qs

class TaskFilter(FilterSet):

    backlog = NullFilter(name='sprint')

    class Meta:
        model = Task
        fields = ('sprint', 'status', 'assigned', 'backlog',)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.filters['assigned'].extra.update(
            {'to_field_name': User.USERNAME_FIELD},
        )

class SprintFilter(FilterSet):

    end = DateFromToRangeFilter('end')

    class Meta:
        model = Sprint
        fields = ('end',)