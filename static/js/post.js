document.addEventListener("DOMContentLoaded", function () {
  loadApprovedPosts();
  const createButton = document.getElementById("create-post-btn");
  createButton.textContent = "Đăng bài";
  
  document.body.addEventListener("click", function(e) {
    if (e.target && e.target.id === "submit-post-btn") {
      submitPostHandler(e);
    }
    
    if (e.target && e.target.id === "create-post-btn") {
      document.getElementById("post-form").style.display = "block";
    }

    // Thêm bình luận
    if (e.target && e.target.classList.contains("submit-comment-btn")) {
      submitCommentHandler(e);
    }

    // Theo dõi bài viết
    if (e.target && e.target.classList.contains("follow-btn")) {
      followPostHandler(e);
    }

    // Xem danh sách bài viết đã theo dõi
    if (e.target && e.target.id === "view-followed-posts-btn") {
      loadFollowedPosts();
    }
  });
});

function followPostHandler(e) {
  const postId = e.target.dataset.postId;

  fetch("/api/posts/follow", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      post_id: postId,
      user_id: sessionStorage.getItem("userId") || "anonymous"
    })
  })
  .then((response) => response.json())
  .then((data) => {
    if (data.success) {
      alert("Bạn đã theo dõi bài viết!");
      e.target.classList.add("following"); // Thêm lớp "following" khi theo dõi
      e.target.textContent = "Đang theo dõi"; // Thay đổi nội dung nút
    } else {
      alert("Lỗi khi theo dõi bài viết.");
    }
  })
  .catch((error) => console.error("Lỗi khi theo dõi bài viết:", error));
}

function loadApprovedPosts() {
  fetch("/api/posts/approved")
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Lỗi HTTP: ${response.status}`);
      }
      return response.json();
    })
    .then((data) => {
      if (data.success) {
        let postList = document.getElementById("post-list");
        postList.innerHTML = "";

        data.approved_posts.forEach((post) => {
          let postDiv = document.createElement("div");
          postDiv.classList.add("post-item");

          postDiv.innerHTML = `
          <div class="add-follow">
            <button class="follow-btn" data-post-id="${post.id}">Theo dõi</button>
          </div>
          <h3>${post.title}</h3>
          <p>${post.body}</p>
          <h4>Bình Luận</h4>
          <div class="comments-container" id="comments-${post.id}"></div>
          <div class="add-comment">
            <textarea id="comment-text-${post.id}" placeholder="Viết bình luận..."></textarea>
            <button class="submit-comment-btn" data-post-id="${post.id}">Thêm bình luận</button>
          </div>
        `;

          postList.appendChild(postDiv);

          // Tải bình luận cho bài viết này
          loadComments(post.id);
        });
      } else {
        console.error("Lỗi tải danh sách bài viết:", data.message);
      }
    })
    .catch((error) => console.error("Lỗi khi tải bài viết:", error));
}

function loadFollowedPosts() {
  const userId = sessionStorage.getItem("userId") || "anonymous";

  fetch(`/api/posts/followed/${userId}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        let postList = document.getElementById("post-list");
        postList.innerHTML = "";

        data.followed_posts.forEach((post) => {
          let postDiv = document.createElement("div");
          postDiv.classList.add("post-item");

          postDiv.innerHTML = `
            <h3>${post.title}</h3>
            <p>${post.body}</p>
          `;

          postList.appendChild(postDiv);
        });
      } else {
        console.error("Lỗi tải danh sách bài viết đã theo dõi:", data.message);
      }
    })
    .catch((error) => console.error("Lỗi khi tải bài viết đã theo dõi:", error));
}

function loadComments(postId) {
  fetch(`/api/posts/comments/${postId}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.success) {
        let commentsContainer = document.getElementById(`comments-${postId}`);
        commentsContainer.innerHTML = "";

        data.comments.forEach((comment) => {
          let commentDiv = document.createElement("div");
          commentDiv.classList.add("comment-item");
          commentDiv.innerHTML = `
            <strong>${comment.user_id}</strong>: <p>${comment.content}</p>
          `;
          commentsContainer.appendChild(commentDiv);
        });
      } else {
        console.error("Lỗi tải bình luận:", data.message);
      }
    })
    .catch((error) => console.error("Lỗi khi tải bình luận:", error));
}

function submitCommentHandler(e) {
  const postId = e.target.dataset.postId;
  const commentText = document.getElementById(`comment-text-${postId}`).value;

  fetch("/api/posts/comments", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      post_id: postId,
      content: commentText
    })
  })
  .then((response) => response.json())
  .then((data) => {
    if (data.success) {
      alert("Bình luận đã được thêm.");
      loadComments(postId); // Tải lại bình luận sau khi thêm thành công
      document.getElementById(`comment-text-${postId}`).value = ""; // Xóa nội dung textarea
    } else {
      alert("Lỗi: " + data.message);
    }
  })
  .catch((error) => console.error("Lỗi khi thêm bình luận:", error));
}

function submitPostHandler(event) {
  event.preventDefault();
  const title = document.getElementById("post-title").value;
  const body = document.getElementById("post-body").value;
  const userId = sessionStorage.getItem("userId") || "anonymous";
  
  fetch("/api/posts/create", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ userId, title, body })
  })
  .then((response) => response.json())
  .then((data) => {
    if (data.success) {
      alert("Bài viết đã được gửi thành công.");
      document.getElementById("post-form").style.display = "none";
      document.getElementById("post-title").value = "";
      document.getElementById("post-body").value = "";
      loadApprovedPosts();
    } else {
      alert("Lỗi: " + data.message);
    }
  })
  .catch((error) => console.error("Lỗi khi đăng bài:", error));
}
