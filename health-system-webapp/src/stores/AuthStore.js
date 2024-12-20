import { defineStore } from "pinia";

export const useAuthStore = defineStore("AuthStore", {
  state: () => ({
    email: "",
    user: {},
    token: "",
  }),
  getters: {},
  actions: {
    setEmail(email) {
      this.email = email;
    },
    setUser(user) {
      this.user = user;
    },
    setToken(token) {
      this.token = token;
    },
  },
  persist: true,
});
