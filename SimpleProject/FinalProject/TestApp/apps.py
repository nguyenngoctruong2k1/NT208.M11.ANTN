from django.apps import AppConfig


class TestappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'TestApp'

    # Tự động sửa database khi vừa mới lưu
    def ready(self):
        from TestApp import signals