from django.urls import path
from .views import simple_string_view, chatbot_res, chatbot_res_with_id, check_process, document_details
from .config import config_list, create_config

__all__ = ('urlpatterns',)

urlpatterns = []

config = [
     path('config_list', config_list, name='config_list'),
    path('create_config', create_config, name='create_config'),
]

urlpatterns = [
    path('simple/', simple_string_view, name='simple_string_view'),
    path('check_process/<int:doc_id>', check_process, name='check_process'),
    path('chatbot_res', chatbot_res, name='chatbot_res'),
    path('chatbot_res_with_id/<int:doc_id>', chatbot_res_with_id, name='chatbot_res_with_id'),
    path('verified_files',  document_details, name='verified_files'),
]

urlpatterns.extend(config)
