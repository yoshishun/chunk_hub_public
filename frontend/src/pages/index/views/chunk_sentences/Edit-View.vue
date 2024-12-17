<template>
  <v-container>
    <h5 class="text-center">
      <svg-icon height="14px" width="14px" type="mdi" :path="mdi_lock_pattern"></svg-icon>
      {{ folder_name }}
    </h5>
    <h2 class="text-center">- チャンク文/フレーズ 編集 -</h2>

    <template v-if="$vuetify.display.xs">
      <h5 class="text-center mt-4" style="color: grey;">
        登録したチャンク文/フレーズを編集（登録内容の変更・削除等）します。
      </h5>
    </template>
    <template v-else>
      <h4 class="text-center mt-4" style="color: grey;">
        登録したチャンク文/フレーズを編集（登録内容の変更・削除等）します。
      </h4>
    </template>

    <v-divider class="mt-4"></v-divider>

    
    <v-text-field class="mt-4" v-model="search_keyword" single-line density="compact" label="クイック検索" outlined hide-details clearable
      :prepend-inner-icon="mdi_magnify"></v-text-field>

    <div class="border-s-lg border-e-lg border-t-lg border-b text-center bg-primary" style="font-size: 16px;">
      チャンク文/フレーズ一覧
    </div>

    
    <div class="border-s-lg border-e-lg border-b-lg rounded-b-lg pa-4 mb-4">
      <template v-for="(chunk_sentence_row, index) in filtered_chunk_sentences">
        <ChunkSentenceWithTrashCompo :props_chunk_sentence_obj="chunk_sentence_row" :key="chunk_sentence_row.id"
          :props_use_chunk_list="use_chunk_list" :props_chunk_folder_list="chunk_folder_list" v-if="true"
          @save="saveChangeChunkSentenceRow" @delete="deleteChunkRow" @addChunk="addChunk"
          @update:selected="updateSelected">
          <template #index>{{ index + 1 }}</template>
        </ChunkSentenceWithTrashCompo>
      </template>
    </div>

    <div class="border-s-lg border-e-lg border-t-lg border-b rounded-t-lg mt-4 text-center bg-primary" style="font-size: 16px;">
      削除一覧
    </div>

    
    <div class="border-s-lg border-e-lg border-b-lg rounded-b-lg pa-4 mb-4">
      <template v-for="(chunk_sentence_row, index) in delete_chunk_sentence_rows">
        <ChunkSentenceWithRedoCompo :props_chunk_sentence_obj="chunk_sentence_row" :key="chunk_sentence_row.id" 
          v-if="true" @redo="redoChunkRow" @update:selected="updateSelected">
          <template #index>{{ index + 1 }}</template>
        </ChunkSentenceWithRedoCompo>
      </template>
    </div>

    
    <div class="d-flex justify-center">
      <v-btn @click="submitFormData" :disabled="!isDataChanged" width="30%" class="my-4" color="primary">保存</v-btn>
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
import { mdiMagnify, mdiLockPattern } from "@mdi/js";
import ChunkSentenceWithRedoCompo from "../../components/ChunkSentenceWithRedo-Compo.vue";
import ChunkSentenceWithTrashCompo from "../../components/ChunkSentenceWithTrash-Compo.vue";

export default {
  components: {
    ChunkSentenceWithRedoCompo,
    ChunkSentenceWithTrashCompo,
    SvgIcon,
  },
  data() {
    return {
      mdi_magnify: mdiMagnify,
      mdi_lock_pattern: mdiLockPattern,

      all_chunk_sentence_rows: [],
      filtered_chunk_sentences: [], 
      edit_chunk_sentence_rows: [], 
      delete_chunk_sentence_rows: [], 
      new_chunks: [], 
      selectedChunks: [], 

      fid: this.$route.query.fid,
      folder_name: "", 
      use_chunk_list: [], 
      chunk_folder_list: [], 
      search_keyword: "", 
      save_change_executed: false,
      
      snackbar: false,
      snackbarMessage: '',
      snackbarColor: 'success',
      snackbarTimeout: 3000
    };
  },
  computed: {
    
    isDataChanged() {
      return this.save_change_executed || this.delete_chunk_sentence_rows.length > 0;
    },
  },
  methods: {
    
    filterChunks() {
      this.filtered_chunk_sentences = this.all_chunk_sentence_rows.filter(chunk_sentence => {
        if (!this.search_keyword) return true;
        return (
          chunk_sentence.chunk_sentence.includes(this.search_keyword) ||
          chunk_sentence.translating_sentence.includes(this.search_keyword) ||
          chunk_sentence.situation.includes(this.search_keyword) ||
          chunk_sentence.notes.includes(this.search_keyword)
        );
      });
    },
    saveChangeChunkSentenceRow(edited_chunk_sentence) {
      const index_to_update = this.all_chunk_sentence_rows.findIndex(chunk => chunk.id === edited_chunk_sentence.id);
      const filtered_index_to_update = this.filtered_chunk_sentences.findIndex(filtered_chunk => filtered_chunk.id === edited_chunk_sentence.id);
      const edit_index_to_update = this.edit_chunk_sentence_rows.findIndex(edit_chunk => edit_chunk.id === edited_chunk_sentence.id);

      if (index_to_update !== -1 || filtered_index_to_update !== -1) {
        this.all_chunk_sentence_rows.splice(index_to_update, 1, edited_chunk_sentence);
        this.filtered_chunk_sentences.splice(filtered_index_to_update, 1, edited_chunk_sentence);

        if (edit_index_to_update !== -1) {
          this.edit_chunk_sentence_rows.splice(edit_index_to_update, 1, edited_chunk_sentence);
        } else {
          this.edit_chunk_sentence_rows.push(edited_chunk_sentence);
        }

        this.filterChunks();

        this.save_change_executed = true;
        this.showSnackbar('チャンク文/フレーズの編集内容を保存しました。', 'success');
      }
    },
    deleteChunkRow(chunk_sentence_to_delete) {
      const index_to_delete = this.all_chunk_sentence_rows.indexOf(chunk_sentence_to_delete);
      const filtered_index_to_delete = this.filtered_chunk_sentences.indexOf(chunk_sentence_to_delete);
      const edit_index_to_update = this.edit_chunk_sentence_rows.indexOf(chunk_sentence_to_delete);

      if (index_to_delete !== -1 || filtered_index_to_delete !== -1 || edit_index_to_update !== -1) {
        this.all_chunk_sentence_rows.splice(index_to_delete, 1);
        this.filtered_chunk_sentences.splice(filtered_index_to_delete, 1);
        this.edit_chunk_sentence_rows.splice(edit_index_to_update, 1);

        this.delete_chunk_sentence_rows.push(chunk_sentence_to_delete);

        this.filterChunks();
        this.showSnackbar('チャンク文/フレーズを削除一覧に移動しました。', 'success');
      }
    },
    redoChunkRow(chunk_to_redo) {
      const index_to_redo = this.delete_chunk_sentence_rows.indexOf(chunk_to_redo);
      if (index_to_redo !== -1) {
        this.delete_chunk_sentence_rows.splice(index_to_redo, 1);

        this.all_chunk_sentence_rows.push(chunk_to_redo);
        this.filtered_chunk_sentences.push(chunk_to_redo);
        this.edit_chunk_sentence_rows.push(chunk_to_redo);
      }
      this.filterChunks();
      this.showSnackbar('チャンク文/フレーズを元に戻しました。', 'success');
    },
    
    addChunk(new_chunk) {
      this.use_chunk_list.push(new_chunk);
      this.new_chunks.push(new_chunk);
    },
    async submitFormData() {
      const form_data_json = JSON.stringify({ editDataList: this.edit_chunk_sentence_rows, deleteDataList: this.delete_chunk_sentence_rows, newChunks: this.new_chunks });

      try {
        const response = await fetch(`/api/chunk_sentences/list/edit?fid=${this.fid}`, {
          method: "POST",
          headers: {
            'Content-Type': 'application/json'
          },
          body: form_data_json,
        });

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        const data = await response.json();
        console.log("Data submitted successfully:", data);
        this.showSnackbar('データが送信されました。', 'success');
        window.location.href = `/chunk_sentences/list?fid=${this.fid}`;
      } catch (error) {
        console.error("Error submitting data:", error);
        this.showSnackbar('データの送信に失敗しました。', 'error');
      }
    },
    async fetchChunkFolderList() {
      try {
        const response = await fetch(`/api/chunk_folders/list?fclass=1`, {
          method: "GET",
        });
        const data = await response.json();
        this.chunk_folder_list = data.map(item => {
          return {
            "title": item.name,
            "value": { "folder_id": item.id, "folder_name": item.name }
          };
        });
      } catch (error) {
        console.error("Fetch error:", error);
        this.showSnackbar('フォルダリストの読み込みに失敗しました。', 'error');
      }
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
          this.showSnackbar('フォルダが見つかりません。', 'error');
        }
      } catch (error) {
        console.error("Fetch error:", error);
        this.showSnackbar('フォルダ名の読み込みに失敗しました。', 'error');
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
    async fetchChunks() {
      try {
        const response = await fetch(`/api/chunks/list`, {
          method: "GET",
        });
        const json_data = await response.json();
        this.use_chunk_list = json_data.map(item => {
          return {
            "title": item.learning_chunk,
            "value": { "chunk_id": item.id,
                      "learning_chunk": item.learning_chunk,
                      "translating_chunk": item.translating_chunk,
                      "pronounced_count": item.pronounced_count,
                      "politeness": item.politeness,
                      "nuance": item.nuance,
                      "situation": item.situation,
                      "notes": item.notes,
                      "create_date": item.create_date,
                      "update_date": item.update_date,
                    },
          };
        });
        
      } catch (error) {
        console.error("Fetch error:", error);
        this.showSnackbar('チャンクの読み込みに失敗しました。', 'error');
      }
    },
    async fetchData() {
      try {
        await this.fetchFolderName();
        await this.fetchChunkSentences();
        await this.fetchChunks();
        await this.fetchChunkFolderList();
      } catch (error) {
        console.error("Fetch data error:", error);
        this.showSnackbar('データの読み込みに失敗しました。', 'error');
      }
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
    showSnackbar(message, color) {
      this.snackbarMessage = message;
      this.snackbarColor = color;
      this.snackbar = true;
    }
  },
  async mounted() {
    await this.fetchData();
  },
  watch: {
    
    search_keyword() {
      this.filterChunks();
    },
  },
};
</script>
