from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from flask_cors import CORS
import sqlite3

app = Flask(__name__)

app.secret_key = "supersecretkey"
CORS(app)

# Khởi tạo database
DATABASE = "database.db"

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        # Tạo bảng users nếu chưa tồn tại
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL,
                is_blocked BOOLEAN NOT NULL
            )
        """)

        # Kiểm tra xem admin đã tồn tại chưa trước khi thêm
        cursor.execute("SELECT email FROM users WHERE email = 'bongthui812@gmail.com'")
        if cursor.fetchone() is None:
            cursor.execute("""
                INSERT INTO users (email, password, role, is_blocked)
                VALUES ('bongthui812@gmail.com', '1234', 'admin', 0)
            """)

        # Tạo bảng posts nếu chưa tồn tại
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                userId TEXT NOT NULL,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                is_approved BOOLEAN NOT NULL,
                FOREIGN KEY (userId) REFERENCES users(email)
            )
        """)

        # Kiểm tra xem dữ liệu mẫu đã tồn tại chưa trước khi thêm
        cursor.execute("SELECT id FROM posts WHERE title = 'Trách nhiệm và hậu quả'")
        if cursor.fetchone() is None:
            cursor.execute("""
                INSERT INTO posts (userId, title, body, is_approved)
                VALUES ('bongthui812@gmail.com', 'Trách nhiệm và hậu quả', 
                    'Vì lợi ích và trách nhiệm\nTrách nhiệm từ chối hậu quả một cách nhanh chóng và cùng nhau\nChịu trách nhiệm về những tổn thất xảy ra\nMọi thứ đều là của chúng tôi nhưng chúng là những điều tồn tại và tạo nên kiến trúc',1)
            """)

        # Tạo bảng comments nếu chưa tồn tại
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER NOT NULL,
                user_id TEXT NOT NULL,
                content TEXT NOT NULL
            )
        """)

        # Thêm dữ liệu mẫu vào bảng comments
        cursor.execute("SELECT id FROM comments WHERE content = 'Bài viết rất hay!'")
        if cursor.fetchone() is None:
            cursor.execute("""
                INSERT INTO comments (post_id, user_id, content)
                VALUES 
                    (1, 'bongthui812@gmail.com', 'Bài viết rất hay!'),
                    (1, 'bongthui812@gmail.com', 'Cảm ơn bạn đã chia sẻ bài viết này, rất bổ ích.'),
                    (1, 'bongthui812@gmail.com', 'Mình hoàn toàn đồng ý với quan điểm trong bài viết này.')
            """)

        # Tạo bảng followposts nếu chưa tồn tại, không cần khóa ngoại
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS followposts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id INTEGER NOT NULL,
                user_id TEXT NOT NULL
            )
        """)

        # Thêm dữ liệu mẫu vào bảng followposts (người dùng 'bongthui812@gmail.com' theo dõi bài viết có id = 1)
        cursor.execute("SELECT id FROM followposts WHERE post_id = 1 AND user_id = 'bongthui812@gmail.com'")
        if cursor.fetchone() is None:
            cursor.execute("""
                INSERT INTO followposts (post_id, user_id)
                VALUES 
                    (1, 'bongthui812@gmail.com')
            """)

        conn.commit()

init_db()

# -------------------- ROUTE HIỂN THỊ TRANG HTML --------------------

@app.route("/")
def home_dangnhap():
    return render_template("home_dangnhap.html")

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route('/register')
def register_page():
    return render_template("register.html")


@app.route("/admin")
def admin():
    if "user" not in session or session.get("role") != "admin":
        return redirect(url_for("login_page"))
    return render_template("admin.html")
@app.route("/post")
def post():
    return render_template("post.html")
@app.route("/post_next")
def post_next():
    return render_template("post_next.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")
@app.route("/manager_post")
def manager_post():
    return render_template("manager_post.html")
# -------------------- API ĐĂNG KÝ & ĐĂNG NHẬP --------------------

@app.route("/api/auth/register", methods=["POST"])
def register_api():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            return jsonify({"success": False, "message": "Email đã tồn tại!"}), 400
        
        cursor.execute("INSERT INTO users (email, password, role, is_blocked) VALUES (?, ?, ?, ?)",
                       (email, password, "user", False))
        conn.commit()
    
    return jsonify({"success": True, "message": "Đăng ký thành công!"})

@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")
    
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT password, role, is_blocked FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
    
    if user:
        stored_password, role, is_blocked = user
        if is_blocked:
            return jsonify({"success": False, "message": "Tài khoản của bạn đã bị khóa!"}), 403
        if stored_password == password:
            session["user"] = email
            session["role"] = role
            redirect_url = "/admin" if role == "admin" else "/"
            return jsonify({"success": True, "role": role, "redirect": redirect_url})
    
    return jsonify({"success": False, "message": "Sai email hoặc mật khẩu!"}), 401

@app.route("/api/auth/status", methods=["GET"])
def auth_status():
    if "user" in session:
        return jsonify({
            "logged_in": True,
            "username": session["user"],
            "role": session["role"]
        })
    return jsonify({"logged_in": False})

@app.route("/api/auth/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"success": True})

# -------------------- API QUẢN LÝ ADMIN --------------------

@app.route("/api/admin/users", methods=["GET"])
def get_users():
    if "user" not in session or session.get("role") != "admin":
        return jsonify({"success": False, "message": "Unauthorized"}), 403
    
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, email, role, is_blocked FROM users")
        user_list = [{"id": user_id,"email": email, "role": role, "is_blocked": is_blocked} for user_id, email, role, is_blocked in cursor.fetchall()]
    
    return jsonify({"success": True, "users": user_list})

@app.route("/api/admin/block_user/<email>", methods=["POST"])
def block_user(email):
    if "user" not in session or session.get("role") != "admin":
        return jsonify({"success": False, "message": "Unauthorized"}), 403
    
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT is_blocked FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        if not user:
            return jsonify({"success": False, "message": "Không tìm thấy người dùng."}), 404
        
        new_status = not user[0]
        cursor.execute("UPDATE users SET is_blocked = ? WHERE email = ?", (new_status, email))
        conn.commit()
        status = "blocked" if new_status else "unblocked"
        return jsonify({"success": True, "message": f"Tài khoản {email} đã được {status}."})
    
# -------------------- API SET ROLE --------------------
@app.route("/api/admin/set_role/<email>", methods=["POST"])
def set_role(email):
    if "user" not in session or session.get("role") != "admin":
        return jsonify({"success": False, "message": "Unauthorized"}), 403
    
    data = request.json
    new_role = data.get("role")
    
    if new_role not in ["user", "admin"]:
        return jsonify({"success": False, "message": "Vai trò không hợp lệ"}), 400
    
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"success": False, "message": "Không tìm thấy người dùng"}), 404
        
        cursor.execute("UPDATE users SET role = ? WHERE email = ?", (new_role, email))
        conn.commit()
        
        return jsonify({
            "success": True, 
            "message": f"Đã cập nhật vai trò của {email} thành {new_role}"
        })
    
@app.route("/api/admin/reset_password/<email>", methods=["POST"])
def reset_password(email):
    # Kiểm tra quyền admin
    if "user" not in session or session.get("role") != "admin":
        return jsonify({"success": False, "message": "Unauthorized"}), 403
    
    data = request.json
    new_password = data.get("password")
    
    if not new_password or not isinstance(new_password, str) or len(new_password.strip()) == 0:
        return jsonify({"success": False, "message": "Mật khẩu không hợp lệ"}), 400
    
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        
        cursor.execute("SELECT email FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()
        
        if not user:
            return jsonify({"success": False, "message": "Không tìm thấy người dùng"}), 404
        
        # Cập nhật mật khẩu đã được hash
        cursor.execute("UPDATE users SET password = ? WHERE email = ?", (new_password, email))
        conn.commit()
        
        return jsonify({
            "success": True, 
            "message": f"Đã đặt lại mật khẩu cho {email}"
        })
    
# -------------------- API POST --------------------

@app.route("/api/admin/posts/pending", methods=["GET"])
def get_pending_posts():
    if "user" not in session or session.get("role") != "admin":
        return jsonify({"success": False, "message": "Unauthorized"}), 403
    
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, userId, title, body FROM posts WHERE is_approved = 0")
        pending_posts = [
            {"id": post_id, "userId": user_id, "title": title, "body": body}
            for post_id, user_id, title, body in cursor.fetchall()
        ]
    
    return jsonify({"success": True, "pending_posts": pending_posts})

@app.route("/api/posts/approved", methods=["GET"])
def get_approved_posts():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, userId, title, body FROM posts WHERE is_approved = 1")
        approved_posts = [
            {"id": post_id, "userId": user_id, "title": title, "body": body}
            for post_id, user_id, title, body in cursor.fetchall()
        ]
    
    return jsonify({"success": True, "approved_posts": approved_posts})


@app.route("/api/posts/create", methods=["POST"])
def create_post():
    if "user" not in session:
        return jsonify({"success": False, "message": "Bạn cần đăng nhập để đăng bài."}), 403
    
    data = request.json
    user_id = data.get("userId")
    title = data.get("title")
    body = data.get("body")
    
    print("user_id:", user_id)
    print("title:", title)
    print("body:", body)
        
    if not user_id or not title or not body:
        return jsonify({"success": False, "message": "Thiếu thông tin bài viết."}), 400
    
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO posts (userId, title, body, is_approved) VALUES (?, ?, ?, ?)",
            (user_id, title, body, 0)  # is_approved = 0 (chưa duyệt)
        )
        conn.commit()
    
    return jsonify({"success": True, "message": "Bài viết đã được gửi và đang chờ duyệt."})

@app.route("/api/admin/all_posts", methods=["GET"])
def get_all_posts():
    if "user" not in session or session.get("role") != "admin":
        return jsonify({"success": False, "message": "Unauthorized"}), 403
    
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, userId, title, body, is_approved FROM posts")
        posts = [
            {
                "id": post_id,
                "userId": user_id,
                "title": title,
                "body": body,
                "is_approved": bool(is_approved)
            }
            for post_id, user_id, title, body, is_approved in cursor.fetchall()
        ]
    
    return jsonify({"success": True, "posts": posts})

# API để cập nhật trạng thái bài viết
@app.route("/api/admin/update_post_status/<int:post_id>", methods=["POST"])
def update_post_status(post_id):
    if "user" not in session or session.get("role") != "admin":
        return jsonify({"success": False, "message": "Unauthorized"}), 403
    
    data = request.json
    is_approved = data.get("is_approved")
    
    if is_approved is None:
        return jsonify({"success": False, "message": "Missing is_approved parameter"}), 400
    
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM posts WHERE id = ?", (post_id,))
        post = cursor.fetchone()
        
        if not post:
            return jsonify({"success": False, "message": "Không tìm thấy bài viết"}), 404
        
        cursor.execute("UPDATE posts SET is_approved = ? WHERE id = ?", (is_approved, post_id))
        conn.commit()
        
        status_text = "được duyệt" if is_approved else "bị ẩn"
        return jsonify({
            "success": True, 
            "message": f"Bài viết #{post_id} đã {status_text}"
        })

# API để xóa bài viết
@app.route("/api/admin/delete_post/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    if "user" not in session or session.get("role") != "admin":
        return jsonify({"success": False, "message": "Unauthorized"}), 403
    
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM posts WHERE id = ?", (post_id,))
        post = cursor.fetchone()
        
        if not post:
            return jsonify({"success": False, "message": "Không tìm thấy bài viết"}), 404
        
        cursor.execute("DELETE FROM posts WHERE id = ?", (post_id,))
        conn.commit()
        
        return jsonify({
            "success": True, 
            "message": f"Bài viết #{post_id} đã được xóa"
        })

# API để lấy bình luận của một bài viết
@app.route("/api/posts/comments/<int:post_id>", methods=["GET"])
def get_comments(post_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, user_id, content FROM comments WHERE post_id = ?", (post_id,))
        comments = [{"id": comment_id, "user_id": user_id, "content": content} for comment_id, user_id, content in cursor.fetchall()]

    return jsonify({"success": True, "comments": comments})


# API để thêm bình luận vào bài viết
@app.route("/api/posts/comments", methods=["POST"])
def add_comment():
    if "user" not in session:
        return jsonify({"success": False, "message": "Bạn cần đăng nhập để bình luận."}), 403
    
    data = request.json
    post_id = data.get("post_id")
    user_id = session["user"]
    content = data.get("content")
    
    if not post_id or not content:
        return jsonify({"success": False, "message": "Thiếu thông tin bài viết hoặc nội dung bình luận."}), 400
    
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO comments (post_id, user_id, content) VALUES (?, ?, ?)", (post_id, user_id, content))
        conn.commit()

    return jsonify({"success": True, "message": "Bình luận đã được thêm."})

# -------------------- API FOLLOW --------------------

@app.route("/api/posts/follow", methods=["POST"])
def follow_post():
    if "user" not in session:
        return jsonify({"success": False, "message": "Bạn cần đăng nhập để theo dõi bài viết."}), 403

    data = request.json
    post_id = data.get("post_id")
    user_id = data.get("user_id")

    if not post_id or not user_id:
        return jsonify({"success": False, "message": "Thiếu thông tin bài viết hoặc người dùng."}), 400

    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()

        # Kiểm tra xem người dùng đã theo dõi bài viết này chưa
        cursor.execute("SELECT * FROM followposts WHERE post_id = ? AND user_id = ?", (post_id, user_id))
        if cursor.fetchone():
            return jsonify({"success": False, "message": "Bạn đã theo dõi bài viết này rồi."}), 400

        # Thêm người dùng vào bảng followposts để theo dõi bài viết
        cursor.execute("INSERT INTO followposts (post_id, user_id) VALUES (?, ?)", (post_id, user_id))
        conn.commit()

    return jsonify({"success": True, "message": "Đã theo dõi bài viết!"})

@app.route("/api/posts/followed/<user_id>", methods=["GET"])
def get_followed_posts(user_id):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT posts.id, posts.userId, posts.title, posts.body
            FROM posts
            JOIN followposts ON posts.id = followposts.post_id
            WHERE followposts.user_id = ?
        """, (user_id,))
        
        followed_posts = [
            {"id": post_id, "userId": user_id, "title": title, "body": body}
            for post_id, user_id, title, body in cursor.fetchall()
        ]
    
    return jsonify({"success": True, "followed_posts": followed_posts})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
