# ĐỒ ÁN LẬP TRÌNH ỨNG DỤNG WEB
## Thông tin chung
- Tên đồ án: [Web chia sẻ tài liệu học tập UIT](https://djangoprojectbutterflies.herokuapp.com/)
- Mã lớp: NT208.M11.ANTN
- Nhóm: 6
- Thầy hướng dẫn: Trần Tấn Dũng
## Thông tin thành vên nhóm 
|STT|Họ và tên|Mã số SV|
|-|-|-|
|1|Nguyễn Ngọc Trưởng (trưởng nhóm)|19522440|
|2|Lê Tôn Nhân|19520199|
|3|Hồ Thị Ngọc Phúc|19520220|
## Giới thiệu chung về đồ án 
### 1. Framework:
- Bootstrap 4
- Django
### 2. Tính năng với các nhóm người dùng
- Người dùng khách (Không đăng nhập)
    > Xem các tài liệu học tập dựa theo môn học<br/>
    > Tìm kiếm các tài liệu<br/>
    > Xem các tài liệu mới nhất được gởi lên<br/>
- Người dùng thường (Đã Đăng ký/Đăng nhập)
    > Có các quyền của người dùng khách<br/>
    > Cho phép bình luận các tài liệu, môn học<br/>
    > Cho phép đóng góp tài liệu, và xem lại danh sách các tài liệu đã đăng của mình<br/>
    > Xem thông tin cả tất cả các môn học, đã có trên hệ thống<br/>
    > Thay đổi thông tin cá nhân<br/>
    > Xem các bài viết đã xem gần đây<br/>
- Cộng tác viên (người dùng đã được duyệt làm quản trị viên)
    > Cho phép thay đổi quyền của các user: khóa/mở tài khoản, thêm/xóa quyền quản trị viên<br/>
    > Duyệt, xem xét, xóa tài liệu<br/>
- Quản trị viên (người dùng superuser)
    > Một tài khoản duy nhất<br/>
    > Có tất cả các quyền của cộng tác viên<br/>
    > có quyền truy cập vào trang /admin<br/>
### 3. Triển khai:
- Heroku: [djangoprojectbutterflies](https://djangoprojectbutterflies.herokuapp.com/)
### 4. Cây thư mục
```
FINALPROJECT
├───FINALPROJECT
├───media
│   ├───avatar
│   └───document
└───myproject
    ├───migrationss
    ├───static
    │   ├───css
    │   └───image
    ├───templates
    └───templatetags
```

