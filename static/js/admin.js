document.addEventListener("DOMContentLoaded", function () {
  fetch("/api/admin/users") // Gửi request để lấy danh sách người dùng
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        const userTable = document.getElementById("user-table");
        userTable.innerHTML = "";

        data.users.forEach((user) => {
          const row = document.createElement("tr");
          row.innerHTML = `
              <td>${user.id}</td>
              <td>${user.email}</td> 
              <td>
                  <select class="role-select" data-user-email="${user.email}">
                      <option value="user" ${
                        user.role === "user" ? "selected" : ""
                      }>User</option>
                      <option value="admin" ${
                        user.role === "admin" ? "selected" : ""
                      }>Admin</option>
                  </select>
              </td>
              <td>
                  <button class="block-user" data-user-email="${user.email}">
                      ${user.is_blocked ? "Unblock" : "Block"}
                  </button>
                  <button class="reset-password" data-user-email="${
                    user.email
                  }">Reset Password</button>
              </td>
          `;
          userTable.appendChild(row);
        });

        // Xử lý sự kiện khóa/mở khóa user
        document.querySelectorAll(".block-user").forEach((button) => {
          button.addEventListener("click", function () {
            const userEmail = this.dataset.userEmail;
            fetch(`/api/admin/block_user/${userEmail}`, { method: "POST" })
              .then((response) => response.json())
              .then((data) => {
                alert(data.message);
                location.reload();
              });
          });
        });

        document.querySelectorAll(".reset-password").forEach((button) => {
          button.addEventListener("click", function () {
            const userEmail = this.dataset.userEmail;
            print("jkhkjhkjhk")
            // Hiển thị hộp thoại nhập mật khẩu mới
            const newPassword = prompt(`Nhập mật khẩu mới cho ${userEmail}:`, "");
            
            // Kiểm tra nếu người dùng đã nhập mật khẩu
            if (newPassword !== null && newPassword.trim() !== "") {
              // Gửi yêu cầu đặt lại mật khẩu với mật khẩu mới
              fetch(`/api/admin/reset_password/${userEmail}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ password: newPassword }),
              })
                .then((response) => response.json())
                .then((data) => {
                  alert(data.message);
                })
                .catch((error) => {
                  console.error("Lỗi khi đặt lại mật khẩu:", error);
                  alert("Đã xảy ra lỗi khi đặt lại mật khẩu");
                });
            } else if (newPassword !== null) {
              alert("Mật khẩu không được để trống");
            }
          });
        });

        // Xử lý sự kiện thay đổi vai trò user
        document.querySelectorAll(".role-select").forEach((select) => {
          select.addEventListener("change", function () {
            const userEmail = this.dataset.userEmail;
            const newRole = this.value;

            fetch(`/api/admin/set_role/${userEmail}`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ role: newRole }),
            })
              .then((response) => response.json())
              .then((data) => {
                alert(data.message);
              });
          });
        });
      } else {
        console.error("Lỗi tải danh sách user:", data.message);
      }
    })
    .catch((error) => console.error("Lỗi khi tải user:", error));
});
function logout() {
  fetch("/api/auth/logout", { method: "POST" })
    .then(() => {
      sessionStorage.clear(); // Xóa thông tin user khỏi trình duyệt
      window.location.href = "/";
    })
    .catch((error) => console.error("Error logging out:", error));
}
