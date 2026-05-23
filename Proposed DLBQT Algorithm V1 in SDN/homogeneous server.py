"""
Original algorithm design:
Dr. Maghrib A. M. Alrammahi
Mohammed Fadhil Mohammed 

decision logic, and methodological formulation
presented in this file were originally developed by Dr. Maghrib A. M. Alrammahi and Mohammed Fadhil Mohammed.
This implementation documents the proposed model for research transparency
and reproducibility.

Unauthorized removal of this attribution is not permitted.
""" 

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import os
import argparse

# مجلد التحميل
UPLOAD_DIR = "uploads"

# التأكد من أن مجلد التحميل موجود
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

class CustomHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """التعامل مع طلبات GET لتنزيل الملفات"""
        try:
            file_name = os.path.basename(self.path.lstrip("/"))  # تأمين المسار
            file_path = os.path.join(UPLOAD_DIR, file_name)

            if not os.path.exists(file_path):
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"File not found.")
                return

            file_size = os.path.getsize(file_path)

            # إرسال الهيدر مع معلومات الملف
            self.send_response(200)
            self.send_header('Content-Type', 'application/octet-stream')
            self.send_header('Content-Disposition', f'attachment; filename="{file_name}"')
            self.send_header("Content-Length", str(file_size))
            self.end_headers()

            # إرسال محتوى الملف بكفاءة
            with open(file_path, "rb") as f:
                self.wfile.write(f.read())

        except Exception as e:
            print(f"Error handling GET request: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Error handling GET request.")

    def do_POST(self):
        """التعامل مع طلبات POST لرفع الملفات"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length <= 0:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"Invalid file upload request.")
                return

            post_data = self.rfile.read(content_length)

            filename = "uploaded_file.bin"
            if "Content-Disposition" in self.headers:
                header = self.headers['Content-Disposition']
                parts = header.split(";")
                for part in parts:
                    part = part.strip()
                    if part.startswith("filename="):
                        filename = part.split("=")[1].strip('"')

            # تأمين اسم الملف
            filename = os.path.basename(filename)
            file_path = os.path.join(UPLOAD_DIR, filename)

            with open(file_path, "wb") as f:
                f.write(post_data)
                print(f"Saved file: {file_path}")

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"File uploaded successfully.")

        except Exception as e:
            print(f"Error handling POST request: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Error handling POST request.")

def run_server(address, port):
    server_address = (address, port)
    httpd = ThreadingHTTPServer(server_address, CustomHTTPRequestHandler)
    print(f"Multi-threaded HTTP Server running on {address}:{port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server.")
        httpd.server_close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a multi-threaded HTTP server.")
    parser.add_argument("--address", type=str, default="0.0.0.0", help="IP address to bind the server to.")
    parser.add_argument("--port", type=int, default=80, help="Port to run the server on.")
    args = parser.parse_args()
    run_server(args.address, args.port)
