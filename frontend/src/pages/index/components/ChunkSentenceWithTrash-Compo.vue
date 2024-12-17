<template>
  <div @mouseover="isHovered = true" @mouseleave="isHovered = false" :class="{ 'hover-effect': isHovered }"
    class="rounded-lg" :style="{ backgroundColor: isHovered ? 'rgba(55,55,55,1)' : 'rgba(33,33,33,1)' }">
    
    <div style="word-break: break-word; width: 100%; font-size: 14px;" class="my-3 d-flex">
      
      <div name="index" class="border rounded-s-lg d-flex align-center justify-center" style="width: 40px;">
        <slot name="index">インデックス</slot>
      </div>

      
      
      <template v-if="$vuetify.display.xs">
        <div name="body" class="d-flex flex-column" style="width: calc(100% - 100px);">
          
          <div name="learning" class="border d-flex flex-wrap align-center">
            <template v-if="props_chunk_sentence_obj.used_chunks.length !== 0">
              <template v-for="used_chunk in props_chunk_sentence_obj.used_chunks">
                <v-chip size="x-small" class="ma-1" :key="used_chunk.chunk_id" v-if="true"
                  @click="openChunkDetailDialog(used_chunk)">{{ used_chunk.title }}</v-chip>
              </template>
            </template>
            <template v-else>
              <v-chip class="ma-1" color="grey" size="x-small">設定無し</v-chip>
            </template>
          </div>
          
          <div name="learning" class="border d-flex align-center pa-1">
            <span v-html="replaceNewLines(props_chunk_sentence_obj.chunk_sentence)"></span>
          </div>
          
          <div name="translating" class="border d-flex align-center pa-1">
            <span v-html="replaceNewLines(props_chunk_sentence_obj.translating_sentence)"></span>
          </div>
          
          <div class="d-flex" style="width: 100%;">
            <div v-for="i in 40" :key="i"
              :style="{ width: '2.5%', backgroundColor: i <= computedPoliteness * 10 ? politenessColor : 'rgba(33,33,33,1)' }"
              class="pt-1 border-b"></div>
          </div>
        </div>
      </template>

      
      <template v-else>
        <div name="body" class="d-flex flex-column" style="width: calc(100% - 120px);">
          
          <div name="learning" class="border d-flex flex-wrap align-center py-1 pl-1">
            <template v-if="props_chunk_sentence_obj.used_chunks.length !== 0">
              <template v-for="used_chunk in props_chunk_sentence_obj.used_chunks">
                <v-chip size="x-small" class="ma-1" :key="used_chunk.chunk_id" v-if="true"
                  @click="openChunkDetailDialog(used_chunk)">{{ used_chunk.title }}</v-chip>
              </template>
            </template>
            <template v-else>
              <v-chip class="ma-1" color="grey" size="x-small">設定無し</v-chip>
            </template>
          </div>

          <div class="d-flex">
            
            <div name="learning" class="border d-flex align-center pa-1" style="width: 50%;">
              <span v-html="replaceNewLines(props_chunk_sentence_obj.chunk_sentence)"></span>
            </div>

            
            <div name="translating" class="border d-flex align-center pa-1" style="width: 50%;">
              <span v-html="replaceNewLines(props_chunk_sentence_obj.translating_sentence)"></span>
            </div>
          </div>
          
          <div class="d-flex" style="width: 100%;">
            <div v-for="i in 40" :key="i"
              :style="{ width: '2.5%', backgroundColor: i <= computedPoliteness * 10 ? politenessColor : 'rgba(33,33,33,1)' }"
              class="pt-1 border-b"></div>
          </div>
        </div>
      </template>

      
      <div name="detail" style="width: 80px;">
        
        <div name="top" class="border rounded-te-lg text-end pr-1" style="height: 20px;">
          {{ props_chunk_sentence_obj.pronounced_count }}
        </div>

        
        <div class="d-flex" style="cursor: pointer; height:calc(100% - 20px);">

          
          <v-dialog v-model="dialog" max-width="600">
            <template v-slot:activator="{ props: activatorProps }">
              
              <div name="bottom" class="border d-flex align-center justify-center" style="width: 50%;"
                v-bind="activatorProps" @click="openDialog">
                <svg-icon type="mdi" :path="mdi_file_edit"></svg-icon>
              </div>
            </template>

            <v-card>
              <v-card-title>編集</v-card-title>

              <v-divider></v-divider>

              <v-card-text>
                <v-row dense>
                  <v-col cols="12">
                    <v-textarea v-model="edited_data.chunk_sentence" label="チャンク" rows="1" counter clear
                      auto-grow></v-textarea>
                  </v-col>

                  <v-col cols="12">
                    <v-textarea v-model="edited_data.translating_sentence" label="翻訳文" rows="1" counter clear
                      auto-grow></v-textarea>
                  </v-col>

                  <v-col cols="12">
                    <div class="d-flex align-center">
                      <v-autocomplete v-model="edited_data.used_chunks" label="使用チャンク" :items="props_use_chunk_list"
                        item-value="value" item-title="title" multiple clearable chips :return-object="true"
                        :menu-props="{ auto: true, closeOnClick: false }">
                      </v-autocomplete>
                      <v-btn icon @click="openAddChunkDialog" color="primary">
                        <svg-icon type="mdi" :path="mdi_plus"></svg-icon>
                      </v-btn>
                    </div>
                  </v-col>

                  <v-col cols="12">
                    <v-slider v-model="computedPoliteness" :color="politenessColor" label="丁寧度(自動計算)" class="w-90"
                      :ticks="{ 0: '低', 1: '', 2: '中', 3: '', 4: '高' }" show-ticks="always" max="4" step="0.1"
                      tick-size="4" readonly></v-slider>
                  </v-col>

                  <v-col cols="12">
                    <v-textarea v-model="edited_data.situation" label="シチュエーション" rows="1" clearable counter
                      auto-grow></v-textarea>
                  </v-col>

                  <v-col cols="12">
                    <v-textarea v-model="edited_data.notes" label="備考" rows="1" clearable counter
                      auto-grow></v-textarea>
                  </v-col>
                </v-row>
              </v-card-text>

              <v-divider></v-divider>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn text="Close" variant="plain" @click="dialog = false">Close</v-btn>
                <v-btn color="primary" text="Save" variant="tonal" @click="saveChanges">Save</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>

          
          <div class="border rounded-be-lg d-flex align-center justify-center" style="width: 50%;" @click="deleteChunk">
            <svg-icon type="mdi" :path="mdi_trash_can_outline"></svg-icon>
          </div>

        </div>
      </div>
    </div>

    
    <v-dialog v-model="add_chunk_dialog" max-width="500">
      <v-card>
        <v-card-title>
          <span class="headline">新規チャンク追加</span>
        </v-card-title>
        <v-card-text>
          <v-autocomplete v-model="save_chunk_folder" label="保存先フォルダ" :items="props_chunk_folder_list"
            item-value="value" item-title="title" clearable :return-object="true"></v-autocomplete>
          <v-textarea v-model="new_chunk_title" label="チャンク" @input="checkForDuplicate" :error="duplicate_error"
            rows="1" clearable counter auto-grow></v-textarea>
          <v-textarea v-model="new_chunk_translation" label="翻訳文" rows="1" clearable counter auto-grow></v-textarea>
          <v-slider label="丁寧度(自動計算)" class="w-90" v-model="new_chunk_politeness" :color="newPolitenessColor"
            :ticks="{ 0: '低', 1: '', 2: '中', 3: '', 4: '高' }" show-ticks="always" max="4" step="1"
            tick-size="4"></v-slider>
          <v-textarea v-model="new_chunk_nuance" label="ニュアンス" rows="1" clearable counter auto-grow></v-textarea>
          <v-textarea v-model="new_chunk_situation" label="シチュエーション" rows="1" clearable counter auto-grow></v-textarea>
          <v-textarea v-model="new_chunk_notes" label="備考" rows="1" clearable counter auto-grow></v-textarea>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" text @click="addNewChunk"
            :disabled="!new_chunk_title || !save_chunk_folder || duplicate_error">追加</v-btn>
          <v-btn color="grey" text @click="add_chunk_dialog = false">キャンセル</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    
    <v-dialog v-model="chunkDetailDialog" max-width="600" style="font-size: 12px;">
      <v-card>
        <v-card-title class="text-center" style="font-size: 16px;">使用チャンク(詳細)</v-card-title>
        <v-card-text>
          <div class="d-flex flex-column px-2">
            <div class="d-flex">
              <div class="border-t-lg border-e border-s-lg border-b rounded-ts-lg pl-1 d-flex align-center"
                style="width: 110px">
                チャンク
              </div>
              <div class="border-t-lg border-e-lg rounded-te-lg border-b pa-2 d-flex align-center"
                style="width: calc(100% - 110px)">
                <span v-html="replaceNewLines(selectedChunk.value.learning_chunk)"></span>
              </div>
            </div>
            <div class="d-flex">
              <div class="border-b-lg border-s-lg border-e rounded-bs-lg pl-1 d-flex align-center" style="width: 110px">
                翻訳文
              </div>
              <div class="border-b-lg border-e-lg rounded-be-lg pa-2 d-flex align-center"
                style="width: calc(100% - 110px)">
                <span v-html="replaceNewLines(selectedChunk.value.translating_chunk)"></span>
              </div>
            </div>
            <div class="d-flex mt-4">
              <div class="border-t-lg border-e border-s-lg rounded-ts-lg pl-1 d-flex align-center" style="width: 110px">
                丁寧度
              </div>
              <div class="border-t-lg border-e-lg rounded-te-lg d-flex align-center justify-center px-2"
                style="width: calc(100% - 110px)">
                <v-slider v-model="selectedChunk.value.politeness"
                  :color="displayPolitenessColor(selectedChunk.value.politeness)" show-ticks="always" max="4" step="1"
                  hide-details="auto" tick-size="4" readonly></v-slider>
              </div>
            </div>
            <div class="d-flex">
              <div class="border-t border-b border-e border-s-lg pl-1 d-flex align-center" style="width: 110px">
                ニュアンス
              </div>
              <div class="border-t border-b border-e-lg pa-2 d-flex align-center" style="width: calc(100% - 110px);">
                <span v-html="replaceNewLines(selectedChunk.value.nuance)"></span>
              </div>
            </div>
            <div class="d-flex">
              <div class="border-t border-b border-e border-s-lg pl-1 d-flex align-center" style="width: 110px">
                シチュエーション
              </div>
              <div class="border-t border-b border-e-lg pa-2 d-flex align-center" style="width: calc(100% - 110px);">
                <span v-html="replaceNewLines(selectedChunk.value.situation)"></span>
              </div>
            </div>
            <div class="d-flex">
              <div class="border-b-lg border-s-lg border-e rounded-bs-lg pl-1 d-flex align-center" style="width: 110px">
                備考
              </div>
              <div class="border-b-lg border-e-lg rounded-be-lg pa-2 d-flex align-center"
                style="width: calc(100% - 110px)">
                <span v-html="replaceNewLines(selectedChunk.value.notes)"></span>
              </div>
            </div>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="chunkDetailDialog = false">閉じる</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </div>
</template>

<script>
import SvgIcon from '@jamescoyle/vue-icon';
import { mdiFileEdit, mdiTrashCanOutline, mdiPlus } from '@mdi/js';
import { getPolitenessColor } from '@/utils/politenessUtils'; 

export default {
  props: {
    props_chunk_sentence_obj: Object,
    props_use_chunk_list: Array,
    props_chunk_folder_list: Array
  },
  components: {
    SvgIcon
  },
  data() {
    return {
      
      mdi_file_edit: mdiFileEdit,
      mdi_trash_can_outline: mdiTrashCanOutline,
      mdi_plus: mdiPlus,

      dialog: false,
      add_chunk_dialog: false,
      new_chunk_title: '',
      save_chunk_folder: null,
      edited_data: { ...this.props_chunk_sentence_obj },
      duplicate_error: false,
      new_chunk_translation: '',
      new_chunk_politeness: 2,
      new_chunk_nuance: "",
      new_chunk_situation: "",
      new_chunk_notes: "",
      isHovered: false,
      chunkDetailDialog: false,
      selectedChunk: {},
    };
  },
  computed: {
    computedPoliteness() {
      return parseFloat(this.calculatePoliteness(this.edited_data.used_chunks)).toFixed(1);
    },
    politenessColor() {
      return getPolitenessColor(this.computedPoliteness); 
    },
    newPolitenessColor() {
      return getPolitenessColor(this.new_chunk_politeness); 
    }
  },
  methods: {
    replaceNewLines(text) {
      return text ? text.replace(/\n/g, '<br>') : '';
    },
    openDialog() {
      this.dialog = true;
      this.edited_data = { ...this.props_chunk_sentence_obj };

      const used_chunks = [];
      this.edited_data.used_chunks.forEach(used_chunk => {
        const found_chunk = this.props_use_chunk_list.find(
          item => item.value.chunk_id === used_chunk.value.chunk_id
        );
        if (found_chunk) {
          used_chunks.push(found_chunk);
        }
      });
      this.edited_data.used_chunks = used_chunks;
    },
    openAddChunkDialog() {
      this.add_chunk_dialog = true;
      this.new_chunk_title = '';
      this.new_chunk_translation = '';
      this.save_chunk_folder = null;
      this.duplicate_error = false;
    },
    checkForDuplicate() {
      const duplicate = this.edited_data.used_chunks.some(chunk => chunk.title === this.new_chunk_title);
      this.duplicate_error = duplicate;
    },
    addNewChunk() {
      if (this.new_chunk_title && this.save_chunk_folder && !this.duplicate_error) {
        const new_chunk = {
          title: this.new_chunk_title,
          value: {
            folder_id: this.save_chunk_folder.value.folder_id,
            chunk_id: '',
            learning_chunk: this.new_chunk_title,
            translating_chunk: this.new_chunk_translation,
            politeness: this.new_chunk_politeness,
            nuance: this.new_chunk_nuance,
            situation: this.new_chunk_situation,
            notes: this.new_chunk_notes
          }
        };
        const new_chunk_proxy = new Proxy(new_chunk, {});
        this.edited_data.used_chunks.push(new_chunk_proxy);

        this.$emit('addChunk', new_chunk_proxy);
        this.new_chunk_title = '';
        this.new_chunk_translation = '';
        this.save_chunk_folder = null;
        this.new_chunk_politeness = 2;
        this.new_chunk_nuance = "";
        this.new_chunk_situation = "";
        this.new_chunk_notes = "";
        this.add_chunk_dialog = false;
      }
    },
    saveChanges() {
      this.edited_data.politeness = this.computedPoliteness;
      this.$emit('save', this.edited_data);
      this.dialog = false;
    },
    deleteChunk() {
      this.$emit('delete', this.props_chunk_sentence_obj);
    },
    calculatePoliteness(used_chunks) {
      if (!used_chunks || used_chunks.length === 0) {
        return 0;
      }
      const politenessSum = used_chunks.reduce((sum, chunk) => sum + (chunk.value.politeness || 0), 0);
      return (politenessSum / used_chunks.length).toFixed(1);
    },
    openChunkDetailDialog(chunk) {
      this.selectedChunk = chunk;
      this.chunkDetailDialog = true;
    },
    displayPolitenessColor(politeness) {
      return getPolitenessColor(politeness); 
    }
  }
};
</script>

<style scoped>
.hover-effect {
  transition: background-color 0.3s;
}
</style>
