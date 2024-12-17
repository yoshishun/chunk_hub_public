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
                  @click="openChunkDetailDialog(used_chunk)">
                  {{ used_chunk.title }}
                </v-chip>
              </template>
            </template>
            <template v-else>
              <v-chip class="ma-1" color="grey" size="x-small">
                設定無し
              </v-chip>
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
                  @click="openChunkDetailDialog(used_chunk)">
                  {{ used_chunk.title }}
                </v-chip>
              </template>
            </template>
            <template v-else>
              <v-chip class="ma-1" color="grey" size="x-small">
                設定無し
              </v-chip>
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

          <v-dialog v-model="dialog" max-width="600" style="font-size: 12px;">
            <template v-slot:activator="{ props: activatorProps }">
              
              <div name="bottom" class="border d-flex align-center justify-center" style="width: 50%;"
                v-bind="activatorProps" @click="openDialog">
                <svg-icon type="mdi" :path="mdi_menu"></svg-icon>
              </div>
            </template>

            <v-card>
              <v-card-title class="text-center" style="font-size: 16px;">詳細</v-card-title>

              <div class="d-flex flex-column px-2">
                <div class="d-flex">
                  <div class="border-t-lg border-e border-s-lg rounded-ts-lg pl-1 d-flex align-center"
                    style="width: 110px">
                    使用チャンク
                  </div>
                  <div class="border-t-lg border-e-lg rounded-te-lg d-flex flex-wrap align-center"
                    style="width: calc(100% - 110px)">
                    <template v-if="local_chunk_sentence_obj.used_chunks.length !== 0">
                      <template v-for="used_chunk in local_chunk_sentence_obj.used_chunks">
                        <v-chip size="small" class="ma-1" @click="openChunkDetailDialog(used_chunk)" :key="used_chunk.chunk_id" v-if="true">
                          {{ used_chunk.title }}
                        </v-chip>
                      </template>
                    </template>
                    <template v-else>
                      <v-chip class="ma-1" color="grey" size="small">
                        設定無し
                      </v-chip>
                    </template>
                  </div>
                </div>

                <div class="d-flex">
                  <div class="border-t border-b border-e border-s-lg pl-1 d-flex align-center" style="width: 110px">
                    チャンク文/<br>フレーズ
                  </div>
                  <div class="border-t border-b border-e-lg pa-2 d-flex align-center"
                    style="width: calc(100% - 110px);">
                    <span v-html="replaceNewLines(local_chunk_sentence_obj.chunk_sentence)"></span>
                  </div>
                </div>
                <div class="d-flex">
                  <div class="border-b-lg border-s-lg border-e rounded-bs-lg pl-1 d-flex align-center"
                    style="width: 110px">
                    翻訳文
                  </div>
                  <div class="border-b-lg border-e-lg rounded-be-lg pa-2 d-flex align-center"
                    style="width: calc(100% - 110px)">
                    <span v-html="replaceNewLines(local_chunk_sentence_obj.translating_sentence)"></span>
                  </div>
                </div>

                <div class="d-flex mt-4">
                  <div class="border-t-lg border-e border-s-lg rounded-ts-lg pl-1 d-flex align-center"
                    style="width: 110px">
                    丁寧度<br>(自動計算)
                  </div>
                  <div class="border-t-lg border-e-lg rounded-te-lg d-flex align-center justify-center px-2"
                    style="width: calc(100% - 110px)">
                    <v-slider v-model="computedPoliteness" :color="politenessColor"
                      :ticks="{ 0: '低', 1: '', 2: '中', 3: '', 4: '高' }" show-ticks="always" max="4" step="0.1"
                      tick-size="4" readonly></v-slider>
                  </div>
                </div>

                <div class="d-flex">
                  <div class="border-t border-b border-e border-s-lg pl-1 d-flex align-center" style="width: 110px">
                    シチュエーション
                  </div>
                  <div class="border-t border-b border-e-lg pa-2 d-flex align-center"
                    style="width: calc(100% - 110px);">
                    <span v-html="replaceNewLines(local_chunk_sentence_obj.situation)"></span>
                  </div>
                </div>

                <div class="d-flex">
                  <div class="border-b-lg border-s-lg border-e rounded-bs-lg pl-1 d-flex align-center"
                    style="width: 110px">
                    備考
                  </div>
                  <div class="border-b-lg border-e-lg rounded-be-lg pa-2 d-flex align-center"
                    style="width: calc(100% - 110px)">
                    <span v-html="replaceNewLines(local_chunk_sentence_obj.notes)"></span>
                  </div>
                </div>
              </div>

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn text="Close" variant="plain" @click="dialog = false">Close</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>

          <div class="border rounded-be-lg d-flex align-center justify-center" style="width: 50%;"
            @click="redoChunkSentence">
            <svg-icon type="mdi" :path="mdi_arrow_u_right_top_bold"></svg-icon>
          </div>

        </div>
      </div>
    </div>

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
import { mdiMenu, mdiArrowURightTopBold } from '@mdi/js';
import { getPolitenessColor } from '@/utils/politenessUtils'; 

export default {
  props: {
    props_chunk_sentence_obj: Object,
  },
  components: {
    SvgIcon
  },
  data() {
    return {
      
      mdi_menu: mdiMenu,
      mdi_arrow_u_right_top_bold: mdiArrowURightTopBold,
      dialog: false, 
      local_chunk_sentence_obj: { ...this.props_chunk_sentence_obj }, 
      isHovered: false,
      chunkDetailDialog: false,
      selectedChunk: {},
    };
  },
  watch: {
    
    props_chunk_sentence_obj: {
      handler(newValue) {
        this.local_chunk_sentence_obj = { ...newValue };
      },
      deep: true,
      immediate: true
    }
  },
  computed: {
    computedPoliteness() {
      return parseFloat(this.calculatePoliteness(this.local_chunk_sentence_obj.used_chunks)).toFixed(1);
    },
    politenessColor() {
      return getPolitenessColor(this.computedPoliteness);
    }
  },
  methods: {
    replaceNewLines(text) {
      return text ? text.replace(/\n/g, '<br>') : '';
    },
    
    openDialog() {
      this.dialog = true;
      this.local_chunk_sentence_obj = { ...this.props_chunk_sentence_obj }; 
    },
    openChunkDetailDialog(chunk) {
      this.selectedChunk = chunk;
      this.chunkDetailDialog = true;
    },
    redoChunkSentence() {
      
      this.$emit('redo', this.props_chunk_sentence_obj);
    },
    calculatePoliteness(used_chunks) {
      if (!used_chunks || used_chunks.length === 0) {
        return 0;
      }
      const politenessSum = used_chunks.reduce((sum, chunk) => sum + (chunk.value.politeness || 0), 0);
      return (politenessSum / used_chunks.length).toFixed(1);
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
