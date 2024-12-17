<template>
  <v-container>
    <h1 class="text-center">アカウント登録</h1>
    <v-form ref="form" v-model="valid" lazy-validation>
      <p v-if="error" class="error">{{ error }}</p>

      <v-label>ユーザ名</v-label>
      <v-text-field
        v-model="user_name"
        :rules="user_name_rules"
        label="User Name"
        required
      ></v-text-field>

      <v-label>メールアドレス</v-label>
      <v-text-field
        v-model="email"
        :rules="email_rules"
        label="Email"
        required
      ></v-text-field>

      <v-label>パスワード</v-label>
      <v-text-field
        v-model="password"
        :rules="password_rules"
        label="Password"
        type="password"
        required
      ></v-text-field>

      <v-btn
        color="primary"
        class="mr-4"
        @click="register"
        :disabled="!valid"
      >
        Register
      </v-btn>

      <v-snackbar v-model="snackbar" :timeout="snackbarTimeout" top>
        {{ snackbarMessage }}
        <v-btn color="red" text @click="snackbar = false">Close</v-btn>
      </v-snackbar>
    </v-form>
  </v-container>
</template>

<script>
export default {
  name: 'RegisterForm',
  data() {
    return {
      user_name: '',
      email: '',
      password: '',
      error: '',
      valid: true,
      snackbar: false,
      snackbarMessage: '',
      snackbarTimeout: 6000,
      user_name_rules: [
        v => !!v || 'User name is required'
      ],
      email_rules: [
        v => !!v || 'Email is required',
        v => /.+@.+\..+/.test(v) || 'Email must be valid'
      ],
      password_rules: [
        v => !!v || 'Password is required'
      ]
    }
  },
  methods: {
    register() {
      if (this.$refs.form.validate()) {
        const form_data = new FormData();
        form_data.append("user_name", this.user_name);
        form_data.append("email", this.email);
        form_data.append("password", this.password);
        fetch("/account/register", {
          method: "POST",
          body: form_data,
        })
        .then(response => response.json())
        .then(data => {
          if (data.status === 'success') {
            window.location.href = "/account/login";
          } else {
            this.snackbarMessage = data.message;
            this.snackbar = true;
          }
        })
        .catch(error => {
          this.error = error.response ? error.response.data.message : error.message;
          this.snackbarMessage = this.error;
          this.snackbar = true;
        });
      }
    },
  }
}
</script>

<style scoped>
.error {
  color: red;
}
</style>
