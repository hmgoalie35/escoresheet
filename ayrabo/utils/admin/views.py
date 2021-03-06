import csv

from django import forms
from django.contrib import messages
from django.shortcuts import render
from django.views import generic

from ayrabo.utils.admin.forms import AdminBulkUploadForm


class AdminBulkUploadView(generic.FormView):
    template_name = 'admin/bulk_upload.html'
    success_url = None
    model = None
    fields = None
    form_class = AdminBulkUploadForm
    # Custom variables
    model_form_class = None
    model_formset_class = None
    admin_site = None

    def get_form_value(self, key, value, row):
        func_name = key.replace(' ', '_').lower()
        func = getattr(self, 'get_{}'.format(func_name), None)
        if func is not None:
            return func(value, row)
        return value

    def as_form_data(self, row, count):
        data = {}
        for key, value in row.items():
            key = key.strip()
            value = value.strip()
            new_key = 'form-{}-{}'.format(count, key)
            data[new_key] = self.get_form_value(key, value, row)
        return data

    def clean_data(self, uploaded_file):
        rows = [row.decode() for row in uploaded_file]
        uploaded_file.seek(0)
        reader = csv.DictReader(rows)
        cleaned_data = {}
        raw_data = []
        count = 0
        for row in reader:
            raw_data.append(row)
            form_data = self.as_form_data(row, count)
            cleaned_data.update(form_data)
            count += 1
        cleaned_data['form-TOTAL_FORMS'] = count
        cleaned_data['form-INITIAL_FORMS'] = 0
        return cleaned_data, raw_data

    def get_formset_class(self):
        kwargs = {}
        if self.fields:
            kwargs['fields'] = self.fields
        if self.model_form_class:
            kwargs['form'] = self.model_form_class
        if self.model_formset_class:
            kwargs['formset'] = self.model_formset_class
        return forms.modelformset_factory(self.model, **kwargs)

    def get_model_form_kwargs(self, data, raw_data):
        return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.admin_site.each_context(self.request))
        return context

    def form_valid(self, form):
        uploaded_file = form.cleaned_data.get('file')
        cleaned_data, raw_data = self.clean_data(uploaded_file)
        FormSetClass = self.get_formset_class()
        formset = FormSetClass(cleaned_data, form_kwargs=self.get_model_form_kwargs(cleaned_data, raw_data))
        if not formset.is_valid():
            context = self.get_context_data()
            context.update({'formset': formset})
            return render(self.request, self.template_name, context)
        instances = formset.save()
        num_instances = len(instances)
        opts = self.model._meta
        verbose_name = opts.verbose_name
        verbose_name_plural = opts.verbose_name_plural
        base_msg = f'Successfully created {num_instances}'
        if num_instances == 0:
            messages.warning(self.request, f'{num_instances} {verbose_name_plural} created. Is the csv empty?')
        elif num_instances == 1:
            messages.success(self.request, f'{base_msg} {verbose_name}')
        else:
            messages.success(self.request, f'{base_msg} {verbose_name_plural}')
        return super().form_valid(form)
