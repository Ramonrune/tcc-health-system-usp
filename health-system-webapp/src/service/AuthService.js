import { post } from "./BaseService";

export const auth = async ({ email, password }) => {
  return await post({ url: "/v1/auth", body: { email, password } });
};

export const signup = async ({ name, email, password, confirm_password }) => {
  return await post({
    url: "/v1/auth/signup",
    body: { name, email, password, confirm_password },
  });
};

export const confirmSignup = async ({ email, code }) => {
  return await post({
    url: "/v1/auth/signup/confirm",
    body: { email, code },
  });
};

export const forgotPassword = async ({ email }) => {
  return await post({
    url: "/v1/auth/forgot-password",
    body: { email },
  });
};

export const confirmForgotPassword = async ({ email, password, code }) => {
  return await post({
    url: "/v1/auth/forgot-password/confirm",
    body: { email, password, code },
  });
};
