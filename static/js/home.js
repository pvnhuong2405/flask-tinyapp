document.addEventListener("DOMContentLoaded", function () {
  fetch("/api/auth/status")
    .then((response) => response.json())
    .then((data) => {
      const userSection = document.getElementById("user-section");

      if (data.logged_in) {
        if (data.role === "admin") {
          setTimeout(() => (window.location.href = "/admin"), 1000);
        } else {
          userSection.innerHTML = `
            <div class="user-info">
              <span>Xin chào, ${data.username}!</span>
              <button class="logout-btn" onclick="logout()">Đăng xuất</button>
            </div>
          `;
        }
      } else {
        userSection.innerHTML = `
          <a href="/login" class="login-btn">Đăng nhập</a> |
          <a href="/register" class="signup-btn">Đăng ký</a>
        `;
      }
    })
    .catch((error) => {
      console.error("Lỗi kiểm tra trạng thái đăng nhập:", error);
      document.getElementById("user-section").innerHTML =
        '<span style="color: red;">Lỗi kết nối</span>';
    });
});

function logout() {
  fetch("/api/auth/logout", { method: "POST" })
    .then(() => {
      sessionStorage.clear(); // Xóa session trên trình duyệt
      window.location.href = "/"; // Quay về trang chủ
    })
    .catch((error) => console.error("Lỗi khi đăng xuất:", error));
}
