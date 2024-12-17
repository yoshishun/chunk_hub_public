<template>
  <v-container>
    <h1 class="text-center">ログイン</h1>
    <v-form ref="form" v-model="valid" lazy-validation>
      <p v-if="error && !loading" class="error">{{ error }}</p>
      <v-label>メールアドレス/ユーザ名</v-label>
      <v-text-field
        v-model="identifier"
        :rules="identifier_rules"
        label="Email or Username"
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
        @click="login"
        :disabled="!valid || loading"
      >
        <template v-if="loading">
          <v-progress-circular indeterminate color="white" size="20"></v-progress-circular>
        </template>
        <template v-else>
          Login
        </template>
      </v-btn>
    </v-form>
  </v-container>
</template>

<script>
export default {
  name: 'LoginForm',
  data() {
    return {
      identifier: '',
      password: '',
      error: '',
      valid: true, 
      loading: false, 
      identifier_rules: [
        v => !!v || 'Email or Username is required'
      ],
      password_rules: [
        v => !!v || 'Password is required'
      ]
    }
  },
  methods: {
    login() {
      
      if (this.$refs.form.validate()) {
        this.loading = true; 
        this.error = ''; 
        setTimeout(() => {
          const form_data = new FormData();
          form_data.append("identifier", this.identifier);
          form_data.append("password", this.password);
          fetch("/account/login", {
            method: "POST",
            body: form_data,
          })
          .then(response => {
            this.loading = false; 
            if (response.ok) {
              window.location.href = "/"; 
            } else {
              return response.json();
            }
          })
          .then(data => {
            if (data && data.message) {
              this.error = data.message;
            }
          })
          .catch(() => {
            this.loading = false; 
            this.error = 'An unexpected error occurred. Please try again later.';
            
          });
        }, 1000); 
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
