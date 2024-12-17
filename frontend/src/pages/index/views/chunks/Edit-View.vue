<template>
  <v-container>
    <h5 class="text-center">
      <svg-icon height="14px" width="14px" type="mdi" :path="mdiPuzzle"></svg-icon>
      {{ folder_name }}
    </h5>
    <h2 class="text-center">- チャンク編集 -</h2>

    <template v-if="$vuetify.display.xs">
      <h5 class="text-center mt-4" style="color: grey;">
        登録したチャンクを編集（登録内容の変更・削除等）します。
      </h5>
    </template>
    <template v-else>
      <h4 class="text-center mt-4" style="color: grey;">
        登録したチャンクを編集（登録内容の変更・削除等）します。
      </h4>
    </template>

    <v-divider class="mt-4"></v-divider>

    <v-text-field class="mt-4" v-model="search_keyword" single-line density="compact" label="クイック検索" outlined hide-details clearable
      :prepend-inner-icon="mdiMagnify"></v-text-field>

    <div class="border-s-lg border-e-lg border-t-lg border-b text-center bg-primary" style="font-size: 16px;">
      チャンク一覧
    </div>

    <div class="border-s-lg border-e-lg border-b-lg rounded-b-lg pa-4 mb-4">
      <template v-for="(chunk_row, index) in filtered_chunks">
        <ChunkWithTrashCompo :key="chunk_row.id" :props_chunk_row="chunk_row" v-if="true"
          @save="saveChangeChunkRow" @delete="deleteChunkRow">
          <template #index>{{ index + 1 }}</template>
        </ChunkWithTrashCompo>
      </template>
    </div>

    <div class="border-s-lg border-e-lg border-t-lg border-b rounded-t-lg mt-4 text-center bg-primary" style="font-size: 16px;">
      削除一覧
    </div>
    
    <div class="border-s-lg border-e-lg border-b-lg rounded-b-lg pa-4 mb-4">
      <template v-for="(chunk_row, index) in delete_chunk_rows">
        <ChunkWithRedoCompo :key="chunk_row.id" :props_chunk_row="chunk_row" v-if="true" @redo="redoChunkRow">
          <template #index>{{ index + 1 }}</template>
        </ChunkWithRedoCompo>
      </template>
    </div>

    <div class="d-flex justify-center">
      <v-btn @click="submitFormData" :disabled="!is_data_changed" width="30%" class="my-4" color="primary">保存</v-btn>
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
import { mdiMagnify, mdiPuzzle } from "@mdi/js";
import ChunkWithTrashCompo from "../../components/ChunkWithTrash-Compo.vue";
import ChunkWithRedoCompo from "../../components/ChunkWithRedo-Compo.vue";
import axios from 'axios';

export default {
  components: {
    ChunkWithTrashCompo,
    ChunkWithRedoCompo,
    SvgIcon,
  },
  data() {
    return {
      mdiMagnify,
      mdiPuzzle,

      all_chunk_rows: [],
      filtered_chunks: [],
      edit_chunk_rows: [],
      delete_chunk_rows: [],

      fid: this.$route.query.fid,
      folder_name: "",
      search_keyword: "",
      save_change_executed: false,

      snackbar: false,
      snackbarMessage: '',
      snackbarColor: 'success',
      snackbarTimeout: 3000
    };
  },
  computed: {
    is_data_changed() {
      return this.save_change_executed || this.delete_chunk_rows.length > 0;
    },
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
    saveChangeChunkRow(edited_chunk) {
      const index_to_update = this.all_chunk_rows.findIndex(chunk => chunk.id === edited_chunk.id);
      const filtered_index_to_update = this.filtered_chunks.findIndex(filtered_chunk => filtered_chunk.id === edited_chunk.id);
      const edit_index_to_update = this.edit_chunk_rows.findIndex(edit_chunk => edit_chunk.id === edited_chunk.id);

      if (index_to_update !== -1 || filtered_index_to_update !== -1) {
        this.all_chunk_rows.splice(index_to_update, 1, edited_chunk);
        this.filtered_chunks.splice(filtered_index_to_update, 1, edited_chunk);

        if (edit_index_to_update !== -1) {
          this.edit_chunk_rows.splice(edit_index_to_update, 1, edited_chunk);
        } else {
          this.edit_chunk_rows.push(edited_chunk);
        }

        this.filterChunks();
        this.save_change_executed = true;
        this.showSnackbar('チャンクの編集内容を保存しました。', 'success');
      }
    },
    deleteChunkRow(chunk_to_delete) {
      const index_to_delete = this.all_chunk_rows.indexOf(chunk_to_delete);
      const filtered_index_to_delete = this.filtered_chunks.indexOf(chunk_to_delete);
      const edit_index_to_update = this.edit_chunk_rows.indexOf(chunk_to_delete);

      if (index_to_delete !== -1 || filtered_index_to_delete !== -1 || edit_index_to_update !== -1) {
        this.all_chunk_rows.splice(index_to_delete, 1);
        this.filtered_chunks.splice(filtered_index_to_delete, 1);
        this.edit_chunk_rows.splice(edit_index_to_update, 1);

        this.delete_chunk_rows.push(chunk_to_delete);
        this.showSnackbar('チャンクを削除一覧に移動しました。', 'success');
      }
      this.filterChunks();
    },
    redoChunkRow(chunk_to_redo) {
      const index_to_redo = this.delete_chunk_rows.indexOf(chunk_to_redo);
      if (index_to_redo !== -1) {
        this.delete_chunk_rows.splice(index_to_redo, 1);

        this.all_chunk_rows.push(chunk_to_redo);
        this.filtered_chunks.push(chunk_to_redo);
        this.edit_chunk_rows.push(chunk_to_redo);
        this.showSnackbar('チャンクを元に戻しました。', 'success');
      }
      this.filterChunks();
    },
    async submitFormData() {
      const form_data_json = JSON.stringify({ editDataList: this.edit_chunk_rows, deleteDataList: this.delete_chunk_rows });

      try {
        const response = await axios.post(`/api/chunks/list/edit?fid=${this.fid}`, form_data_json, {
          headers: { 'Content-Type': 'application/json' },
        });

        if (response.status !== 200) {
          throw new Error("Network response was not ok");
        }

        window.location.href = `/chunks/list?fid=${this.fid}`;
      } catch (error) {
        console.error("Error submitting data:", error);
        this.showSnackbar('データの送信に失敗しました。', 'error');
      }
    },
    async fetchFolderName() {
      try {
        const response = await axios.get(`/api/folders/name?fid=${this.fid}`);
        if (response.data.name) {
          this.folder_name = response.data.name;
        } else {
          console.error("Folder not found");
          this.showSnackbar('フォルダが見つかりませんでした。', 'error');
        }
      } catch (error) {
        console.error("Fetch error:", error);
        this.showSnackbar('フォルダの読み込みに失敗しました。', 'error');
      }
    },
    async fetchChunks() {
      try {
        const response = await axios.get(`/api/chunks/list?fid=${this.fid}`);
        this.all_chunk_rows = response.data;
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
    search_keyword: function () {
      this.filterChunks();
    },
  },
};
</script>
