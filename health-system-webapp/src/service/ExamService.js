import axios from "axios";
const request = axios.CancelToken.source();
import { del, get, post, put } from "./BaseService";

export const register = async ({
  name,
  note,
  date,
  patient_id,
  file_extension,
}) => {
  const response = await post({
    url: "/v1/exam",
    body: { name, note, date, patient_id, file_extension },
  });

  if (response && response.status === 201) {
    return response.data.data.id;
  }

  return null;
};

export const update = async ({
  id,
  name,
  note,
  date,
  patient_id,
  file_extension,
}) => {
  return await put({
    url: `/v1/exam/${id}`,
    body: { name, note, date, patient_id, file_extension },
  });
};

export const remove = async ({ id }) => {
  const response = await del({
    url: `/v1/exam/${id}`,
    body: {},
  });

  if (response && response.status === 200) {
    return true;
  }

  return false;
};

export const getExam = async ({ id }) => {
  const response = await get({
    url: `/v1/exam/${id}`,
  });

  return response.data.data;
};

export const getExams = async ({ patient_id }) => {
  const response = await get({
    url: `/v1/exam?patient_id=${patient_id}`,
  });

  return response.data.data;
};

export const uploadExamDocument = async ({
  id,
  file,
  patient_id,
  file_extension,
}) => {
  const resPresigned = await createUploadLink(id, patient_id, file_extension);
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

export const createUploadLink = async (id, patient_id, file_extension) => {
  return await post({
    url: `/v1/exam/${id}/upload-document-link`,
    body: { patient_id, file_extension },
  });
};

export const getExamDocumentFileFormat = async ({ id }) => {
  const link = await getExamDocument({ id });
  const urlWithoutQuery = link.split("?")[0];
  const urlParts = urlWithoutQuery.split("/");
  const fileName = urlParts[urlParts.length - 1];

  const response = await fetch(link);
  const blob = await response.blob();
  const file = new File([blob], fileName, { type: blob.type });

  return file;
};

export const getExamDocument = async ({ id }) => {
  const response = await get({
    url: `/v1/exam/${id}/document-link`,
    body: {},
  });

  return response.data.data.link;
};
