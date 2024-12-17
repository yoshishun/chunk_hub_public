<template>
  <div @mouseover="isHovered = true" @mouseleave="isHovered = false" :class="{'hover-effect': isHovered}" :style="{ backgroundColor: isHovered ? 'rgba(55,55,55,1)' : 'rgba(33,33,33,1)' }">
    <div style="word-break: break-word; width: 100%; font-size: 14px;" class="my-3 d-flex">
      
      <div name="index" class="border rounded-s-lg d-flex align-center justify-center" style="width: 40px;">
        <slot name="index">インデックス</slot>
      </div>

      
      
      <template v-if="$vuetify.display.xs">
        <div name="body" class="d-flex flex-column" style="width: calc(100% - 100px);">
          
          <div name="learning" class="border d-flex align-center pa-1">
            <span v-html="replaceNewLines(local_chunk_row.learning_chunk)"></span>
          </div>
          
          <div name="translating" class="border d-flex align-center pa-1">
            <span v-html="replaceNewLines(local_chunk_row.translating_chunk)"></span>
          </div>
          <div class="d-flex" style="width: 100%;">
            <div v-for="i in 4" :key="i"
              :style="{ width: '25%', backgroundColor: i <= local_chunk_row.politeness ? PolitenessColor : 'rgba(33,33,33,1)' }"
              class="pt-1 border-b"></div>
          </div>
        </div>
      </template>

      
      <template v-else>
        <div name="body" class="d-flex flex-column" style="width: calc(100% - 120px);">
          <div class="d-flex" style="height: 100%;">
            
            <div name="learning" class="border d-flex align-center pa-1" style="width: 50%;">
              <span v-html="replaceNewLines(local_chunk_row.learning_chunk)"></span>
            </div>
            
            <div name="translating" class="border d-flex align-center pa-1" style="width: 50%;">
              <span v-html="replaceNewLines(local_chunk_row.translating_chunk)"></span>
            </div>
          </div>
          <div class="d-flex">
            <div v-for="i in 4" :key="i"
              :style="{ width: '25%', backgroundColor: i <= local_chunk_row.politeness ? PolitenessColor : 'rgba(33,33,33,1)' }"
              class="pt-1 border-b"></div>
          </div>
        </div>
      </template>

      
      <div name="detail" style="width: 80px;">
        
        <div name="top" class="border rounded-te-lg text-end pr-1" style="height: 20px;">
          {{ local_chunk_row.pronounced_count }}
        </div>

        
        <div class="d-flex" style="cursor: pointer; height:calc(100% - 20px);">

          
          <v-dialog v-model="dialog" max-width="600" style="font-size: 12px;">
            <template v-slot:activator="{ props: activatorProps }">
              
              <div name="bottom" class="border d-flex align-center justify-center" style="width: 50%;" v-bind="activatorProps" @click="openDialog">
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
                    <v-slider v-model="local_chunk_row.politeness" :color="PolitenessColor" show-ticks="always" max="4"
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

              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn text="Close" variant="plain" @click="dialog = false" color="primary"></v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>

          
          <div class="border rounded-be-lg d-flex align-center justify-center" style="width: 50%;" @click="redoChunk">
            <svg-icon type="mdi" :path="mdiArrowURightTopBold"></svg-icon>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SvgIcon from '@jamescoyle/vue-icon';
import { mdiMenu, mdiArrowURightTopBold } from '@mdi/js';

export default {
  props: {
    props_chunk_row: Object,
  },
  components: {
    SvgIcon
  },
  data() {
    return {
      mdiMenu,
      mdiArrowURightTopBold,
      dialog: false,
      isHovered: false,
      local_chunk_row: { ...this.props_chunk_row }
    };
  },
  watch: {
    props_chunk_row: {
      handler(newVal) {
        this.local_chunk_row = { ...newVal };
      },
      deep: true,
      immediate: true
    }
  },
  computed: {
    PolitenessColor() {
      const politeness = this.local_chunk_row.politeness;
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
      this.dialog = true;
    },
    redoChunk() {
      this.$emit('redo', this.props_chunk_row);
    }
  },
};
</script>

<style scoped>
  .hover-effect {
    transition: background-color 0.3s;
  }
</style>
