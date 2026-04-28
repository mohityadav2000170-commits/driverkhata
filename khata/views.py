from django.shortcuts import render

from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.urls import reverse_lazy
from .models import Entry
from django.views.generic import DeleteView

class DashboardView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = 'khata/dashboard.html'

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        entries = self.get_queryset()

        total_add = entries.filter(type='ADD').aggregate(Sum('amount'))['amount__sum'] or 0
        total_pay = entries.filter(type='PAY').aggregate(Sum('amount'))['amount__sum'] or 0

        context['total_add'] = total_add
        context['total_pay'] = total_pay
        context['balance'] = total_add - total_pay

        return context


class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    fields = ['amount', 'type', 'note']
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class EntryDeleteView(LoginRequiredMixin, DeleteView):
    model = Entry
    success_url = '/'

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)  
