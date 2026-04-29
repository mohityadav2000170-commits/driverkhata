from django.shortcuts import render

from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.urls import reverse_lazy
from .models import Entry
from django.views.generic import DeleteView 
from django.contrib.auth.forms import UserCreationForm
from urllib.parse import quote

class DashboardView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = 'khata/dashboard.html'

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user).order_by('date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        entries = context['object_list']

        balance = 0
        running_data = []

        for e in entries:
            if e.type == "ADD":
                balance += e.amount
                debit = e.amount
                credit = 0
            else:
                balance -= e.amount
                debit = 0
                credit = e.amount

            running_data.append({
                'entry': e,
                'debit': debit,
                'credit': credit,
                'balance': balance
            })

        context['running_data'] = running_data
        context['balance'] = balance
        context['total_add'] = sum(x['debit'] for x in running_data)
        context['total_pay'] = sum(x['credit'] for x in running_data)

        return context


class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    fields = ['amount', 'type', 'note', 'phone']
    success_url = '/'

    def form_valid(self, form):
        form.instance.user = self.request.user

        amount = form.cleaned_data['amount']
        type = form.cleaned_data['type']
        phone = form.cleaned_data['phone']

        if type == "ADD":
            msg = f"You need to pay ₹{amount}"
        else:
            msg = f"You paid ₹{amount}"

        # Encode message
        message = quote(msg)

        # WhatsApp link
        self.whatsapp_url = f"https://wa.me/{phone}?text={message}"

        return super().form_valid(form)

    def get_success_url(self):
        return self.whatsapp_url

class EntryDeleteView(LoginRequiredMixin, DeleteView):
    model = Entry
    success_url = '/'

    def get_queryset(self):
        return Entry.objects.filter(user=self.request.user)  
    
class SignupView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('login')    

    def get_form(self):
        form = super().get_form()
        for field in form.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        return form
