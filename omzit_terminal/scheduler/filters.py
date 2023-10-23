import copy
from collections import OrderedDict

import django_filters
from django import forms
from django_filters import ChoiceFilter

from scheduler.models import ShiftTask

SHIFT_TASK_FILTER_FIELDS = (
    'id',
    'workshop',
    'order',
    'model_name',
    'datetime_done',
    'ws_number',
    'op_number',
    'op_name_full',
    'norm_tech',
    'fio_doer',
    'st_status'
)


class ShiftTaskFilter(django_filters.FilterSet):
    fields_values = {field: set() for field in SHIFT_TASK_FILTER_FIELDS}

    tasks = ShiftTask.objects.values(*SHIFT_TASK_FILTER_FIELDS)
    for task in tasks:
        for field, value in task.items():
            # if field == 'fio_doer' and ',' in value:
            #     for fio in value.split(', '):
            #         fields_values[field].add((fio, fio))
            # else:
            fields_values[field].add((value, value))

    order = ChoiceFilter(
        choices=fields_values['order'],
        widget=forms.Select(attrs={
            'onchange': "onChange()"
        }))
    model_name = ChoiceFilter(
        choices=fields_values['model_name'],
        widget=forms.Select(attrs={
            'onchange': "onChange()"
        }))
    datetime_done = ChoiceFilter(
        choices=fields_values['datetime_done'],
        widget=forms.Select(attrs={
            'onchange': "onChange()"
        }))
    fio_doer = ChoiceFilter(
        choices=fields_values['fio_doer'],
        widget=forms.Select(attrs={
            'onchange': "onChange()"
        }))

    def get_form_class(self):
        fields = OrderedDict(
            [(name, filter_.field) for name, filter_ in self.filters.items()]
        )


        return type(str("%sForm" % self.__class__.__name__), (self._meta.form,), fields)

    def __init__(self, data=None, queryset=None, *, request=None, prefix=None):
        if queryset is None:
            queryset = self._meta.model._default_manager.all()
        model = queryset.model

        self.is_bound = data is not None
        self.data = data or {}
        self.queryset = queryset
        self.request = request
        self.form_prefix = prefix

        self.filters = copy.deepcopy(self.base_filters)
        print(self.filters)

        # propagate the model and filterset to the filters
        for filter_ in self.filters.values():
            filter_.model = model
            filter_.parent = self

    class Meta:
        model = ShiftTask
        fields = SHIFT_TASK_FILTER_FIELDS
