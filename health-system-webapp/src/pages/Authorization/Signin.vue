<template>
  <q-page class="q-pa-md justify-center column items-center justify-center">
    <div class="login-card">
      <div class="text-bold q-pb-md text-h6 text-blue-grey-9 text-center">
        Acesse sua conta
      </div>
      <!-- Campo de E-mail -->
      <q-input
        outlined
        v-model="email"
        type="email"
        label="E-mail"
        class="q-mb-md"
      />

      <!-- Campo de Senha -->
      <q-input
        outlined
        v-model="password"
        type="password"
        label="Senha"
        class="q-mb-md"
      />

      <router-link to="forgot-password">
        <div
          class="text-right text-body2 text-blue-grey-10 q-pb-md cursor-pointer"
        >
          Esqueci minha senha
        </div>
      </router-link>
      <!-- Botão de Enviar -->
      <q-btn
        type="submit"
        label="Entrar"
        color="primary"
        class="full-width"
        no-caps
        :loading="isLoading"
        @click="handleSubmit"
      />

      <router-link to="signup">
        <div
          class="text-center text-body2 text-blue-grey-10 q-pt-md cursor-pointer"
        >
          Não possui conta? <b>Criar conta</b>
        </div>
      </router-link>
    </div>
  </q-page>
</template>

<script setup>
import { auth } from "src/service/AuthService";
import { useAuthStore } from "src/stores/AuthStore";
import { showNegativeNotify, showWarningNotify } from "src/util/plugins";
import { isEmail } from "src/util/validate";
import { ref } from "vue";
import { useRouter } from "vue-router";

defineOptions({
  name: "SigninPage",
});

const email = ref("ramonrune@gmail.com");
const password = ref("Ramon@123");
const isLoading = ref(false);
const router = useRouter();
const authStore = useAuthStore();

const handleSubmit = async () => {
  const isEmailValid = isEmail(email.value);
  if (!isEmailValid) {
    showWarningNotify("Informe um e-mail válido!");
    return;
  }

  if (
    !/^(?!\s+)(?!.*\s+$)(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[$^*.[\]{}()?"!@#%&/\\,><':;|_~`=+\- ])[A-Za-z0-9$^*.[\]{}()?"!@#%&/\\,><':;|_~`=+\- ]{8,256}$/.test(
      password.value
    )
  ) {
    showWarningNotify("Informe uma senha válida!");
    return;
  }

  isLoading.value = true;
  const response = await auth({ email: email.value, password: password.value });

  isLoading.value = false;

  if (response === null || response.status === 500) {
    showNegativeNotify("An error ocurred! Please try again later!");
    return;
  }

  if (response.status !== 200) {
    try {
      const code = response.data.data.code;

      if (code === "UserNotConfirmedException") {
        authStore.setEmail(email.value);

        router.push({
          path: "/activate",
        });

        return;
      }

      const messages = {
        AccountNotFound: "Conta não encontrada!",
        NotAuthorizedException: "E-mail ou senha não encontrados!",
      };

      showNegativeNotify(messages[code]);
    } catch (err) {
      showNegativeNotify("An error ocurred! Please try again later!");
      return;
    }
    return;
  }

  authStore.setEmail(email.value);
  authStore.setUser(response.data.data.user);
  authStore.setToken("Bearer " + response.data.data.token);

  router.push({
    path: "/home",
  });
};
</script>

<style lang="scss">
a {
  text-decoration: none;
}
</style>
