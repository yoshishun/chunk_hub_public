<template>
  <div @mouseover="isHovered = true" @mouseleave="isHovered = false" :class="{ 'hover-effect': isHovered }"
    :style="{ backgroundColor: isHovered ? 'rgba(55,55,55,1)' : 'rgba(33,33,33,1)' }"
    style="word-break: break-word; width: 100%;" class="my-3 d-flex rounded-lg">
    
    <div name="index" class="border rounded-s-lg d-flex align-center justify-center" style="width: 40px;">
      <slot name="index" class="fontsize-14">インデックス</slot>
    </div>

    <template v-if="$vuetify.display.xs">
      <div name="body" class="d-flex flex-column" style="width: calc(100% - 100px);">
        
        <div name="learning" class="border d-flex align-center pa-1 fontsize-14">
          <span v-html="replaceNewLines(props_chunk_row.learning_chunk)"></span>
        </div>
        
        <div name="translating" class="border d-flex align-center pa-1 fontsize-14">
          <span v-html="replaceNewLines(props_chunk_row.translating_chunk)"></span>
        </div>
        <div class="d-flex" style="width: 100%;">
          <div v-for="i in 4" :key="i"
            :style="{ width: '25%', backgroundColor: i <= local_chunk_row.politeness ? politenessColor : 'rgba(33,33,33,1)' }"
            class="pt-1 border-b"></div>
        </div>
      </div>
    </template>

    <template v-else>
      <div name="body" class="d-flex flex-column" style="width: calc(100% - 120px);">
        <div class="d-flex" style="height: 100%;">
          
          <div name="learning" class="border d-flex align-center pa-1 fontsize-14" style="width: 50%;">
            <span v-html="replaceNewLines(props_chunk_row.learning_chunk)"></span>
          </div>
          
          <div name="translating" class="border d-flex align-center pa-1 fontsize-14" style="width: 50%;">
            <span v-html="replaceNewLines(props_chunk_row.translating_chunk)"></span>
          </div>
        </div>
        <div class="d-flex">
          <div v-for="i in 4" :key="i"
            :style="{ width: '25%', backgroundColor: i <= local_chunk_row.politeness ? politenessColor : 'rgba(33,33,33,1)' }"
            class="pt-1 border-b"></div>
        </div>
      </div>
    </template>

    <div name="detail" style="width: 80px;">
      <div name="top" class="border rounded-te-lg text-end pr-1 fontsize-14" style="height: 20px;">
        {{ props_chunk_row.pronounced_count }}
      </div>

      <v-dialog v-model="dialog" max-width="600" style="font-size: 12px;">
        <template v-slot:activator="{ props: activatorProps }">
          
          <div name="bottom" class="border rounded-be-lg d-flex align-center justify-center"
            style="cursor: pointer; height:calc(100% - 20px);" v-bind="activatorProps" @click="openDialog">
            <svg-icon type="mdi" :path="mdiMenu"></svg-icon>
          </div>
        </template>

        <v-card>
          <v-card-title class="text-center" style="font-size: 16px;">詳細</v-card-title>

          <div class="d-flex flex-column px-2">
            <div class="d-flex">
              <div class="border-t border-b border-e border-s-lg pl-1 d-flex align-center" style="width: 110px">
                チャンク
              </div>
              <div class="border-t border-b border-e-lg pa-2 d-flex align-center" style="width: calc(100% - 110px);">
                <span v-html="replaceNewLines(local_chunk_row.learning_chunk)"></span>
              </div>
            </div>
            <div class="d-flex">
              <div class="border-b-lg border-s-lg border-e rounded-bs-lg pl-1 d-flex align-center" style="width: 110px">
                翻訳文
              </div>
              <div class="border-b-lg border-e-lg rounded-be-lg pa-2 d-flex align-center"
                style="width: calc(100% - 110px)">
                <span v-html="replaceNewLines(local_chunk_row.translating_chunk)"></span>
              </div>
            </div>

            <div class="d-flex mt-4">
              <div class="border-t-lg border-e border-s-lg rounded-ts-lg pl-1 d-flex align-center" style="width: 110px">
                丁寧度
              </div>
              <div class="border-t-lg border-e-lg rounded-te-lg d-flex align-center justify-center px-2"
                style="width: calc(100% - 110px)">
                <v-slider v-model="local_chunk_row.politeness" :color="politenessColor" show-ticks="always" max="4"
                  step="1" tick-size="4" readonly hide-details="auto"></v-slider>
              </div>
            </div>

            <div class="d-flex">
              <div class="border-t border-b border-e border-s-lg pl-1 d-flex align-center" style="width: 110px">
                ニュアンス
              </div>
              <div class="border-t border-b border-e-lg pa-2 d-flex align-center" style="width: calc(100% - 110px);">
                <span v-html="replaceNewLines(local_chunk_row.nuance)"></span>
              </div>
            </div>

            <div class="d-flex">
              <div class="border-t border-b border-e border-s-lg pl-1 d-flex align-center" style="width: 110px">
                シチュエーション
              </div>
              <div class="border-t border-b border-e-lg pa-2 d-flex align-center" style="width: calc(100% - 110px);">
                <span v-html="replaceNewLines(local_chunk_row.situation)"></span>
              </div>
            </div>

            <div class="d-flex">
              <div class="border-b-lg border-s-lg border-e rounded-bs-lg pl-1 d-flex align-center" style="width: 110px">
                備考
              </div>
              <div class="border-b-lg border-e-lg rounded-be-lg pa-2 d-flex align-center"
                style="width: calc(100% - 110px)">
                <span v-html="replaceNewLines(local_chunk_row.notes)"></span>
              </div>
            </div>

          </div>

          
          <v-container class="d-flex align-center">
            <v-autocomplete v-model="selectedFolder" label="移動先のフォルダを選択" :items="folders"
              item-title="name" item-value="id" clearable>
            </v-autocomplete>
            <v-btn icon @click="moveChunk" color="primary">
              <svg-icon type="mdi" :path="mdi_folder_move"></svg-icon>
            </v-btn>
          </v-container>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn text="Close" variant="plain" @click="dialog = false" color="primary"></v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-snackbar v-model="snackbar" :timeout="snackbarTimeout" :color="snackbarColor">
        {{ snackbarMessage }}
        <template v-slot:action="{ attrs }">
          <v-btn color="white" text @click="snackbar = false" v-bind="attrs">Close</v-btn>
        </template>
      </v-snackbar>
    </div>
  </div>
</template>

<script>
import SvgIcon from '@jamescoyle/vue-icon';
import { mdiMenu, mdiFolderMove } from '@mdi/js';
import axios from 'axios';
import { getPolitenessColor } from '@/utils/politenessUtils';

export default {
  components: {
    SvgIcon
  },
  props: {
    props_chunk_row: Object,
  },
  data() {
    return {
      mdiMenu,
      mdi_folder_move: mdiFolderMove,

      dialog: false,
      local_chunk_row: { ...this.props_chunk_row },
      isHovered: false,
      folders: [],
      selectedFolder: null,
      snackbar: false,
      snackbarMessage: '',
      snackbarColor: 'success',
      snackbarTimeout: 3000
    };
  },
  watch: {
    props_chunk_row: {
      handler(newValue) {
        this.local_chunk_row = { ...newValue };
      },
      deep: true
    }
  },
  computed: {
    politenessColor() {
      return getPolitenessColor(this.local_chunk_row.politeness);
    }
  },
  methods: {
    replaceNewLines(text) {
      return text ? text.replace(/\n/g, '<br>') : '';
    },
    openDialog() {
      this.dialog = true;
      this.loadFolders();
    },
    loadFolders() {
      axios.get('/api/chunk_folders/list?fclass=1')
        .then(response => {
          this.folders = response.data.filter(folder => folder.id !== this.local_chunk_row.folder_id);
        })
        .catch(error => {
          console.error(error);
          this.showSnackbar('フォルダの読み込みに失敗しました。', 'error');
        });
    },
    moveChunk() {
      if (!this.selectedFolder) {
        this.showSnackbar('フォルダを選択してください。', 'error');
        return;
      }

      axios.post('/api/chunks/move', {
        chunk_ids: [this.local_chunk_row.id],
        target_folder_id: this.selectedFolder
      })
        .then(() => {
          this.showSnackbar('チャンクが移動されました。', 'success');
          this.dialog = false;
          this.$emit('chunk-moved', this.local_chunk_row.id); 
        })
        .catch(error => {
          console.error(error);
          this.showSnackbar('チャンクの移動に失敗しました。', 'error');
        });
    },
    showSnackbar(message, color) {
      this.snackbarMessage = message;
      this.snackbarColor = color;
      this.snackbar = true;
    }
  }
};
</script>

<style scoped>
.fontsize-14 {
  font-size: 14px;
}

.hover-effect {
  transition: background-color 0.3s;
}
</style>
