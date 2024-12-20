const routes = [
  {
    path: "/",
    component: () => import("layouts/AuthorizationLayout.vue"),
    children: [
      { path: "", component: () => import("pages/Authorization/Signin.vue") },
      {
        path: "signup",
        component: () => import("pages/Authorization/Signup.vue"),
      },
      {
        path: "forgot-password",
        component: () => import("pages/Authorization/ForgotPassword.vue"),
      },
      {
        path: "activate",
        component: () => import("pages/Authorization/Activate.vue"),
      },
    ],
  },
  {
    path: "/",
    component: () => import("layouts/MainLayout.vue"),
    children: [
      { path: "home", component: () => import("src/pages/Home/Home.vue") },
      {
        path: "appointment",
        component: () => import("pages/Appointment/Appointment.vue"),
      },
      {
        path: "patient",
        component: () => import("pages/Patient/Patient.vue"),
      },
      {
        path: "patient/data",
        component: () => import("pages/Appointment/Patient/Patient.vue"),
      },
    ],
  },

  // Always leave this as last one,
  // but you can also remove it
  {
    path: "/:catchAll(.*)*",
    component: () => import("pages/ErrorNotFound.vue"),
  },
];

export default routes;
