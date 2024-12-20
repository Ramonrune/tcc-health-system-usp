<template>
  <q-page class="q-pa-md justify-center column items-center justify-center">
    <div class="login-card">
      <div class="text-bold q-pb-md text-h6 text-blue-grey-9 text-center">
        Ativar conta
      </div>

      <div class="q-pb-md">
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
            type="submit"
            label="Ativar conta"
            :loading="isLoading"
            color="primary"
            class="col full-width"
            no-caps
            @click="handleSubmit"
          />
        </div>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref } from "vue";
import {
  showWarningNotify,
  showNegativeNotify,
  showPositiveNotify,
} from "src/util/plugins";

import { useRouter } from "vue-router";
import { confirmSignup } from "src/service/AuthService";
import VOtpInput from "vue3-otp-input";
import { useAuthStore } from "src/stores/AuthStore";

defineOptions({
  name: "ActivatePage",
});

const pin = ref("");
const isLoading = ref(false);
const router = useRouter();
const authStore = useAuthStore();

const handleSubmit = async () => {
  if (pin.value === "") {
    showWarningNotify("Informe o código de verificação!");
    return;
  }

  const body = {
    email: authStore.email,
    code: pin.value,
  };

  isLoading.value = true;
  const response = await confirmSignup(body);

  isLoading.value = false;

  if (
    response !== null &&
    response.status === 409 &&
    response.data.data.status === "CodeMismatchException"
  ) {
    showNegativeNotify("Código incorreto informado!");
  } else if (response !== null && response.status === 200) {
    showPositiveNotify("Conta ativada com sucesso!");

    setTimeout(() => {
      router.push({ path: "/" });
    }, 1000);
  } else {
    showNegativeNotify("Um erro ocorreu, tente novamente mais tarde!");
    return;
  }
};
</script>
