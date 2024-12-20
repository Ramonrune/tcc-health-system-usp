import { defineStore } from "pinia";

export const usePatientStore = defineStore("PatientStore", {
  state: () => ({
    patient: null,
  }),
  getters: {},
  actions: {
    setPatient(patient) {
      this.patient = patient;
    },
  },
  persist: true,
});
