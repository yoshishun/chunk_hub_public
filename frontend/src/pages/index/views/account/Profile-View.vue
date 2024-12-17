<template>
  <v-container>
    <h1 class="text-center">プロフィール</h1>

    <div class="d-flex flex-column px-2 mt-4" style="word-break: break-word;">
      <div class="d-flex">
        <div class="border-t-lg border-e border-s-lg rounded-ts-lg pl-1 d-flex align-center" style="width: 120px">
          ユーザID
        </div>
        <div class="border-t-lg border-e-lg rounded-te-lg d-flex align-center pa-2" style="width: calc(100% - 120px)">
          {{ profile.id }}
        </div>
      </div>

      <div class="d-flex">
        <div class="border-t border-b border-e border-s-lg pl-1 d-flex align-center" style="width: 120px">
          ユーザ名
        </div>
        <div class="border-t border-b border-e-lg pa-2 d-flex align-center" style="width: calc(100% - 120px);">
          {{ profile.name }}
        </div>
      </div>

      <div class="d-flex">
        <div class="border-b-lg border-s-lg border-e rounded-bs-lg pl-1 d-flex align-center" style="width: 120px">
          メールアドレス
        </div>
        <div class="border-b-lg border-e-lg rounded-be-lg pa-2 d-flex align-center" style="width: calc(100% - 120px)">
          {{ profile.email }}
        </div>
      </div>
    </div>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      profile: {}
    };
  },
  created() {
    this.fetchProfile();
  },
  methods: {
    async fetchProfile() {
      try {
        const response = await axios.get('/api/account/profile');
        this.profile = response.data;
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    }
  }
};
</script>
