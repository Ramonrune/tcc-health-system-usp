<template>
  <q-page class="q-pa-md justify-center column items-center justify-center">
    <div class="login-card">
      <div class="text-bold q-pb-md text-h6 text-blue-grey-9 text-center">
        Nova conta
      </div>

      <q-input
        outlined
        v-model="name"
        type="text"
        label="Nome"
        class="q-mb-md"
      />

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

      <q-input
        outlined
        v-model="confirmPassword"
        type="password"
        label="Confirmar senha"
        class="q-mb-md"
      />

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
            label="Criar conta"
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
import { isEmail } from "src/util/validate";
import { useRouter } from "vue-router";
import { signup } from "src/service/AuthService";
import { useAuthStore } from "src/stores/AuthStore";

defineOptions({
  name: "SignupPage",
});

const name = ref("");
const email = ref("");
const password = ref("");
const confirmPassword = ref("");
const isLoading = ref(false);
const router = useRouter();
const authStore = useAuthStore();

const handleSubmit = async () => {
  if (name.value === "") {
    showWarningNotify("Informe seu nome!");
    return;
  }

  const isEmailValid = isEmail(email.value);
  if (!isEmailValid) {
    showWarningNotify("Informe um e-mail válido!");
    return;
  }

  if (password.value === "") {
    showWarningNotify("Informe sua senha!");
    return;
  }

  if (confirmPassword.value === "") {
    showWarningNotify("Informe a confirmação da sua senha!");
    return;
  }

  if (password.value !== confirmPassword.value) {
    showWarningNotify("As senhas não coincidem!");
    return;
  }

  if (
    !/^(?!\s+)(?!.*\s+$)(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*[$^*.[\]{}()?"!@#%&/\\,><':;|_~`=+\- ])[A-Za-z0-9$^*.[\]{}()?"!@#%&/\\,><':;|_~`=+\- ]{8,256}$/.test(
      password.value
    )
  ) {
    showWarningNotify(
      "A senha deve ter pelo menos 8 caracteres, incluindo uma letra maiúscula, uma letra minúscula, um número e um caractere especial!"
    );
    return;
  }

  const body = {
    name: name.value,
    email: email.value,
    password: password.value,
  };

  isLoading.value = true;
  const response = await signup(body);

  isLoading.value = false;

  if (response !== null && response.status === 409) {
    showNegativeNotify("Já existe uma conta com esse e-mail cadastrado!");
  } else if (response !== null && response.status === 201) {
    showPositiveNotify("Conta criada com sucesso!");
    authStore.setEmail(email.value);

    setTimeout(() => {
      router.push({ path: "/activate" });
    }, 1000);
  } else {
    showNegativeNotify("Um erro ocorreu, tente novamente mais tarde!");
    return;
  }
};
</script>
