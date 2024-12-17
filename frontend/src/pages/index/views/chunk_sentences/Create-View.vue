<template>
  <v-container grid-list-xs>
    <h5 class="text-center">
      <svg-icon height="14px" width="14px" type="mdi" :path="mdi_lock_pattern"></svg-icon>
      {{ folder_name }}
    </h5>
    <h2 class="text-center">- チャンク文/フレーズ 作成 -</h2>

    <template v-if="$vuetify.display.xs">
      <h5 class="text-center mt-4" style="color: grey;">
        チャンク文/フレーズを作成します。
      </h5>
    </template>
    <template v-else>
      <h4 class="text-center mt-4" style="color: grey;">
        チャンク文/フレーズを作成します。
      </h4>
    </template>

    <v-divider class="mt-4"></v-divider>

    <div class="border-s-lg border-e-lg border-t-lg border-b rounded-t-lg mt-4 text-center bg-primary" style="font-size: 16px;">
      チャンク文/フレーズ入力
    </div>

    
    <div class="border-s-lg border-e-lg border-b-lg rounded-b-lg pa-4 mb-4">
      <v-textarea label="チャンク文/フレーズ" v-model="form_data.chunk_sentence" rows="1" clearable counter auto-grow></v-textarea>

      <v-textarea label="翻訳文" v-model="form_data.translating_sentence" rows="1" clearable counter auto-grow></v-textarea>

      
      <div class="d-flex align-center">
        <v-autocomplete v-model="form_data.used_chunks" label="使用チャンク" :items="use_chunk_list" item-value="value"
          item-title="title" multiple clearable chips :return-object="true"
          :menu-props="{ auto: true, closeOnClick: false }">
        </v-autocomplete>
        <v-btn icon @click="openAddChunkDialog" color="primary">
          <svg-icon type="mdi" :path="mdi_plus"></svg-icon>
        </v-btn>
      </div>

      <v-slider label="丁寧度(自動計算)" class="w-90" :color="politenessColor" v-model="computedPoliteness"
        :ticks="{ 0: '低', 1: '', 2: '中', 3: '', 4: '高' }" show-ticks="always" max="4" step="0.1" tick-size="4" readonly>
      </v-slider>

      <v-textarea label="シチュエーション" v-model="form_data.situation" rows="1" clearable counter auto-grow></v-textarea>

      <v-textarea label="備考" v-model="form_data.notes" rows="1" clearable counter auto-grow></v-textarea>

      
      <div class="d-flex justify-center">
        <v-btn @click="addContainer" :disabled="isAddButtonDisabled" width="30%" color="primary" :prepend-icon="mdi_arrow_down_circle">追加</v-btn>
      </div>
    </div>

    <div class="border-s-lg border-e-lg border-t-lg border-b rounded-t-lg mt-4 text-center bg-primary" style="font-size: 16px;">
      追加一覧
    </div>
    <div class="border-s-lg border-e-lg border-b-lg rounded-b-lg pa-4 mb-4">
      
      <template v-for="(chunk_sentence_obj, index) in form_data_list">
        <ChunkSentenceWithTrashCompo :key="chunk_sentence_obj.index" :props_chunk_sentence_obj="chunk_sentence_obj"
          :props_use_chunk_list="use_chunk_list" v-if="true" :props_chunk_folder_list="chunk_folder_list"
          @delete="deleteChunkRow" @addChunk="addChunk" @save="saveChangeChunkSentenceRow">
          <template #index>{{ index + 1 }}</template>
        </ChunkSentenceWithTrashCompo>
      </template>

      
      <div class="d-flex justify-center mt-4">
        <v-btn @click="submitFormData" :disabled="isSubmitButtonDisabled" width="30%" color="primary">送信</v-btn>
      </div>
    </div>

    
    <v-dialog v-model="add_chunk_dialog" max-width="500">
      <v-card>
        <v-card-title>
          <span class="headline">新規チャンク追加</span>
        </v-card-title>
        <v-card-text>
          <v-autocomplete v-model="save_chunk_folder" label="保存先フォルダ" :items="chunk_folder_list" item-value="value"
          item-title="title" clearable :return-object="true"></v-autocomplete>
          <v-textarea v-model="new_chunk_title" label="チャンクタイトル" @input="checkForDuplicate" :error="duplicate_error"
            rows="1" clearable counter auto-grow></v-textarea>
          <v-textarea v-model="new_chunk_translation" label="翻訳文" rows="1" clearable counter auto-grow></v-textarea>
          <v-slider label="丁寧度" class="w-90" v-model="new_chunk_politeness" :color="newPolitenessColor"
            :ticks="{ 0: '低', 1: '', 2: '中', 3: '', 4: '高' }" show-ticks="always" max="4" step="1"
            tick-size="4"></v-slider>
          <v-textarea v-model="new_chunk_nuance" label="ニュアンス" rows="1" clearable counter auto-grow></v-textarea>
          <v-textarea v-model="new_chunk_situation" label="シチュエーション" rows="1" clearable counter auto-grow></v-textarea>
          <v-textarea v-model="new_chunk_notes" label="備考" rows="1" clearable counter auto-grow></v-textarea>
          <v-alert v-if="duplicate_error" type="error" dense outlined>重複するチャンクがあります。</v-alert>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="addNewChunk"
            :disabled="!new_chunk_title || !save_chunk_folder || duplicate_error">追加</v-btn>
          <v-btn color="grey" text @click="add_chunk_dialog = false">キャンセル</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" :timeout="snackbar.timeout" top>
      {{ snackbar.text }}
    </v-snackbar>
  </v-container>
</template>

<script>
import SvgIcon from '@jamescoyle/vue-icon';
import { mdiArrowDownCircle, mdiLockPattern, mdiPlus } from "@mdi/js";
import ChunkSentenceWithTrashCompo from "../../components/ChunkSentenceWithTrash-Compo.vue";
import { getPolitenessColor } from '@/utils/politenessUtils'; 

export default {
  components: {
    ChunkSentenceWithTrashCompo,
    SvgIcon,
  },
  data() {
    return {
      mdi_arrow_down_circle: mdiArrowDownCircle,
      mdi_lock_pattern: mdiLockPattern,
      mdi_plus: mdiPlus,

      form_data: {
        index: 0,
        chunk_sentence: "",
        translating_sentence: "",
        used_chunks: [],
        situation: "",
        notes: "",
        politeness: 0, 
      },
      use_chunk_list: [],
      new_chunks: [], 
      chunk_folder_list: [], 

      folder_name: "", 
      form_data_list: [],
      fid: this.$route.query.fid,
      index: 0,

      add_chunk_dialog: false,
      new_chunk_title: "",
      new_chunk_translation: "",
      new_chunk_politeness: 2, 
      new_chunk_nuance: "",
      new_chunk_situation: "",
      new_chunk_notes: "",
      save_chunk_folder: null,
      duplicate_error: false,

      snackbar: {
        show: false,
        text: '',
        color: '',
        timeout: 3000,
      }
    };
  },
  methods: {
    addContainer() {
      this.form_data.politeness = parseFloat(this.computedPoliteness); 
      this.form_data.index = this.index++;
      this.form_data_list.push({ ...this.form_data });

      
      this.form_data = {
        chunk_sentence: "",
        translating_sentence: "",
        used_chunks: [],
        situation: "",
        notes: "",
        politeness: 0, 
      };

      this.showSnackbar('チャンク文/フレーズを追加しました。', 'success');
    },
    saveChangeChunkSentenceRow(edited_chunk_sentence) {
      const index_to_update = this.form_data_list.findIndex(chunk_sentence => chunk_sentence.index === edited_chunk_sentence.index);
      if (index_to_update !== -1) {
        this.form_data_list.splice(index_to_update, 1, edited_chunk_sentence);
      }
    },
    deleteChunkRow(chunk_to_delete) {
      const index_to_delete = this.form_data_list.indexOf(chunk_to_delete);
      if (index_to_delete !== -1) {
        this.form_data_list.splice(index_to_delete, 1);
      }
      this.showSnackbar('チャンク文/フレーズを削除しました。', 'info');
    },
    async submitFormData() {
      const form_data_json = JSON.stringify({ form_data_list: this.form_data_list, new_chunks: this.new_chunks });

      try {
        const response = await fetch(`/api/chunk_sentences/list/create?fid=${this.fid}`, {
          method: "POST",
          headers: {
            'Content-Type': 'application/json'
          },
          body: form_data_json,
        });

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        this.showSnackbar('データが正常に送信されました。', 'success');
        window.location.href = `/chunk_sentences/list?fid=${this.fid}`;
      } catch (error) {
        this.showSnackbar('データの送信中にエラーが発生しました。', 'error');
        console.error("Error submitting data:", error);
      }
    },
    checkForDuplicate() {
      this.duplicate_error = this.use_chunk_list.some(chunk => chunk.title === this.new_chunk_title);
    },
    calculatePoliteness(used_chunks) {
      if (!used_chunks || used_chunks.length === 0) {
        return 0;
      }
      const politenessSum = used_chunks.reduce((sum, chunk) => sum + (chunk.value.politeness || 0), 0);
      return (politenessSum / used_chunks.length).toFixed(1);
    },
    addChunk(new_chunk) {
      this.use_chunk_list.push(new_chunk);
      this.new_chunks.push(new_chunk);
    },
    addNewChunk() {
      if (this.new_chunk_title && this.save_chunk_folder && !this.duplicate_error) {
        const new_chunk = {
          title: this.new_chunk_title,
          value: {
            chunk_id: "",
            folder_id: this.save_chunk_folder.value.folder_id,
            learning_chunk: this.new_chunk_title,
            translating_chunk: this.new_chunk_translation,
            politeness: this.new_chunk_politeness,
            nuance: this.new_chunk_nuance,
            situation: this.new_chunk_situation,
            notes: this.new_chunk_notes,
          }
        };

        this.form_data.used_chunks.push(new_chunk);
        this.use_chunk_list.push(new_chunk);
        this.new_chunks.push(new_chunk);

        this.new_chunk_title = "";
        this.new_chunk_translation = "";
        this.save_chunk_folder = null;
        this.new_chunk_politeness = 2;
        this.new_chunk_nuance = "";
        this.new_chunk_situation = "";
        this.new_chunk_notes = "";
        this.add_chunk_dialog = false;

        this.showSnackbar('新しいチャンクを追加しました。', 'success');
      } else {
        this.showSnackbar('新しいチャンクの追加に失敗しました。', 'error');
      }
    },
    openAddChunkDialog() {
      this.add_chunk_dialog = true;
      this.new_chunk_title = "";
      this.new_chunk_translation = "";
      this.save_chunk_folder = null;
      this.duplicate_error = false;
    },
    async fetchChunkFolderList() {
      try {
        const response = await fetch(`/api/chunk_folders/list?fclass=1`, {
          method: "GET",
        });
        const data = await response.json();
        this.chunk_folder_list = data.map(item => {
          return {
            title: item.name,
            value: { folder_id: item.id, folder_name: item.name }
          };
        });
      } catch (error) {
        console.error("Fetch error:", error);
        this.showSnackbar('チャンクフォルダの取得に失敗しました。', 'error');
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
          await this.fetchChunkFolderList();
        } else {
          console.error("Folder not found");
          this.showSnackbar('フォルダが見つかりません。', 'error');
        }
      } catch (error) {
        console.error("Fetch error:", error);
        this.showSnackbar('フォルダ名の取得に失敗しました。', 'error');
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
            title: item.learning_chunk,
            value: { "chunk_id": item.id,
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
        this.showSnackbar('チャンクの取得に失敗しました。', 'error');
      }
    },
    async fetchData() {
      try {
        await this.fetchFolderName();
        await this.fetchChunks();
      } catch (error) {
        console.error("Fetch data error:", error);
        this.showSnackbar('データの取得に失敗しました。', 'error');
      }
    },
    showSnackbar(text, color) {
      this.snackbar.text = text;
      this.snackbar.color = color;
      this.snackbar.show = true;
    }
  },
  async mounted() {
    await this.fetchData();
  },
  computed: {
    isAddButtonDisabled() {
      return !this.form_data.chunk_sentence;
    },
    isSubmitButtonDisabled() {
      return this.form_data_list.length === 0;
    },
    computedPoliteness() {
      return parseFloat(this.calculatePoliteness(this.form_data.used_chunks)).toFixed(1);
    },
    politenessColor() {
      return getPolitenessColor(this.computedPoliteness); 
    },
    newPolitenessColor() {
      return getPolitenessColor(this.new_chunk_politeness); 
    }
  },
};
</script>
