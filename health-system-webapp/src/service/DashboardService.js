import { del, get, post, put } from "./BaseService";

export const getOverview = async () => {
  const response = await get({
    url: `/v1/dashboard/overview`,
  });
  return response.data.data;
};

export const getAppointmentsPerMonth = async () => {
  const response = await get({
    url: `/v1/dashboard/appointment-per-month`,
  });
  return response.data.data;
};

export const getAppointmentCalendar = async () => {
  const response = await get({
    url: `/v1/dashboard/appointment-calendar`,
  });
  return response.data.data;
};
