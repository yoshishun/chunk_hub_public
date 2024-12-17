<template>
  <div @mouseover="isHovered = true" @mouseleave="isHovered = false" :class="{'hover-effect': isHovered}" class="rounded-lg" :style="{ backgroundColor: isHovered ? 'rgba(55,55,55,1)' : 'rgba(33,33,33,1)' }">
    <div style="word-break: break-word; width: 100%; font-size: 14px;" class="my-3 d-flex">
      <div name="index" class="border rounded-s-lg d-flex align-center justify-center" style="width: 40px;">
        <slot name="index">インデックス</slot>
      </div>

      <template v-if="$vuetify.display.xs">
        <div name="body" class="d-flex flex-column" style="width: calc(100% - 100px);">
          <div name="learning" class="border d-flex align-center pa-1">
            <span v-html="replaceNewLines(props_chunk_row.learning_chunk)"></span>
          </div>
          <div name="translating" class="border d-flex align-center pa-1">
            <span v-html="replaceNewLines(props_chunk_row.translating_chunk)"></span>
          </div>
          <div class="d-flex" style="width: 100%;">
            <div v-for="i in 4" :key="i"
              :style="{ width: '25%', backgroundColor: i <= props_chunk_row.politeness ? displayPolitenessColor : 'rgba(33,33,33,1)' }"
              class="pt-1 border-b"></div>
          </div>
        </div>
      </template>

      <template v-else>
        <div name="body" class="d-flex flex-column" style="width: calc(100% - 120px);">
          <div class="d-flex" style="height: 100%;">
            <div name="learning" class="border d-flex align-center pa-1" style="width: 50%;">
              <span v-html="replaceNewLines(props_chunk_row.learning_chunk)"></span>
            </div>
            <div name="translating" class="border d-flex align-center pa-1" style="width: 50%;">
              <span v-html="replaceNewLines(props_chunk_row.translating_chunk)"></span>
            </div>
          </div>
          <div class="d-flex">
            <div v-for="i in 4" :key="i"
              :style="{ width: '25%', backgroundColor: i <= props_chunk_row.politeness ? displayPolitenessColor : 'rgba(33,33,33,1)' }"
              class="pt-1 border-b"></div>
          </div>
        </div>
      </template>

      <div name="detail" style="width: 80px;">
        <div name="top" class="border rounded-te-lg text-end pr-1" style="height: 20px;">
          {{ props_chunk_row.pronounced_count }}
        </div>

        <div class="d-flex" style="cursor: pointer; height:calc(100% - 20px);">

          <v-dialog v-model="dialog" max-width="600">
            <template v-slot:activator="{ props: activator_props }">
              <div name="bottom" class="border d-flex align-center justify-center" style="width: 50%;" v-bind="activator_props" @click="openDialog">
                <svg-icon type="mdi" :path="mdi_file_edit"></svg-icon>
              </div>
            </template>

            <v-card>
              <v-card-title>編集</v-card-title>
              <v-divider></v-divider>
              <v-card-text>
                <v-row dense>
                  <v-col cols="12">
                    <v-label>チャンク</v-label>
                    <v-textarea v-model="edited_chunk.learning_chunk" clear rows="1" counter auto-grow></v-textarea>
                  </v-col>
                  <v-col cols="12">
                    <v-label>翻訳文</v-label>
                    <v-textarea v-model="edited_chunk.translating_chunk" clear rows="1" counter auto-grow></v-textarea>
                  </v-col>
                  <v-col cols="12">
                    <v-label>丁寧度</v-label>
                    <v-slider v-model="edited_chunk.politeness" :color="editPolitenessColor" class="w-90" :ticks="{ 0: '低', 1: '', 2: '中', 3: '', 4: '高' }" show-ticks="always" max="4" step="1" tick-size="4"></v-slider>
                  </v-col>
                  <v-col cols="12">
                    <v-label>ニュアンス</v-label>
                    <v-textarea v-model="edited_chunk.nuance" rows="1" clearable counter auto-grow></v-textarea>
                  </v-col>
                  <v-col cols="12">
                    <v-label>シチュエーション</v-label>
                    <v-textarea v-model="edited_chunk.situation" rows="1" clearable counter auto-grow></v-textarea>
                  </v-col>
                  <v-col cols="12">
                    <v-label>備考</v-label>
                    <v-textarea v-model="edited_chunk.notes" rows="1" clearable counter auto-grow></v-textarea>
                  </v-col>
                </v-row>
              </v-card-text>
              <v-divider></v-divider>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn text="Close" variant="plain" @click="dialog = false" color="primary"></v-btn>
                <v-btn color="primary" text="Save" variant="tonal" @click="saveChanges">保存</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>

          <div class="border rounded-be-lg d-flex align-center justify-center" style="width: 50%;" @click="deleteChunk">
            <svg-icon type="mdi" :path="mdi_trash_can_outline"></svg-icon>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SvgIcon from '@jamescoyle/vue-icon';
import { mdiFileEdit, mdiTrashCanOutline } from '@mdi/js';

export default {
  props: {
    props_chunk_row: Object,
  },
  components: {
    SvgIcon
  },
  data() {
    return {
      mdi_file_edit: mdiFileEdit,
      mdi_trash_can_outline: mdiTrashCanOutline,
      dialog: false,
      isHovered: false,
      edited_chunk: {
        id: '',
        learning_chunk: '',
        translating_chunk: '',
        politeness: 0,
        nuance: '',
        situation: '',
        notes: '',
        pronounced_count: 0, 
      }
    }
  },
  computed: {
    displayPolitenessColor() {
      const politeness = this.props_chunk_row.politeness;
      if (politeness === 0) return '#3F51B5'; 
      if (politeness === 1) return '#03A9F4'; 
      if (politeness === 2) return '#4CAF50'; 
      if (politeness === 3) return '#FF9800'; 
      if (politeness === 4) return '#F44336'; 
      return 'grey';
    },
    editPolitenessColor() {
      const politeness = this.edited_chunk.politeness;
      if (politeness === 0) return '#3F51B5'; 
      if (politeness === 1) return '#03A9F4'; 
      if (politeness === 2) return '#4CAF50'; 
      if (politeness === 3) return '#FF9800'; 
      if (politeness === 4) return '#F44336'; 
      return 'grey';
    }
  },
  methods: {
    replaceNewLines(text) {
      return text ? text.replace(/\n/g, '<br>') : '';
    },
    openDialog() {
      this.edited_chunk = {
        id: this.props_chunk_row.id,
        learning_chunk: this.props_chunk_row.learning_chunk,
        translating_chunk: this.props_chunk_row.translating_chunk,
        politeness: this.props_chunk_row.politeness,
        nuance: this.props_chunk_row.nuance,
        situation: this.props_chunk_row.situation,
        notes: this.props_chunk_row.notes,
        pronounced_count: this.props_chunk_row.pronounced_count, 
      };
      this.dialog = true;
    },
    saveChanges() {
      this.$emit('save', this.edited_chunk);
      this.dialog = false;
    },
    deleteChunk() {
      this.$emit('delete', this.props_chunk_row);
    }
  },
};
</script>

<style scoped>
  .hover-effect {
    transition: background-color 0.3s;
  }
</style>
