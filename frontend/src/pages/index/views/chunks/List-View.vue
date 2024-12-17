<template>
  <v-container>
    <h5 class="text-center">
      <svg-icon height="14px" width="14px" type="mdi" :path="mdiPuzzle"></svg-icon>
      {{ folder_name }}
    </h5>
    <h2 class="text-center">- チャンク一覧 -</h2>

    <template v-if="$vuetify.display.xs">
      <h5 class="text-center mt-4" style="color: grey;">
        登録したチャンクを管理します。
      </h5>
    </template>
    <template v-else>
      <h4 class="text-center mt-4" style="color: grey;">
        登録したチャンクを管理します。
      </h4>
    </template>

    <v-divider class="mt-4"></v-divider>

    <div class="d-flex justify-space-evenly my-2 py-2">
      <v-btn @click="toChunksAdd" width="30%" :prepend-icon="mdiPlusCircle" class="border" color="primary">追加</v-btn>
      <v-btn @click="toChunksEdit" width="30%" :prepend-icon="mdiFileEdit" class="border" color="primary">編集</v-btn>
    </div>

    <v-text-field v-model="search_keyword" single-line density="compact" label="クイック検索" outlined hide-details clearable :prepend-inner-icon="mdiMagnify"></v-text-field>

    <div class="border-lg rounded-b-lg pa-4 mb-4">
      <template v-for="(chunk_row, index) in filtered_chunks" >
        <ChunkCompo :props_chunk_row="chunk_row" :key="chunk_row.id" v-if="true" @chunk-moved="removeChunk">
          <template #index>{{ index + 1 }}</template>
        </ChunkCompo>
      </template>
    </div>

    
    <v-snackbar v-model="snackbar" :timeout="snackbarTimeout" :color="snackbarColor">
      {{ snackbarMessage }}
      <template v-slot:action="{ attrs }">
        <v-btn color="white" text @click="snackbar = false" v-bind="attrs">Close</v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script>
import SvgIcon from '@jamescoyle/vue-icon';
import { mdiMagnify, mdiPlusCircle, mdiFileEdit, mdiPuzzle } from "@mdi/js";
import ChunkCompo from "../../components/Chunk-Compo.vue";

export default {
  components: {
    ChunkCompo,
    SvgIcon,
  },
  data() {
    return {
      mdiMagnify,
      mdiPlusCircle,
      mdiFileEdit,
      mdiPuzzle,

      all_chunk_rows: [],
      filtered_chunks: [],

      fid: this.$route.query.fid,
      folder_name: "",
      search_keyword: "",

      snackbar: false,
      snackbarMessage: '',
      snackbarColor: 'success',
      snackbarTimeout: 3000
    };
  },
  methods: {
    filterChunks() {
      this.filtered_chunks = this.all_chunk_rows.filter(chunk => {
        if (!this.search_keyword) return true;
        return (
          (chunk.learning_chunk || '').includes(this.search_keyword) ||
          (chunk.translating_chunk || '').includes(this.search_keyword) ||
          (chunk.nuance || '').includes(this.search_keyword) || 
          (chunk.situation || '').includes(this.search_keyword) || 
          (chunk.notes || '').includes(this.search_keyword)
        );
      });
    },
    removeChunk(chunkId) {
      this.all_chunk_rows = this.all_chunk_rows.filter(chunk => chunk.id !== chunkId);
      this.filterChunks();
      this.showSnackbar('チャンクを移動しました。', 'success');
    },
    toChunksAdd() {
      this.$router.push({
        path: "/chunks/list/add",
        query: { fid: this.$route.query.fid },
      });
    },
    toChunksEdit() {
      this.$router.push({
        path: "/chunks/list/edit",
        query: { fid: this.$route.query.fid },
      });
    },
    toBack() {
      this.$router.go(-1);
    },
    async fetchFolderName() {
      try {
        const response = await fetch(`/api/folders/name?fid=${this.fid}`, {
          method: "GET",
        });
        const data = await response.json();
        if (data.name) {
          this.folder_name = data.name;
        } else {
          console.error("Folder not found");
        }
      } catch (error) {
        console.error("Fetch error:", error);
        this.showSnackbar('フォルダの読み込みに失敗しました。', 'error');
      }
    },
    async fetchChunks() {
      try {
        const response = await fetch(`/api/chunks/list?fid=${this.fid}`, {
          method: "GET",
        });
        const data = await response.json();
        this.all_chunk_rows = data;
        this.filterChunks();
      } catch (error) {
        console.error("Fetch error:", error);
        this.showSnackbar('チャンクの読み込みに失敗しました。', 'error');
      }
    },
    async fetchData() {
      try {
        await this.fetchFolderName();
        await this.fetchChunks();
      } catch (error) {
        console.error("Fetch data error:", error);
        this.showSnackbar('データの読み込みに失敗しました。', 'error');
      }
    },
    showSnackbar(message, color) {
      this.snackbarMessage = message;
      this.snackbarColor = color;
      this.snackbar = true;
    }
  },
  mounted() {
    this.fetchData();
  },
  watch: {
    search_keyword() {
      this.filterChunks();
    },
  },
};
</script>
