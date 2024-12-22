import axios from "axios";
const request = axios.CancelToken.source();
import { del, get, post, put } from "./BaseService";
import { calculateAge } from "src/util/date";

export const register = async ({ name, birth_date, cpf, email, phone }) => {
  return await post({
    url: "/v1/patient",
    body: { name, birth_date, cpf, email, phone },
  });
};

export const update = async ({
  id,
  name,
  phone,
  weight,
  height,
  gender,
  birth_date,
  blood_type,
  smookes,
}) => {
  let response = await put({
    url: `/v1/patient/${id}`,
    body: {
      name,
      phone,
      weight,
      height,
      gender,
      birth_date,
      blood_type,
      smookes,
    },
  });

  if (response && response.status === 200) {
    return true;
  } else {
    return false;
  }
};

export const remove = async ({ id }) => {
  const response = await del({
    url: `/v1/patient/${id}`,
    body: {},
  });

  return response.status === 200;
};

export const getPatient = async ({ id }) => {
  let response = await get({
    url: `/v1/patient/${id}`,
  });

  if (response.status === 404) {
    return null;
  }

  return response.data.data;
};

export const getPatientByCpf = async ({ cpf }) => {
  const response = await get({
    url: `/v1/patient?cpf=${cpf}`,
  });

  if (response.status === 404) {
    return null;
  }

  return response.data.data;
};

export const uploadProfilePicture = async ({ id, file }) => {
  const resPresigned = await createUploadLink(id);
  if (resPresigned && resPresigned.status !== 200) {
    return { status: false, link: "" };
  }

  const link = resPresigned.data.data.fields;

  let data = new FormData();
  data.append("key", link["key"]);
  data.append("X-Amz-Signature", link["x-amz-signature"]);
  data.append("X-Amz-Date", link["x-amz-date"]);
  data.append("X-Amz-Credential", link["x-amz-credential"]);
  data.append("X-Amz-Algorithm", link["x-amz-algorithm"]);
  data.append("Policy", link["policy"]);
  data.append("file", file);

  return await axios
    .post(resPresigned.data.data.url, data, {
      cancelToken: request.token,
      headers: {
        "Content-Type": "multipart/form-data",
      },
    })
    .then(async (response) => {
      if (response.status === 204) {
        return {
          status: true,
          link: link,
        };
      }
    })
    .catch(function () {
      return {
        status: false,
        link: link,
      };
    });
};

export const createUploadLink = async (id) => {
  return await post({
    url: `/v1/patient/${id}/profile-picture/upload-link`,
    body: {},
  });
};

export const getPatientPicture = async ({ id }) => {
  const response = await get({
    url: `/v1/patient/${id}/profile-picture-link`,
    body: {},
  });

  return response.data.data.link;
};

export const getDoctorPatients = async () => {
  let response = await get({
    url: `/v1/doctor/patient`,
  });

  return response.data.data.map((e) => {
    return {
      ...e,
      age: calculateAge(e.birth_date),
    };
  });
};

export const sendEmail = async ({ id, subject, html_content }) => {
  const response = await post({
    url: `/v1/patient/${id}/email`,
    body: { subject, html_content },
  });

  return response.status === 200;
};
