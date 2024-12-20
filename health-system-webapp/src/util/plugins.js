import { Loading, Notify, QSpinnerBars } from "quasar";

export function showLoading(message) {
  Loading.show({
    message: message,
    spinner: QSpinnerBars,
    spinnerColor: "primary",
  });
}

export function hideLoading() {
  Loading.hide();
}

export function showNegativeNotify(message) {
  Notify.create({
    message: message,
    type: "negative",
    actions: [
      {
        icon: "close",
        color: "white",
      },
    ],
  });
}

export function showWarningNotify(message) {
  Notify.create({
    message: message,
    type: "warning",
    actions: [
      {
        icon: "close",
        color: "white",
      },
    ],
  });
}

export function showPositiveNotify(message, action) {
  Notify.create({
    message: message,
    type: "positive",
    //timeout: 2000,
    actions: [
      {
        icon: "close",
        color: "white",
      },
    ],
    onDismiss: action,
  });
}

export function showInfoNotify(message, action) {
  Notify.create({
    message: message,
    type: "info",
    //timeout: 2000,
    actions: [
      {
        icon: "close",
        color: "white",
      },
    ],
    onDismiss: action,
  });
}
