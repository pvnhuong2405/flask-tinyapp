document.addEventListener("DOMContentLoaded", async function () {
  const postsList = document.getElementById("posts-list");
  const pagination = document.getElementById("pagination");
  const postsPerPageInput = document.getElementById("posts-per-page");
  
  let posts = [];
  let currentPage = 1;
  let postsPerPage = parseInt(postsPerPageInput.value);  // Số bài mỗi trang (mặc định là 10)

  // Hàm tải tất cả bài viết
  async function loadPosts() {
    try {
      const response = await fetch("/api/admin/all_posts");

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      
      const data = await response.json();

      if (!data.success) {
        throw new Error(data.message || "Failed to load posts");
      }

      posts = data.posts;  // Lưu lại tất cả các bài viết
      displayPosts(currentPage);  // Hiển thị bài viết cho trang hiện tại
      createPagination();  // Tạo phân trang
    } catch (error) {
      console.error("Lỗi khi tải bài viết:", error);
      postsList.innerHTML = `
        <tr>
          <td colspan="7" class="error-message">
            Không thể tải danh sách bài viết. Vui lòng thử lại sau.
          </td>
        </tr>
      `;
    }
  }

  // Hàm hiển thị bài viết cho một trang cụ thể
  function displayPosts(page) {
    const startIndex = (page - 1) * postsPerPage;
    const endIndex = startIndex + postsPerPage;
    const postsToDisplay = posts.slice(startIndex, endIndex);
    
    postsList.innerHTML = "";  // Reset lại danh sách bài viết

    postsToDisplay.forEach((post) => {
      const statusText = post.is_approved ? "Đã duyệt" : "Chưa duyệt";
      const statusBtnText = post.is_approved ? "Ẩn bài" : "Duyệt bài";
      const statusClass = post.is_approved ? "approved" : "pending";

      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${post.id}</td>
        <td>${post.title}</td>
        <td>${post.body}</td>
        <td>${post.userId}</td>
        <td class="status ${statusClass}">${statusText}</td>
        <td>
          <button class="toggle-status-btn" data-post-id="${post.id}" data-current-status="${post.is_approved}">
            ${statusBtnText}
          </button>
        </td>
        <td>
          <button class="delete-btn" data-post-id="${post.id}">Xóa</button>
        </td>
      `;
      postsList.appendChild(row);
    });

    // Gắn sự kiện click cho các nút Duyệt bài và Xóa bài
    addEventListeners();
  }

  function addEventListeners() {
    // Lắng nghe sự kiện Duyệt bài
    const toggleStatusButtons = document.querySelectorAll('.toggle-status-btn');
    toggleStatusButtons.forEach(button => {
      button.addEventListener('click', async function() {
        const postId = this.getAttribute('data-post-id');
        const currentStatus = this.getAttribute('data-current-status') === 'true';
        const newStatus = !currentStatus;

        try {
          const response = await fetch(`/api/admin/update_post_status/${postId}`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ is_approved: newStatus })
          });

          const data = await response.json();

          if (data.success) {
            alert(data.message);
            loadPosts();  // Tải lại danh sách bài viết
          } else {
            alert('Có lỗi khi duyệt bài.');
          }
        } catch (error) {
          console.error('Lỗi khi duyệt bài:', error);
        }
      });
    });

    // Lắng nghe sự kiện Xóa bài
    const deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach(button => {
      button.addEventListener('click', async function() {
        const postId = this.getAttribute('data-post-id');

        if (confirm("Bạn chắc chắn muốn xóa bài viết này?")) {
          try {
            const response = await fetch(`/api/admin/delete_post/${postId}`, {
              method: 'DELETE'
            });

            const data = await response.json();

            if (data.success) {
              alert(data.message);
              loadPosts();  // Tải lại danh sách bài viết
            } else {
              alert('Có lỗi khi xóa bài viết.');
            }
          } catch (error) {
            console.error('Lỗi khi xóa bài viết:', error);
          }
        }
      });
    });
  }

  // Hàm tạo phân trang
  function createPagination() {
    const totalPages = Math.ceil(posts.length / postsPerPage);  // Tính tổng số trang
    pagination.innerHTML = "";  // Reset phân trang

    for (let page = 1; page <= totalPages; page++) {
      const button = document.createElement("button");
      button.textContent = page;
      button.className = page === currentPage ? "active" : "";
      button.addEventListener("click", () => {
        currentPage = page;  // Cập nhật trang hiện tại
        displayPosts(currentPage);  // Hiển thị bài viết cho trang mới
        createPagination();  // Tạo lại các nút phân trang
      });
      pagination.appendChild(button);
    }
  }

  // Lắng nghe sự kiện thay đổi số bài mỗi trang
  postsPerPageInput.addEventListener("input", () => {
    postsPerPage = parseInt(postsPerPageInput.value);
    currentPage = 1; 
    displayPosts(currentPage);
    createPagination();
  });

  loadPosts();
});
