from datetime import date

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Sprint, Task

User = get_user_model()

class SprintSerializer(serializers.ModelSerializer):

    links = serializers.SerializerMethodField('get_links')
    
    class Meta:
        model = Sprint
        fields = ('id', 'name', 'description', 'end', 'links')
    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('sprint-detail', kwargs={'pk': obj.pk}, request=request),
            'taks': reverse('task-list', request=request) + '?sprint={}'.format(obj.pk),
        }

    def validate_end(self, end_date):
        if end_date <= date.today():
            msg =_('End date cannot be in the past.')
            raise serializers.ValidationError(msg)
        return end_date
    
class TaskSerializer(serializers.ModelSerializer):
    
    assigned = serializers.SlugRelatedField(
        slug_field=User.USERNAME_FIELD, 
        required=False,
        queryset=User.objects.all())
    status_diplay = serializers.CharField(source='get_status_display')
    links = serializers.SerializerMethodField('get_links')
    
    class Meta:
        model = Task
        fields = ('id', 'name', 'description', 'sprint', 'status_diplay',
                  'order', 'assigned', 'due', 'completed', 'links')

    def get_status_diplay(self, obj):
        return obj.get_status_display(),
    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('task-detail', kwargs={'pk': obj.pk}, request=request),
        }

    def validate_sprint(self, sprint:Sprint):
        formData = Task(self.get_initial())
        if formData and formData.id:
            if sprint.id != formData.sprint:
                if formData.status == Task.STATUS_DONE:
                    msg = _('Cannot change the sprint of a completed task.')
                    raise serializers.ValidationError(msg)
                if sprint and sprint.end < date.today():
                    msg = _('Cannot assign tasks to past sprints.')
                    raise serializers.ValidationError(msg)
        else:
            if sprint and sprint.end < date.today():
                msg = _('Cannot add task to past sprints.')
                raise serializers.ValidationError(msg)

        return sprint

    def validate(self, attrs:Task):
        sprint = attrs.get('sprint')
        
        # There are few status choices, in the case of that list grows this need to be changed 
        status = dict((u,v) for v,u in Task.STATUS_CHOICES)[attrs['get_status_display']]
        attrs['status'] = status
        attrs.pop('get_status_display', None)

        if status == 0:
            msg = _('The status must be a valid one.')
            raise serializers.ValidationError(msg)
        started = attrs.get('started')
        completed= attrs.get('completed')

        if not sprint and status != Task.STATUS_TODO:
            msg = _('Backlog tasks must have "Not Started" status.')
            raise serializers.ValidationError(msg)
        if started and status == Task.STATUS_DONE:
            msg = _('Completed date cannot be set for uncompleted tasks.')
            raise serializers.ValidationError(msg)
        if completed and status != Task.STATUS_DONE:
            msg = _('Completed date cannot be set for uncompleted tasks.')
            raise serializers.ValidationError(msg)
        return attrs


class UserSerializer(serializers.ModelSerializer):
    
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    links = serializers.SerializerMethodField('get_links')
    
    class Meta:
        model = User
        fields = ('id', User.USERNAME_FIELD, 'full_name', 'is_active', 'links')

    def get_links(self, obj):
        request = self.context['request']
        username = obj.get_username()
        links = {
            'self': reverse('user-detail', kwargs={User.USERNAME_FIELD: username }, request=request),
            'sprint': None,
            'assigned': None,
            'tasks': '{}?assigned={}'.format(reverse('task-list', request=request), username),
        }
        if obj.sprint_id:
            links['sprint'] = reverse('sprint-detail', kwargs={'pk': obj.sprint_id}, request=request)
        if obj.assigned:
            links['assigned'] = reverse('user-detail', kwargs={User.USERNAME_FIELD: obj.assigned}, request=request)
        
        return links
