import { del, get, post, put } from "./BaseService";

export const register = async ({ patient_id, disease_id, note }) => {
  return await post({
    url: "/v1/disease",
    body: { patient_id, disease_id, note },
  });
};

export const update = async ({ id, patient_id, disease_id, note }) => {
  const response = await put({
    url: `/v1/disease/${id}`,
    body: { patient_id, disease_id, note },
  });

  return response.status === 200;
};

export const remove = async ({ id }) => {
  const response = await del({
    url: `/v1/disease/${id}`,
    body: {},
  });
  return response.status === 200;
};

export const getDiseases = async ({ name }) => {
  const response = await get({
    url: `/v1/disease?name=${name}`,
  });
  return response.data.data;
};

export const getPatientDiseases = async ({ patient_id }) => {
  const response = await get({
    url: `/v1/disease?patient_id=${patient_id}`,
  });

  let data = response.data.data;

  return data.map((e) => {
    return {
      patient_disease_id: e.id,
      ...e.disease,
      date: e.date_entered,
    };
  });
};

export const getDisease = async ({ id }) => {
  const response = await get({
    url: `/v1/disease/${id}`,
  });

  return response.data.data;
};
