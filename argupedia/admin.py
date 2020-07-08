from django.contrib import admin
from .models import Network, Argument, Scheme, ActionScheme, ExpertOpinionScheme, PopularOpinionScheme


# Register your models here.
admin.site.register(Network)
admin.site.register(Argument)
admin.site.register(ActionScheme)
admin.site.register(ExpertOpinionScheme)
admin.site.register(PopularOpinionScheme)
