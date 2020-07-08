from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import F
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, DetailView, ListView
from django.views.generic.edit import FormView
from formtools.wizard.views import SessionWizardView
from .models import Network, Argument, Scheme, ActionScheme, ExpertOpinionScheme, PopularOpinionScheme
from .choices import ActionCQChoices, ExpertCQChoices, PopularCQChoices
from .forms import ArgumentForm

class HomeView(TemplateView):
    template_name = 'argupedia/home.html'

class NetworkListView(LoginRequiredMixin, ListView):

    login_url = '/login/'

    model = Network
    context_object_name = 'networks'
    ordering = ['-date_created']
    paginate_by = 5

class NetworkDetailView(LoginRequiredMixin, DetailView):

    login_url = '/login/'

    model = Network
    context_object_name = 'network'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['initial'] = self.object.initial_argument
        context['arguments'] = self.object.argument_set.all()
        return context

class ArgumentDetailView(LoginRequiredMixin, DetailView):

    login_url = '/login/'

    model = Argument
    context_object_name = 'argument'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['scheme'] = Scheme.objects.get(argument_id=self.object.id)
        context['attackers'] = self.object.attackers.all()
        if self.object.attacking:
            cq_value = self.object.target_critical_question
            parent_scheme_type = self.object.attacking.scheme_type
            if parent_scheme_type == 'action':
                context['critical_question'] = ActionCQChoices(cq_value).label
            elif parent_scheme_type == 'expert':
                context['critical_question'] = ExpertCQChoices(cq_value).label
            elif parent_scheme_type == 'popular':
                context['critical_question'] = PopularCQChoices(cq_value).label

        return context

class NewInitialArgumentView(LoginRequiredMixin, TemplateView):

    login_url = '/login/'

    template_name = 'argupedia/initial_scheme_select.html'

class ArgumentWizard(LoginRequiredMixin, SessionWizardView):

    login_url = '/login/'

    template_name='argupedia/wizard_form.html'

    def get_form_kwargs(self, step):
        kwargs = super(ArgumentWizard, self).get_form_kwargs()

        if step == '0':
            kwargs.update(self.kwargs)
        return kwargs

    def done(self, form_list, **kwargs):

        cleaned_data = self.get_all_cleaned_data()
        argument = Argument()
        attacked_argument = Argument.objects.get(id=self.kwargs['pk'])
        argument.target_critical_question = cleaned_data.get('target_critical_question')
        argument.network = attacked_argument.network
        argument.attacking = attacked_argument
        argument.scheme_type = cleaned_data.get('scheme_type')
        scheme = Scheme()

        if argument.scheme_type == 'action':
            scheme = ActionScheme()
            scheme.situation = cleaned_data.get('situation')
            scheme.action = cleaned_data.get('action')
            scheme.goal = cleaned_data.get('goal')
            scheme.value = cleaned_data.get('value')
        elif argument.scheme_type == 'expert':
            scheme = ExpertOpinionScheme()
            scheme.domain = cleaned_data.get('domain')
            scheme.expert_source = cleaned_data.get('expert_source')
            scheme.assertion = cleaned_data.get('assertion')
            scheme.reference = cleaned_data.get('reference')
        elif argument.scheme_type == 'popular':
            scheme = PopularOpinionScheme()
            scheme.assertion = cleaned_data.get('assertion')
            scheme.reference = cleaned_data.get('reference')

        argument.save()
        scheme.argument = argument
        scheme.save()

        argument.network.grounded_algorithm()

        return redirect('argument-details', pk=argument.id)

def action_selected(wizard):

    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}

    return 'action' == cleaned_data.get('scheme_type')

def expert_selected(wizard):

    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}

    return 'expert' == cleaned_data.get('scheme_type')

def popular_selected(wizard):

    cleaned_data = wizard.get_cleaned_data_for_step('0') or {}

    return 'popular' == cleaned_data.get('scheme_type')

class InitialActionCreateView(LoginRequiredMixin, CreateView):

    login_url = '/login/'

    model = ActionScheme
    fields = ['situation', 'action','goal','value']

    def form_valid(self, form):
        scheme = form.save(commit=False)
        network = Network()
        network.save()
        argument = Argument()
        argument.network = network
        argument.scheme_type = 'action'
        argument.scheme_added = True
        argument.save()
        network.initial_argument = argument
        network.save()
        scheme.argument = argument
        scheme.save()
        return redirect('argument-details', pk=argument.id)

class InitialExpertCreateView(LoginRequiredMixin, CreateView):

    login_url = '/login/'

    model = ExpertOpinionScheme
    fields = ['domain','expert_source','assertion','reference']

    def form_valid(self, form):
        scheme = form.save(commit=False)
        network = Network()
        network.save()
        argument = Argument()
        argument.network = network
        argument.scheme_type = 'expert'
        argument.scheme_added = True
        argument.save()
        network.initial_argument = argument
        network.save()
        scheme.argument = argument
        scheme.save()
        return redirect('argument-details', pk=argument.id)

class InitialPopularCreateView(LoginRequiredMixin, CreateView):

    login_url = '/login/'

    model = PopularOpinionScheme
    fields = ['assertion', 'reference']

    def form_valid(self, form):
        scheme = form.save(commit=False)
        network = Network()
        network.save()
        argument = Argument()
        argument.network = network
        argument.scheme_type = 'popular'
        argument.scheme_added = True
        argument.save()
        network.initial_argument = argument
        network.save()
        scheme.argument = argument
        scheme.save()
        return redirect('argument-details', pk=argument.id)

def get_network_arguments(request, pk):
    data = Argument.objects.filter(network_id=pk,attacking__isnull=False).values('state',source=F('id'),target=F('attacking_id'))
    #data = Argument.objects.filter(network_id=pk).values('state',source=F('id'),target=F('attacking_id'))
    return JsonResponse(list(data), safe=False)
