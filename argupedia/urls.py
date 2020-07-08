from django.urls import path
from .views import (HomeView,
                    NewInitialArgumentView,
                    InitialActionCreateView,
                    InitialPopularCreateView,
                    InitialExpertCreateView,
                    NetworkDetailView,
                    NetworkListView,
                    ArgumentDetailView,
                    ArgumentWizard,
                    action_selected,
                    expert_selected,
                    popular_selected)
from .forms import (ArgumentForm,
                    ActionSchemeForm,
                    ExpertOpinionSchemeForm,
                    PopularOpinionSchemeForm)
from . import views

argument_forms = [ArgumentForm, ActionSchemeForm, ExpertOpinionSchemeForm, PopularOpinionSchemeForm]

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('networks/', NetworkListView.as_view(), name='network-list'),
    path('network/<int:pk>/', NetworkDetailView.as_view(), name='network-overview'),
    path('argument/<int:pk>/', ArgumentDetailView.as_view(), name='argument-details'),
    path('argument/<int:pk>/new_argument/', ArgumentWizard.as_view(argument_forms, condition_dict={'1': action_selected, '2': expert_selected, '3': popular_selected}), name='new-argument'),
    path('new_initial_argument/', NewInitialArgumentView.as_view(), name='new-initial-argument'),
    path('new_initial_argument/action/', InitialActionCreateView.as_view(), name='action-initial'),
    path('new_initial_argument/expert/', InitialExpertCreateView.as_view(), name='expert-initial'),
    path('new_initial_argument/popular/', InitialPopularCreateView.as_view(), name='popular-initial'),
    path('get_network_arguments/<int:pk>/', views.get_network_arguments, name='get-network-arguments')
]
