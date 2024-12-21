import { calculateAge } from "src/util/date";
import { del, get, post, put } from "./BaseService";

export const getAppointments = async ({ start_date, end_date }) => {
  const response = await get({
    url: `/v1/appointment?start_date=${start_date}&end_date=${end_date}`,
  });

  return response.data.data.map((e) => {
    return {
      ...e,
      age: calculateAge(e.birth_date),
    };
  });
};

export const register = async ({ patient_id, annotation }) => {
  const response = await post({
    url: "/v1/appointment",
    body: { patient_id, annotation },
  });

  return response.status === 201;
};

export const update = async ({ id, patient_id, annotation }) => {
  const response = await put({
    url: `/v1/appointment/${id}`,
    body: { patient_id, annotation },
  });

  return response.status === 200;
};

export const remove = async ({ id }) => {
  const response = await del({
    url: `/v1/appointment/${id}`,
    body: {},
  });

  return response.status === 200;
};

export const getPatientAppointments = async ({ patient_id }) => {
  const response = await get({
    url: `/v1/appointment?patient_id=${patient_id}`,
  });

  return response.data.data;
};

export const getAppointment = async ({ id }) => {
  const response = await get({
    url: `/v1/appointment/${id}`,
  });

  return response.data.data;
};

export const getAppointmentEntities = async ({ id }) => {
  const response = await get({
    url: `/v1/appointment/${id}/entity`,
  });

  return response.data.data;
};
