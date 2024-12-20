from sqlalchemy import func, case, text
from datetime import datetime, timedelta
from sqlalchemy.orm import aliased
from app.config.infra.database import db
from app.appointment.model import Appointment
from app.patient.model import Patient
from app.util.response import Response


class DashboardService:

    def overview(self, g):
        user_id = g.user_id
        today = datetime.today()

        first_day_of_last_month = today - timedelta(days=30)
        last_day_of_last_month = today

        (total_appointments, mean_age, total_males, total_females) = (
            db.session.query(
                func.count(Appointment.appointment_id).label("total_appointments"),
                func.avg(text("TIMESTAMPDIFF(YEAR, patient.birth_date, NOW())")).label(
                    "mean_age"
                ),
                func.coalesce(
                    func.sum(case((Patient.gender == "M", 1), else_=0)), 0
                ).label("total_males"),
                func.coalesce(
                    func.sum(case((Patient.gender == "F", 1), else_=0)), 0
                ).label("total_females"),
            )
            .join(Patient, Patient.id == Appointment.patient_id)
            .filter(Appointment.date_entered >= first_day_of_last_month)
            .filter(Appointment.date_entered <= last_day_of_last_month)
            .filter(Appointment.user_id == user_id)
            .one()
        )

        return Response.ok(
            data={
                "total_appointments": total_appointments,
                "mean_age": int(mean_age),
                "total_males": total_males,
                "total_females": total_females,
            },
            message="Successfully returned dashboard overview",
        )

    def appointments_per_month(self, g):
        user_id = g.user_id

        today = datetime.today()
        start_date = today - timedelta(days=180)

        months = []
        current_date = start_date
        while current_date <= today:
            months.append((current_date.year, current_date.month))
            if current_date.month == 12:
                current_date = current_date.replace(
                    year=current_date.year + 1, month=1, day=1
                )
            else:
                current_date = current_date.replace(month=current_date.month + 1, day=1)

        results = (
            db.session.query(
                func.extract("year", Appointment.date_entered).label("year"),
                func.extract("month", Appointment.date_entered).label("month"),
                func.count(Appointment.appointment_id).label("appointments_count"),
            )
            .filter(Appointment.date_entered >= start_date)
            .filter(Appointment.user_id == user_id)
            .group_by("year", "month")
            .order_by("year", "month")
            .all()
        )

        appointments_by_month = {
            (int(r.year), int(r.month)): r.appointments_count for r in results
        }

        appointments_by_month_filled = {}
        for year, month in months:
            appointments_by_month_filled[f"{year}-{month:02d}"] = (
                appointments_by_month.get((year, month), 0)
            )

        months = []
        for month, count in appointments_by_month_filled.items():
            months.append({"period": month, "total": count})

        return Response.ok(
            data=months,
            message="Successfully returned appointments overview",
        )


    def appointment_calendar(self, g):
        today = datetime.today()
        first_day_of_current_month = today.replace(day=1)

        if today.month == 12:
            last_day_of_current_month = datetime(today.year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day_of_current_month = (first_day_of_current_month.replace(month=today.month + 1, day=1) - timedelta(days=1))

        days_in_month = []
        current_date = first_day_of_current_month
        while current_date <= last_day_of_current_month:
            days_in_month.append(current_date)

            current_date += timedelta(days=1)
            
            
        start_of_day = first_day_of_current_month
        end_of_day = last_day_of_current_month.replace(hour=23, minute=59, second=59)


        results = (
            db.session.query(
                func.date(Appointment.date_entered).label("date"),
                func.count(Appointment.appointment_id).label("appointments_count"),
            )
            .filter(Appointment.date_entered >= start_of_day)
            .filter(Appointment.date_entered <= end_of_day)
            .group_by(func.date(Appointment.date_entered))
            .order_by(func.date(Appointment.date_entered))
            .all()
        )


        appointments_by_day = {r.date.strftime("%Y-%m-%d"): r.appointments_count for r in results}

        appointments_by_day_filled = {}
        for day in days_in_month:
            appointments_by_day_filled[day.strftime("%Y-%m-%d")] = appointments_by_day.get(day.strftime("%Y-%m-%d"), 0)

        items = []
        for day, count in appointments_by_day_filled.items():
            items.append({
                "period": day,
                "count": count
            })
        
        return Response.ok(data=items, message="Sucessfully returned calendar!")