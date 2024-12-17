<template>
  <v-container grid-list-xs>
    <h5 class="text-center">
      <svg-icon height="14px" width="14px" type="mdi" :path="mdi_puzzle"></svg-icon>
      {{ folder_name }}
    </h5>
    <h2 class="text-center">- チャンク追加 -</h2>

    <template v-if="$vuetify.display.xs">
      <h5 class="text-center mt-4" style="color: grey;">
        チャンクを追加します。
      </h5>
    </template>
    <template v-else>
      <h4 class="text-center mt-4" style="color: grey;">
        チャンクを追加します。
      </h4>
    </template>

    <v-divider class="mt-4"></v-divider>

    <div class="border-s-lg border-e-lg border-t-lg border-b rounded-t-lg mt-4 text-center bg-primary" style="font-size: 16px;">
      チャンク入力フォーム
    </div>
    <div class="border-s-lg border-e-lg border-b-lg rounded-b-lg pa-4 mb-4">
      <v-label>チャンク</v-label>
      <v-textarea v-model="form_data.learning_chunk" rows="1" clearable counter auto-grow></v-textarea>

      <v-label>翻訳文</v-label>
      <v-textarea v-model="form_data.translating_chunk" rows="1" clearable counter auto-grow></v-textarea>

      <v-label>丁寧度</v-label>
      <v-slider v-model="form_data.politeness" :color="politenessColor" class="w-90"
        :ticks="{ 0: '低', 1: '', 2: '中', 3: '', 4: '高' }" show-ticks="always" max="4" step="1" tick-size="4"></v-slider>

      <v-label>ニュアンス</v-label>
      <v-textarea v-model="form_data.nuance" rows="1" clearable counter auto-grow></v-textarea>

      <v-label>シチュエーション</v-label>
      <v-textarea v-model="form_data.situation" rows="1" clearable counter auto-grow></v-textarea>

      <v-label>備考</v-label>
      <v-textarea v-model="form_data.notes" rows="1" clearable counter auto-grow></v-textarea>

      <div class="d-flex justify-center">
        <v-btn @click="addContainer" :disabled="isAddButtonDisabled" width="30%" :prepend-icon="mdi_arrow_down_circle" color="primary">追加</v-btn>
      </div>

    </div>

    <div class="border-s-lg border-e-lg border-t-lg border-b rounded-t-lg mt-4 text-center bg-primary" style="font-size: 16px;">
      追加チャンク一覧
    </div>
    <div class="border-s-lg border-e-lg border-b-lg rounded-b-lg pa-4 mb-4">
      <template v-for="(chunk_row, index) in form_data_list">
        <ChunkWithTrashCompo :key="chunk_row.id" :props_chunk_row="chunk_row" v-if="true"
          @save="saveChangeChunkRow" @delete="deleteChunkRow">
          <template #index>{{ index + 1 }}</template>
        </ChunkWithTrashCompo>
      </template>

      <div class="d-flex justify-center mt-4">
        <v-btn @click="submitFormData" :disabled="isSubmitButtonDisabled" width="30%" color="primary">送信</v-btn>
      </div>

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
import { mdiArrowDownCircle, mdiPuzzle } from "@mdi/js";
import ChunkWithTrashCompo from "../../components/ChunkWithTrash-Compo.vue";

export default {
  components: {
    ChunkWithTrashCompo,
    SvgIcon,
  },
  data() {
    return {
      mdi_arrow_down_circle: mdiArrowDownCircle,
      mdi_puzzle: mdiPuzzle,

      form_data: {
        learning_chunk: '',
        translating_chunk: '',
        politeness: 2,
        nuance: '',
        situation: '',
        notes: ''
      },
      form_data_list: [],
      folder_name: "",
      fid: this.$route.query.fid,

      snackbar: false,
      snackbarMessage: '',
      snackbarColor: 'success',
      snackbarTimeout: 3000
    };
  },
  computed: {
    isAddButtonDisabled() {
      return !this.form_data.learning_chunk;
    },
    isSubmitButtonDisabled() {
      return this.form_data_list.length === 0;
    },
    politenessColor() {
      const politeness = this.form_data.politeness;
      if (politeness === 0) return 'indigo';
      if (politeness === 1) return 'light-blue';
      if (politeness === 2) return 'green';
      if (politeness === 3) return 'orange';
      if (politeness === 4) return 'red';
      return 'grey';
    }
  },
  methods: {
    addContainer() {
      const newChunk = { ...this.form_data };
      this.form_data_list.push(newChunk);

      this.form_data = {
        learning_chunk: '',
        translating_chunk: '',
        politeness: 2,
        nuance: '',
        situation: '',
        notes: ''
      };

      this.showSnackbar('チャンクを追加しました。', 'success');
    },
    saveChangeChunkRow(edited_chunk) {
      const index_to_update = this.form_data_list.findIndex(chunk => chunk.id === edited_chunk.id);

      if (index_to_update !== -1) {
        this.form_data_list.splice(index_to_update, 1, edited_chunk);
        this.showSnackbar('チャンクの変更内容を保存しました。', 'success');
      }
    },
    deleteChunkRow(chunkToDelete) {
      const indexToDelete = this.form_data_list.indexOf(chunkToDelete);
      if (indexToDelete !== -1) {
        this.form_data_list.splice(indexToDelete, 1);
        this.showSnackbar('チャンクを削除しました。', 'success');
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
          this.showSnackbar('フォルダが見つかりませんでした。', 'error');
        }
      } catch (error) {
        console.error("Fetch error:", error);
        this.showSnackbar('フォルダの読み込みに失敗しました。', 'error');
      }
    },
    async submitFormData() {
      const formDataJSON = JSON.stringify({ form_data_list: this.form_data_list });

      try {
        const response = await fetch(`/api/chunks/list/add?fid=${this.fid}`, {
          method: "POST",
          headers: {
            'Content-Type': 'application/json'
          },
          body: formDataJSON,
        });

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        const data = await response.json();
        console.log("Data submitted successfully:", data);
        this.showSnackbar('データが送信されました。', 'success');
        window.location.href = `/chunks/list?fid=${this.fid}`;
      } catch (error) {
        console.error("Error submitting data:", error);
        this.showSnackbar('データの送信に失敗しました。', 'error');
      }
    },
    showSnackbar(message, color) {
      this.snackbarMessage = message;
      this.snackbarColor = color;
      this.snackbar = true;
    },
    toBack() {
      this.$router.go(-1);
    },
  },
  async mounted() {
    await this.fetchFolderName();
  }
};
</script>
