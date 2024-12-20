import { del, get, post, put } from "./BaseService";

export const register = async ({ patient_id, medication_id, note }) => {
  const response = await post({
    url: "/v1/medication",
    body: { patient_id, medication_id, note },
  });

  return response.status === 201;
};

export const update = async ({ id, patient_id, medication_id, note }) => {
  const response = await put({
    url: `/v1/medication/${id}`,
    body: { patient_id, medication_id, note },
  });

  return response.status === 200;
};

export const remove = async ({ id }) => {
  const response = await del({
    url: `/v1/medication/${id}`,
    body: {},
  });

  return response.status === 200;
};

export const getMedications = async ({ name }) => {
  const response = await get({
    url: `/v1/medication?name=${name}`,
  });

  return response.data.data;
};

export const getPatientMedications = async ({ patient_id }) => {
  const response = await get({
    url: `/v1/medication?patient_id=${patient_id}`,
  });

  let data = response.data.data;

  return data.map((e) => {
    return {
      patient_medication_id: e.id,
      ...e.medication,
      date: e.date_entered,
    };
  });
};

export const getMedication = async ({ id }) => {
  const response = await get({
    url: `/v1/medication/${id}`,
  });

  return response.data.data;
};
