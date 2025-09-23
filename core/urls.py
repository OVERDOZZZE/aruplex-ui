from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('client/', include('client.urls')),
    path('dashboard/', include('dashboard.urls')),

    path('', TemplateView.as_view(template_name='landing.html'), name='landing'),
    path('about/', TemplateView.as_view(template_name='about.html'), name='about'),
    path('pricing/', TemplateView.as_view(template_name='pricing.html'), name='pricing'),
    path('contact/', TemplateView.as_view(template_name='contact.html'), name='contact'),
    path('privacy_policy/', TemplateView.as_view(template_name='privacy_policy.html'), name='privacy_policy'),
]
