<template>
  <q-page class="q-pa-md justify-center column items-center justify-center">
    <div class="login-card">
      <div class="text-bold q-pb-md text-h6 text-blue-grey-9 text-center">
        Esqueci minha senha
      </div>

      <div class="input-text-label">E-mail</div>
      <q-input
        class="q-mb-md bg-white rounded-borders"
        color="primary"
        outlined
        label="username@example.com"
        v-model="email"
        type="text"
        autofocus
      />

      <div v-if="step === 1" class="q-pb-md">
        <div class="input-text-label">Senha</div>
        <q-input
          class="q-mb-md bg-white rounded-borders"
          color="primary"
          outlined
          label="Senha"
          v-model="password"
          type="password"
        />

        <div class="input-text-label">Confirmar senha</div>
        <q-input
          class="q-mb-md bg-white rounded-borders"
          color="primary"
          outlined
          label="Confirmar senha"
          v-model="confirmPassword"
          type="password"
        />

        <div class="center">
          <div class="q-mb-md input-text-label">
            Código de verificação enviado por e-mail
          </div>

          <v-otp-input
            ref="otpInput"
            input-classes="otp-input"
            :conditionalClass="['one', 'two', 'three', 'four', 'five', 'six']"
            separator=""
            inputType="letter-numeric"
            :num-inputs="6"
            v-model:value="pin"
            :should-auto-focus="true"
            :should-focus-order="true"
            :placeholder="['', '', '', '', '', '']"
          />
        </div>
      </div>

      <div class="row q-col-gutter-md">
        <div class="col-6">
          <router-link to="/">
            <q-btn
              type="submit"
              label="Voltar"
              color="secondary"
              class="col full-width"
              no-caps
            />
          </router-link>
        </div>

        <div class="col-6">
          <q-btn
            class="col full-width"
            label="Recuperar senha"
            type="submit"
            no-caps
            color="primary"
            @click="handleSubmit"
            :loading="isLoading"
          />
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref } from "vue";

import {
  showNegativeNotify,
  showWarningNotify,
  showPositiveNotify,
} from "src/util/plugins";
import { isEmail } from "src/util/validate";
import { confirmForgotPassword, forgotPassword } from "src/service/AuthService";

import VOtpInput from "vue3-otp-input";
import { useRouter } from "vue-router";

defineOptions({
  name: "ForgotPassword",
});

const router = useRouter();

const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const pin = ref("");
const step = ref(0); // Step 1 is for password and verification
const isLoading = ref(false);

const handleSubmit = async () => {
  const isEmailValid = isEmail(email.value);
  if (!isEmailValid) {
    showWarningNotify("Informe um e-mail válido!");
    return;
  }

  if (step.value === 0) {
    const body = {
      email: email.value,
    };
    isLoading.value = true;
    const response = await forgotPassword(body);
    console.log(response);
    isLoading.value = false;
    if (response === null || response.status !== 200) {
      showNegativeNotify(
        "Um erro ocorreu, por favor tente novamente mais tarde!"
      );
      return;
    }

    step.value = 1;
    return;
  }

  if (password.value === "") {
    showWarningNotify("Informe sua senha!");
    return;
  }

  if (confirmPassword.value === "") {
    showWarningNotify("Informe sua senha novamente!");
    return;
  }

  if (password.value !== confirmPassword.value) {
    showWarningNotify("Suas senhas não são iguais!");
    return;
  }

  if (
    !/^(?!\s+)(?!.*\s+$)(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[$^*.[\]{}()?"!@#%&/\\,><':;|_~`=+\- ])[A-Za-z0-9$^*.[\]{}()?"!@#%&/\\,><':;|_~`=+\- ]{8,256}$/.test(
      password.value
    )
  ) {
    showWarningNotify(
      "Sua senha deve ter no mínimo 8 caracteres, uma letra maiúscula, uma minúscula, um número e um caractere especial"
    );
    return;
  }

  if (pin.value === "" || pin.value.length != 6) {
    showWarningNotify("Informe o código de verificação!");
    return;
  }

  const body = {
    email: email.value,
    code: pin.value,
    password: password.value,
  };

  isLoading.value = true;
  const response = await confirmForgotPassword(body);
  if (response !== null && response.status === 409) {
    const status = response.data.data.status;

    if (status === "CodeMismatchException") {
      showNegativeNotify("O código inserido está errado, tente novamente!");
      isLoading.value = false;
      return;
    }

    if (status === "ExpiredCodeException") {
      showNegativeNotify("Seu código expirou, tente novamente!");
      isLoading.value = false;
      return;
    }
  }

  if (response === null || response.status !== 200) {
    showNegativeNotify("Um erro ocorreu, tente novamente mais tarde!");
    isLoading.value = false;
    return;
  }

  isLoading.value = false;
  showPositiveNotify("Senha redefinida com sucesso!");

  setTimeout(() => {
    router.push({
      path: "/",
    });
  }, 1000);
};
</script>

<style>
input::placeholder {
  font-size: 15px;
  text-align: center;
  font-weight: 600;
}
</style>
