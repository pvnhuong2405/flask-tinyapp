# Thông tin cá nhân

Pham Thi Ngoc Huong


# Mô tả project

Tạo một website chia sẻ các bài viết về cách chăm sóc, chữa bệnh, truyền cảm hứng nuôi chó mèo. Ở đây người dùng(user) có thể login tài khoản sao đó có thể đăng kiến thức bổ ích về chó mèo. Admin quản lí bài viết ()

Use Case Diagram - Website Chia Sẻ Kiến Thức Về Chó Mèo

# V1: Cơ bản

- Actors:
  - User (Người dùng chưa đăng nhập)
  - Registered User (Người dùng đã đăng nhập)
  - Admin
- Use Cases:
  - Xem danh sách bài viết

# V2: Đăng ký/Đăng nhập

- Actors:
  - User
  - Registered User
- Use Cases:
  - Đăng ký tài khoản
  - Đăng nhập
  - Đăng xuất

# V3: Trang Admin Quản Lý User

- Actors:
  - Admin
- Use Cases:
  - Xem danh sách user
  - Khóa/mở khóa tài khoản user
  - Reset mật khẩu user
  - Xoá bài viết
  - Duyệt bài viết

# V4: Xóa nhiều bài viết cùng lúc

- Actors:
  - Registered User
  - Admin
- Use Cases:
  - Chọn nhiều bài viết cần xóa
  - Xóa các bài viết đã chọn

# V5: Phân trang

- Actors:
  - User
  - Registered User
  - Admin
- Use Cases:
  - Chuyển trang khi xem danh sách bài viết
  - Giới hạn số bài viết hiển thị trên mỗi trang
# V6: Tương tác bài viết
- Actors:
  - Registered User
- Use Cases:
  - Viết bình luận cho bài viết
  - Xem bình luận của bài viết
  - Thích (like) bài viết
# Giao diện từng trang 

# Hướng dẫn cài đặt, chạy

- cài đặc flask thông qua terminal bằng lệnh pip install flask
- chạy file app.py (truy cập đúng thư mục)
  hoặc
- chạy thông qua file install.zsh mà không cần gõ python app.py
  - cấp quyền chạy cho file: chmod +x install.zsh
  - chạy file:./install.zsh hoặc zsh install.zsh

# Link project đã triển khai

- deploy bằng render: https://flask-tinyapp-eju1.onrender.com 
- Khi deploy bằng render thì ảnh sẽ bị mất 
