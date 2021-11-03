## Cài đặt môi trường
- mở teminal trên vscode
- thực hiện lệnh `python3 -m venv venv` 
- thực hiện:
    - Ctrl +Shift + P
    - gõ `python: Select Interpreter`
    - chọn python3: thư mục ./venv/Scripts/python3
- vào cmd trên vscode
- cài đặt một số gói:
    - pip install -U wheel 
    - pip install django 
- Tạo project `django-admin startproject MyProject`
# Các lệnh 
- Tạo 1 project mới
> django-admin startproject FinalProject
- Tạo 1 app mới
> python manage.py startapp MainApp
- Kiểm tra thay đổi trong cơ sở dữ liệu lưu vào bộ nhớ tạm
> python manage.py makemigrations
- Lưu database
> python manage.py migrate
- Run python manage.py runserver
# một số gói cài thêm 
> pip install icecream
> pip install django-ckeditor