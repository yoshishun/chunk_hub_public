<template>
  <v-container>
    <h5 class="text-center">Speak More</h5>
    <h2 class="text-center">- 結果 -</h2>

    <template v-if="$vuetify.display.xs">
      <h5 class="text-center mt-4" style="color: grey;">
        以下のチャンク文/フレーズを実践しました。
      </h5>
    </template>
    <template v-else>
      <h4 class="text-center mt-4" style="color: grey;">
        以下のチャンク文/フレーズを実践しました。
      </h4>
    </template>

    <v-divider class="mt-4"></v-divider>

    <v-list style="word-break: break-word;" class="mt-4">
      <v-list-item v-for="chunk in practicedChunks" :key="chunk.chunk_id">

        <template v-if="$vuetify.display.xs">
          <v-list-item-content class="d-flex flex-column">
            <div class="d-flex flex-column">
              <h5>{{ chunk.chunk_sentence }}</h5>
              <h6 style="color: grey;">{{ chunk.translating_sentence }}</h6>
            </div>
            <div class="d-flex justify-end border-l">
              <h4>
                {{ chunk.pronounced_count }}
              </h4>
              <span>（</span>
              <h4 class="text-green"> +{{ chunk.current_session_count }}</h4>
              <span>）</span>
            </div>
          </v-list-item-content>
        </template>
        
        <template v-else>
          <v-list-item-content class="d-flex align-center">
            <div class="d-flex flex-column" style="width: calc(100% - 100px);">
              <h4>{{ chunk.chunk_sentence }}</h4>
              <h5 style="color: grey;">{{ chunk.translating_sentence }}</h5>
            </div>
            <div class="d-flex justify-end border-l" style="width: 100px;">
              <h4>
                {{ chunk.pronounced_count }}
              </h4>
              <span>（</span>
              <h4 class="text-green"> +{{ chunk.current_session_count }}</h4>
              <span>）</span>
            </div>
          </v-list-item-content>
        </template>

      </v-list-item>
    </v-list>

    <div class="d-flex justify-center mt-4">
      <v-btn width="30%" @click="$router.push('/speak_more/select')" color="primary">戻る</v-btn>
    </div>
  </v-container>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  computed: {
    ...mapGetters(['practicedChunks'])
  }
};
</script>

<style scoped>
.v-list-item {
  border-bottom: 1px solid #ccc;
}

.text-green {
  color: green;
}
</style>
