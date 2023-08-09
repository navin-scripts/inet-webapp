# from django.apps import AppConfig

# class MerakiConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'  # Customize the auto-generated primary key field if needed
#     name = 'scripts.meraki'
#     verbose_name = 'Meraki'

#     def ready(self):
#         # Optional: You can perform any app-specific initialization or setup tasks here
#         from .utils import update_meraki_devices
#         # update_meraki_devices()
#         # from .models import MerakiDevice

#         # for field in MerakiDevice._meta.get_fields():
#         #     print(field.name)

