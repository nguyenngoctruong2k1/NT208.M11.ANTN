""" from django.db.models.signals import pre_save
from django.dispatch import receiver
from myproject.models import Student
import arrow

@receiver(pre_save,sender=Student)
def handl_pre_save_model_student(sender, instance: Student, **kwargs):
    #Xử lý các dữ liệu trước khi được lưu vào csdl
    if instance.birthday:
        now = arrow.now()
        bth = arrow.get(instance.birthday)
        dt = now - bth
        instance.age = round(dt.total_seconds()/(3600*24*365),1)
 """