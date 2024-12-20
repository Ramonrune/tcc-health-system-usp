from flask import Blueprint, request, g
from flask_pydantic import validate
from app.config.infra.jwt import require_token
from app.dashboard.service import DashboardService

dashboard_service = DashboardService()

dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/v1/dashboard/overview", methods=["GET"])
@validate()
@require_token
def overview():
    return dashboard_service.overview(g)


@dashboard.route("/v1/dashboard/appointment-per-month", methods=["GET"])
@validate()
@require_token
def appointments_per_month():
    return dashboard_service.appointments_per_month(g)

@dashboard.route("/v1/dashboard/appointment-calendar", methods=["GET"])
@validate()
@require_token
def appointment_calendar():
    return dashboard_service.appointment_calendar(g)