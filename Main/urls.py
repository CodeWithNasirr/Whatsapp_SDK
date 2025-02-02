from django.urls import path
from . import views

urlpatterns = [
    path("send-template/",views.SendWhatsAppTemplateView.as_view(), name="send-template"),
    path("check_template_status/<str:template_name>/", views.check_template_status, name="check_template_status"),
    # path("send-message/", views.send_whatsapp_message, name="send_whatsapp_message"),
    path("create-template/", views.create_template, name="create-template"),
    path("template-message/", views.send_template_message, name="send_whatsapp_template"),
    path("webhook/", views.whatsapp_webhook, name="whatsapp_webhook"),
]
