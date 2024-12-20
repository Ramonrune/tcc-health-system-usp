import { api } from "src/boot/axios";

export const get = async ({ url }) => {
  return await api
    .get(url, {
      headers: {
        "Content-Type": "application/json",
      },
    })
    .then((response) => {
      return response;
    })
    .catch((err) => {
      if (err.response) {
        return err.response;
      }
      return null;
    });
};

export const post = async ({ url, body }) => {
  return await api
    .post(url, body, {
      headers: {
        "Content-Type": "application/json",
      },
    })
    .then((response) => {
      return response;
    })
    .catch((err) => {
      if (err.response) {
        return err.response;
      }
      return null;
    });
};

export const put = async ({ url, body }) => {
  return await api
    .put(url, body, {
      headers: {
        "Content-Type": "application/json",
      },
    })
    .then((response) => {
      return response;
    })
    .catch((err) => {
      if (err.response) {
        return err.response;
      }
      return null;
    });
};

export const del = async ({ url, body }) => {
  return await api
    .delete(url, {
      headers: {
        "Content-Type": "application/json",
      },
      data: body,
    })
    .then((response) => {
      return response;
    })
    .catch((err) => {
      if (err.response) {
        return err.response;
      }
      return null;
    });
};
