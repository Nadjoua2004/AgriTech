from django.conf import settings
from django.views.generic import TemplateView


class DashboardView(TemplateView):
    template_name = 'dashboard.html'


class AgritectureView(TemplateView):
    template_name = 'agritecture.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['MAPBOX_TOKEN'] = settings.MAPBOX_TOKEN
        return context
