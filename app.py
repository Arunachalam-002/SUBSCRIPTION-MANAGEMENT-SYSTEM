from flask import Flask, render_template, session, redirect
from config import SECRET_KEY

from routes.auth_routes import auth_bp
from routes.plan_routes import plan_bp
from routes.subscription_routes import subscription_bp

from models.user_model import find_user_by_email
from models.plan_model import get_all_plans

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(plan_bp)
app.register_blueprint(subscription_bp)

# ---------------- ADMIN DASHBOARD ----------------
@app.route("/admin/dashboard")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect("/")

    plans = get_all_plans()
    return render_template("admin_dashboard.html", plans=plans)

# ---------------- CLIENT DASHBOARD ----------------
@app.route("/client/dashboard")
def client_dashboard():
    if session.get("role") != "client":
        return redirect("/")

    user = find_user_by_email(session["user_email"])
    plans = get_all_plans()

    return render_template(
        "client_dashboard.html",
        wallet=user["wallet_balance"],
        plans=plans
    )

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
 