<template>
  <v-app :theme="theme">
    <v-app-bar color="primary">
      <template v-slot:prepend>
        <v-app-bar-nav-icon @click.stop="drawer = !drawer">
        </v-app-bar-nav-icon>
      </template>
      <v-app-bar-title>Chunk Hub</v-app-bar-title>

      <template v-slot:append>
        <v-spacer></v-spacer>
        <v-avatar v-if="isLoggedIn" @click="goToProfile" style="cursor: pointer;">
          <img src="@/assets/logo.png" alt="avatarImage" class="avatar-image" />
        </v-avatar>
      </template>
    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>
    <v-footer color="primary" app height="30" class="d-flex justify-center">
      <span class="white--text">&copy; 2024 Chunk Hub</span>
    </v-footer>

    <v-navigation-drawer v-model="drawer" temporary>
      <v-list nav>
        <template v-if="!isLoggedIn">
          <v-list-item title="アカウント登録" value="register" to="/account/register"></v-list-item>
          <v-list-item title="ログイン" value="login" to="/account/login"></v-list-item>
        </template>
        <template v-else>
          <v-list-item title="ホーム" value="home" to="/" :prepend-icon="mdiHome"></v-list-item>
            <v-list-item title="チャンク管理" value="chunk_mng" to="/folders/list"
              :prepend-icon="mdiBookshelf"></v-list-item>
            <v-list-item title="発声練習" value="speak_more" to="/speak_more/select"
              :prepend-icon="mdiAccountVoice"></v-list-item>
          <v-list-group value="Analytics">
            <template v-slot:activator="{ props }">
              <v-list-item v-bind="props" title="分析" :prepend-icon="mdiGoogleAnalytics"></v-list-item>
            </template>
            <v-list-item title="チャンクネットワーク" value="chunk_network" to="/pyvis"
              :prepend-icon="mdiHubOutline"></v-list-item>
            <v-list-item title="学習統計" value="Statistics" to="/statistics" :prepend-icon="mdiSchool"></v-list-item>
          </v-list-group>

          <v-list-item title="使い方" value="usage" to="/usage" :prepend-icon="mdiHelp"></v-list-item>

          <v-list-item title="ログアウト" value="logout" @click="showLogoutDialog" :prepend-icon="mdiLogout"></v-list-item>
        </template>
      </v-list>
    </v-navigation-drawer>
    
    <v-dialog v-model="logoutDialog" max-width="290">
      <v-card>
        <v-card-title class="text-h5">ログアウト確認</v-card-title>
        <v-card-text>本当にログアウトしますか？</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="logoutDialog = false">キャンセル</v-btn>
          <v-btn color="blue darken-1" text @click="logout">OK</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-app>
</template>

<script setup>
import axios from 'axios';
import { ref, watch } from "vue";
import { useRoute } from "vue-router";

const theme = ref("dark");
const drawer = ref(false);
const logoutDialog = ref(false);
const isLoggedIn = ref(false);
const route = useRoute();

watch(route, (newRoute) => {
  document.title = newRoute.meta.title || 'デフォルトのタイトル';
});

function showLogoutDialog() {
  logoutDialog.value = true;
}

function logout() {
  logoutDialog.value = false;
  
  
  fetch("/account/logout", {
    method: "GET",
  })
    .then((response) => {
      
      if (response.ok) {
        window.location.href = "/account/login"; 
      } else {
        
        console.error("ログアウトに失敗しました");
      }
    })
    .catch((error) => {
      console.error("エラーが発生しました", error);
    });
}

function goToProfile() {
  window.location.href = '/account/profile';
}

function checkSession() {
  axios.get('/account/check_session')
    .then(response => {
      isLoggedIn.value = response.data.logged_in;
    })
    .catch(error => {
      console.error('Error checking session:', error);
    });
}

checkSession();
</script>
