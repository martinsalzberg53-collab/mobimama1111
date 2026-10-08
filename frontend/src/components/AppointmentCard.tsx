import { useCallback, useEffect, useState } from "react";
import { Link } from "react-router-dom";
import API from "../api/axios";
import "../styles/MotherDashboard.css";

type NurseDetails = {
  name: string;
  registration_type: string;
  registration_number: string;
  phone_number: string;
};

type Appointment = {
  id: number;
  date_time: string;
  reason: string;
  status: "pending" | "approved" | "cancelled" | "completed";
  clinic_display: string;
  nurse_name: string;
  nurse_details: NurseDetails | null;
};

const UPCOMING_STATUSES: Appointment["status"][] = ["pending", "approved"];

// en-GB keeps day-month-year, which is the ordering used in Ghana.
const dateFormatter = new Intl.DateTimeFormat("en-GB", {
  weekday: "long",
  day: "numeric",
  month: "long",
  year: "numeric",
});

const timeFormatter = new Intl.DateTimeFormat("en-GB", {
  hour: "numeric",
  minute: "2-digit",
  hour12: true,
});

const AppointmentCard = () => {
  const [appointment, setAppointment] = useState<Appointment | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Soonest non-cancelled appointment that has not already happened.
  const pickNext = (list: Appointment[]) => {
    const now = Date.now();
    return (
      list
        .filter((item) => UPCOMING_STATUSES.includes(item.status))
        .filter((item) => new Date(item.date_time).getTime() >= now)
        .sort(
          (a, b) =>
            new Date(a.date_time).getTime() - new Date(b.date_time).getTime()
        )[0] ?? null
    );
  };

  const fetchAppointment = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await API.get<Appointment[]>(
        "/appointments/appointments/"
      );
      setAppointment(pickNext(response.data));
    } catch (err) {
      console.error(err);
      setError("Could not load your appointment. Please try again.");
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchAppointment();
  }, [fetchAppointment]);

  const isApproved = appointment?.status === "approved";
  const nurseLabel = appointment?.nurse_details
    ? `${appointment.nurse_details.registration_type} ${
        appointment.nurse_details.registration_number
      }`.trim()
    : "";

  return (
    <section className="dashboard-card appointment-card">
      <h2>Next Appointment</h2>

      {isLoading ? (
        <p className="loading-note">Loading appointment...</p>
      ) : error ? (
        <p className="notice notice-error">{error}</p>
      ) : appointment ? (
        <>
          <div className="appointment-details">
            <p className="appointment-date">
              {dateFormatter.format(new Date(appointment.date_time))}
            </p>
            <p className="appointment-time">
              {timeFormatter.format(new Date(appointment.date_time))}
            </p>
            <p className="appointment-location">
              {appointment.clinic_display || "Clinic to be confirmed"}
            </p>

            {isApproved && appointment.nurse_name ? (
              <p className="appointment-doctor">
                with {appointment.nurse_name}
              </p>
            ) : (
              <p className="loading-note">Awaiting nurse confirmation</p>
            )}
          </div>

          <div className="appointment-card-foot">
            <span className={`badge ${appointment.status}`}>
              {isApproved ? "Confirmed" : "Awaiting approval"}
            </span>

            {isApproved && nurseLabel && (
              <span className="badge neutral">{nurseLabel}</span>
            )}

            {isApproved && appointment.nurse_details?.phone_number && (
              <a
                className="appointment-call"
                href={`tel:${appointment.nurse_details.phone_number}`}
              >
                Call nurse
              </a>
            )}
          </div>
        </>
      ) : (
        <div className="appointment-empty">
          <p className="loading-note">Next appointment appears here.</p>
          <Link to="/motherappointments" className="btn btn-primary">
            Book an appointment
          </Link>
        </div>
      )}
    </section>
  );
};

export default AppointmentCard;
