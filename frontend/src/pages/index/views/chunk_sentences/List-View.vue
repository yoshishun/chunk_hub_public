<template>
  <v-container>
    <h5 class="text-center">
      <svg-icon height="14px" width="14px" type="mdi" :path="mdi_lock_pattern"></svg-icon>
      {{ folder_name }}
    </h5>
    <h2 class="text-center">- チャンク文/フレーズ 一覧 -</h2>

    <template v-if="$vuetify.display.xs">
      <h5 class="text-center mt-4" style="color: grey;">
        登録したチャンク文/フレーズを管理します。
      </h5>
    </template>
    <template v-else>
      <h4 class="text-center mt-4" style="color: grey;">
        登録したチャンク文/フレーズを管理します。
      </h4>
    </template>

    <v-divider class="mt-4"></v-divider>

    <div class="d-flex justify-space-evenly my-2 py-2">
      <v-btn @click="toChunkSentencesCreate" width="45%" :prepend-icon="mdi_plus_circle" class="border" color="primary">作成</v-btn>
      <v-btn @click="toChunkSentencesEdit" width="45%" :prepend-icon="mdi_file_edit" class="border" color="primary">一括編集</v-btn>
    </div>

    
    <v-text-field v-model="search_keyword" single-line density="compact" label="クイック検索" outlined hide-details clearable
      :prepend-inner-icon="mdi_magnify"></v-text-field>

    <div height="480" tile class="border-lg overflow-auto rounded-b-lg pa-4 mb-4">
      <template v-for="(chunk_sentence_row, index) in filtered_chunks">
        <ChunkSentenceCompo :props_chunk_sentence_row="chunk_sentence_row" :index="index" @chunk-sentence-moved="removeChunkSentence" :key="chunk_sentence_row.id" v-if="true">
          <template #index>{{ index + 1 }}</template>
        </ChunkSentenceCompo>
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
import { mdiMagnify, mdiPlusCircle, mdiFileEdit, mdiLockPattern } from "@mdi/js";
import ChunkSentenceCompo from "../../components/ChunkSentence-Compo.vue";

export default {
  components: {
    ChunkSentenceCompo,
    SvgIcon,
  },
  data() {
    return {
      
      mdi_magnify: mdiMagnify,
      mdi_plus_circle: mdiPlusCircle,
      mdi_file_edit: mdiFileEdit,
      mdi_lock_pattern: mdiLockPattern,

      all_chunk_sentence_rows: [],
      filtered_chunks: [], 
      selectedChunks: [], 

      folder_name: "", 
      fid: this.$route.query.fid,
      search_keyword: "", 

      snackbar: false,
      snackbarMessage: '',
      snackbarColor: 'success',
      snackbarTimeout: 3000
    };
  },
  methods: {
    
    filterChunks() {
      this.filtered_chunks = this.all_chunk_sentence_rows.filter(chunk_sentence => {
        
        if (!this.search_keyword) return true;
        
        return (
          chunk_sentence.chunk_sentence.includes(this.search_keyword) ||
          chunk_sentence.translating_sentence.includes(this.search_keyword) ||
          chunk_sentence.situation.includes(this.search_keyword) ||
          chunk_sentence.notes.includes(this.search_keyword)
        );
      });
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
          this.showSnackbar('フォルダの読み込みに失敗しました。', 'error');
        }
      } catch (error) {
        console.error("Fetch error:", error);
        this.showSnackbar('フォルダの読み込みに失敗しました。', 'error');
      }
    },
    async fetchChunkSentences() {
      try {
        const response = await fetch(`/api/chunk_sentences/list?fid=${this.fid}`, {
          method: "GET",
        });
        const data = await response.json();
        if (data.length > 0 && data[0].chunk_sentences) {
          this.all_chunk_sentence_rows = data[0].chunk_sentences;
        } else {
          this.all_chunk_sentence_rows = [];
        }
        this.filterChunks();
      } catch (error) {
        console.error("Fetch error:", error);
        this.showSnackbar('チャンク文/フレーズの読み込みに失敗しました。', 'error');
      }
    },
    async fetchData() {
      try {
        await this.fetchFolderName();
        await this.fetchChunkSentences();
      } catch (error) {
        console.error("Fetch data error:", error);
        this.showSnackbar('データの読み込みに失敗しました。', 'error');
      }
    },
    toChunkSentencesCreate() {
      this.$router.push({
        path: "/chunk_sentences/list/create",
        query: { fid: this.$route.query.fid },
      });
    },
    toChunkSentencesEdit() {
      this.$router.push({
        path: "/chunk_sentences/list/edit",
        query: { fid: this.$route.query.fid },
      });
    },
    updateSelected(checked, chunk_sentence_row) {
      if (checked) {
        this.selectedChunks.push(chunk_sentence_row);
      } else {
        const index = this.selectedChunks.findIndex(chunk => chunk.id === chunk_sentence_row.id);
        if (index !== -1) {
          this.selectedChunks.splice(index, 1);
        }
      }
    },
    removeChunkSentence(chunkSentenceId) {
      this.all_chunk_sentence_rows = this.all_chunk_sentence_rows.filter(chunk_sentence => chunk_sentence.id !== chunkSentenceId);
      this.filterChunks();
      this.showSnackbar('チャンク文/フレーズが移動されました。', 'success');
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
    }
  }
};
</script>
