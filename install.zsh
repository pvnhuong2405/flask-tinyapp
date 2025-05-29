#!/bin/zsh

echo "🔧 Bắt đầu chạy ứng dụng Flask..."

# Kiểm tra xem Python đã cài chưa
if ! command -v python3 &> /dev/null; then
    echo "⚠️  Python chưa được cài đặt, vui lòng cài đặt trước!"
    exit 1
fi

# Chạy file app.py
echo "🚀 Đang chạy Flask app..."
python3 app.py

echo "✅ Ứng dụng Flask đã chạy xong!"
