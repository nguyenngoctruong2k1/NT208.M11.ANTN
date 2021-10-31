from django.db import models

class Khoa(models.Model):
    name = models.CharField(max_length=50)
    Ma = models.CharField(max_length=49)
    def __str__(self):
        return self.name

class Student(models.Model):
    """
    Lưu dữ liệu về sinh viên
    """

    name = models.CharField(max_length=30, help_text="Họ và tên của sinh viên.")
    student_code = models.CharField(max_length=18, help_text="Mã số sinh viên")
    gender_choices = (
        ('N','Nam'),
        ('F','Nữ')
    )
    gender = models.CharField(max_length=1, choices=gender_choices, default='N')
    birth_place = models.CharField(max_length=100)
    birthday = models.DateField(blank=True, null=True)
    age = models.DecimalField(max_digits=3,decimal_places=1,default=0)
    khoa = models.ForeignKey(Khoa, on_delete=models.PROTECT)

    def __str__(self):
        return self.name