from flask import Blueprint, render_template, redirect, session
from utils.db import plans, subscriptions, payments

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required():
    return "role" in session and session["role"] == "admin"


@admin_bp.route("/dashboard")
def dashboard():
    if not admin_required():
        return redirect("/")

    # ✅ TOTAL PLANS
    total_plans = plans.count_documents({})

    # ✅ ACTIVE SUBSCRIPTIONS (DISTINCT USERS)
    active_users = subscriptions.distinct(
        "user_email",
        {"status": "Active"}
    )
    active_subs = len(active_users)

    # ✅ TOTAL REVENUE (ONLY PAID PAYMENTS)
    revenue_cursor = payments.find({"status": "Paid"})
    total_revenue = sum(p["amount"] for p in revenue_cursor)

    return render_template(
        "admin_dashboard.html",
        total_plans=total_plans,
        active_subs=active_subs,
        total_revenue=total_revenue
    )
