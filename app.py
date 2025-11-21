from flask import Flask, render_template, request, redirect, url_for, session, flash
import sys
from db import init_db, find_user
from auth import register_user, authenticate_user
from mail import new_alias_for_user, send_message, get_inbox, get_message_detail, decrypt_message_id, decrypt_attachment
import bleach
from address import build_address
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

init_db()

@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        local = request.form.get("local", "").strip()
        password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()
        if not local or not password:
            flash("Local name and password required", "error")
            return render_template("register.html")
        if confirm_password and password != confirm_password:
            flash("Passwords do not match!", "error")
            return render_template("register.html")
        existing = find_user(local)
        try:
            register_user(local, password)
            if existing and not existing[2]:
                flash(f"Password set for existing user {local}. You can now login.", "success")
            else:
                flash(f"User {local} registered successfully! You can now login.", "success")
            return redirect(url_for("login"))
        except ValueError as e:
            flash(str(e), "error")
    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        local = request.form.get("local", "").strip()
        password = request.form.get("password", "")
        raw_len = len(password)
        password = password.strip()
        if not local or not password:
            flash("Username and password required", "error")
            return render_template("login.html")
        ok = authenticate_user(local, password)
        print(f"[DEBUG] LOGIN attempt user='{local}' raw_len={raw_len} stripped_len={len(password)} success={ok}", file=sys.stderr)
        if ok:
            session["user"] = local
            flash("Login successful!", "success")
            return redirect(url_for("dashboard"))
        user = find_user(local)
        if not user:
            flash(f"User '{local}' not found. Please register first.", "error")
        elif user and not user[2]:
            flash("No password set for this user. Use Register to set one.", "error")
        else:
            flash("Invalid password. Please try again.", "error")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Logged out", "info")
    return redirect(url_for("login"))

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    user_local = session["user"]
    primary_address = build_address(user_local)
    return render_template("dashboard.html", user=user_local, primary_address=primary_address)

@app.route("/alias", methods=["POST"])
def alias():
    if "user" not in session:
        return redirect(url_for("login"))
    user_local = session["user"]
    try:
        new_addr = new_alias_for_user(user_local)
        flash(f"New alias created: {new_addr}", "success")
    except Exception as e:
        flash(str(e), "error")
    return redirect(url_for("dashboard"))

@app.route("/send", methods=["GET", "POST"])
def send():
    if "user" not in session:
        return redirect(url_for("login"))
    user_local = session["user"]
    if request.method == "POST":
        recipient = request.form.get("recipient", "").strip()
        raw_html = request.form.get("rich_html", "").strip()
        message_plain = request.form.get("message", "").strip()
        content = raw_html if raw_html else message_plain
        if raw_html:
            # sanitize HTML
            allowed_tags = bleach.sanitizer.ALLOWED_TAGS + ["p","span","div","br","strong","em","u","ul","ol","li","blockquote","code","pre"]
            content = bleach.clean(raw_html, tags=allowed_tags, strip=True)
        if not recipient or not content:
            flash("Recipient and message required", "error")
            return render_template("send.html", user=user_local)
        try:
            # attachments handling
            attachments = []
            if 'attachments' in request.files:
                files = request.files.getlist('attachments')
                for f in files:
                    if f and f.filename:
                        data = f.read()
                        attachments.append({"filename": f.filename, "mime_type": f.mimetype or "application/octet-stream", "data_bytes": data})
            result = send_message(user_local, recipient, content, attachments=attachments)
            flash(f"Message sent! ID: {result['message_id']}", "success")
            return redirect(url_for("dashboard"))
        except Exception as e:
            flash(str(e), "error")
    return render_template("send.html", user=user_local)

@app.route("/inbox")
def inbox():
    if "user" not in session:
        return redirect(url_for("login"))
    user_local = session["user"]
    try:
        messages = get_inbox(user_local)
        return render_template("inbox.html", user=user_local, messages=messages)
    except Exception as e:
        flash(str(e), "error")
        return redirect(url_for("dashboard"))

@app.route("/message/<int:mid>")
def message_detail(mid):
    if "user" not in session:
        return redirect(url_for("login"))
    try:
        detail = get_message_detail(mid)
        plaintext = decrypt_message_id(mid)
        return render_template("message.html", detail=detail, plaintext=plaintext)
    except Exception as e:
        flash(str(e), "error")
        return redirect(url_for("inbox"))

@app.route('/attachment/<int:aid>')
def attachment_download(aid):
    if "user" not in session:
        return redirect(url_for("login"))
    try:
        att = decrypt_attachment(aid)
        from flask import Response
        return Response(att['data'], headers={"Content-Disposition": f"attachment; filename={att['filename']}", "Content-Type": att['mime_type']})
    except Exception as e:
        flash(str(e), "error")
        return redirect(url_for('inbox'))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
