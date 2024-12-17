<template>
  <v-container>
    <h5 class="text-center">Speak More</h5>
    <h2 class="text-center">- 選択 -</h2>

    <template v-if="$vuetify.display.xs">
      <h5 class="text-center mt-4" style="color: grey;">
        以下一覧から発声実践するチャンク文/フレーズを選択してください。
      </h5>
    </template>
    <template v-else>
      <h4 class="text-center mt-4" style="color: grey;">
        以下一覧から発声実践するチャンク文/フレーズを選択してください。
      </h4>
    </template>

    <v-divider class="mt-4"></v-divider>

    <div class="d-flex justify-space-evenly my-2 py-2">
      <v-btn @click="goToPractice" width="45%" class="border" color="primary"
        :disabled="selected_chunks.length === 0">実践（選択）</v-btn>
      <v-btn @click="openRandomDialog" width="45%" :prepend-icon="mdi_random" class="border"
        color="primary">実践（ランダム）</v-btn>
    </div>

    <v-text-field v-model="search_keyword" single-line density="compact" label="クイック検索" outlined hide-details clearable
      :prepend-inner-icon="mdi_magnify"></v-text-field>

    <div class="border-lg rounded-lg pa-4 my-2" v-for="folder in filtered_chunk_sentences" :key="folder.folder_id">
      <div class="d-flex justify-space-between align-center">
        <h3>{{ folder.folder_name }}</h3>
        <v-btn icon @click="toggleFolderVisibility(folder.folder_id)">
          <v-icon>{{ folderVisibility[folder.folder_id] ? mdiChevronUp : mdiChevronDown }}</v-icon>
        </v-btn>
      </div>
      <v-expand-transition>
        <div v-show="folderVisibility[folder.folder_id]">
          <template v-for="(chunk_sentence_row, index) in folder.chunk_sentences">
            <ChunkSentenceSelectCompo :props_chunk_sentence_row="chunk_sentence_row" :index="index + 1"
              :key="chunk_sentence_row.id" v-if="true" @update:selected="updateSelected">
              <template #index>{{ index + 1 }}</template>
            </ChunkSentenceSelectCompo>
          </template>
        </div>
      </v-expand-transition>
    </div>

    <v-dialog v-model="randomDialog" max-width="500">
      <v-card>
        <v-card-title>
          <span class="headline">ランダム実践設定</span>
        </v-card-title>
        <v-card-text>
          <v-select v-model="selectedFolderId" :items="folderOptions" label="フォルダ選択" item-title="name"
            item-value="id"></v-select>
          <v-text-field v-model="randomCount" type="number" label="選択するチャンク文の数" min="1"
            :max="totalChunkSentenceCount"></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" text @click="randomDialog = false">キャンセル</v-btn>
          <v-btn color="primary" text @click="startRandomPractice">開始</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-container>
</template>

<script>
import { mdiMagnify, mdiPlusCircle, mdiRandom, mdiChevronDown, mdiChevronUp } from "@mdi/js"; 
import { mapActions } from "vuex"; 
import ChunkSentenceSelectCompo from "../../components/ChunkSentenceSelect-Compo.vue"; 

export default {
  components: {
    ChunkSentenceSelectCompo,
  },
  data() {
    return {
      mdi_magnify: mdiMagnify,
      mdi_plus_circle: mdiPlusCircle,
      mdi_random: mdiRandom,
      mdiChevronDown: mdiChevronDown,
      mdiChevronUp: mdiChevronUp,

      all_chunk_sentence_rows: [], 
      filtered_chunk_sentences: [], 

      search_keyword: "", 
      selected_chunks: [], 

      randomDialog: false, 
      randomCount: 5, 

      folderVisibility: {}, 
      selectedFolderId: null, 
      folderOptions: [] 
    };
  },
  computed: {
    totalChunkSentenceCount() {
      return this.filtered_chunk_sentences.reduce((total, folder) => total + folder.chunk_sentences.length, 0);
    }
  },
  methods: {
    ...mapActions(['addChunk', 'removeChunk', 'clearChunks']), 
    
    toggleFolderVisibility(folderId) {
      if (Object.prototype.hasOwnProperty.call(this.folderVisibility, folderId)) {
        this.folderVisibility[folderId] = !this.folderVisibility[folderId];
      } else {
        this.folderVisibility = { ...this.folderVisibility, [folderId]: true };
      }
    },
    
    filterChunks() {
      this.filtered_chunk_sentences = this.all_chunk_sentence_rows.map(folder => {
        return {
          ...folder,
          chunk_sentences: folder.chunk_sentences.filter(chunk_sentence => {
            
            if (!this.search_keyword) return true;
            
            return (
              chunk_sentence.chunk_sentence.includes(this.search_keyword) ||
              chunk_sentence.translating_sentence.includes(this.search_keyword) ||
              chunk_sentence.situation.includes(this.search_keyword) ||
              chunk_sentence.notes.includes(this.search_keyword)
            );
          })
        };
      });
    },
    
    updateSelected(checked, chunk_sentence_row) {
      if (checked) {
        this.selected_chunks.push(chunk_sentence_row); 
        this.addChunk(chunk_sentence_row); 
      } else {
        
        const index_to_delete = this.selected_chunks.findIndex(chunk => chunk.chunk_id === chunk_sentence_row.chunk_id);
        this.selected_chunks.splice(index_to_delete, 1);

        this.removeChunk(chunk_sentence_row); 
      }
    },
    
    goToPractice() {
      this.$router.push("/speak_more/practice");
    },
    openRandomDialog() {
      this.randomDialog = true;
    },
    startRandomPractice() {
      const folder = this.filtered_chunk_sentences.find(f => f.folder_id === this.selectedFolderId);
      if (folder) {
        const shuffled = folder.chunk_sentences.sort(() => 0.5 - Math.random());
        this.selected_chunks = shuffled.slice(0, this.randomCount);
        
        this.clearChunks();
        this.selected_chunks.forEach(chunk => this.addChunk(chunk));
        this.randomDialog = false;
        this.goToPractice();
      } else {
        console.error("Selected folder is not found");
      }
    },
    async fetchChunkSentences() {
      try {
        const response = await fetch(`/api/chunk_sentences/list`, {
          method: "GET",
        });

        if (!response.ok) {
          throw new Error("Network response was not ok.");
        }

        const data = await response.json();
        this.all_chunk_sentence_rows = data;
        
        this.filterChunks();
        
        data.forEach(folder => {
          this.folderVisibility = { ...this.folderVisibility, [folder.folder_id]: false }; 
          this.folderOptions.push({ id: folder.folder_id, name: folder.folder_name });
        });
        
      } catch (error) {
        console.error("Fetch error:", error);
      }
    }
  },
  async mounted() {
    this.clearChunks();
    await this.fetchChunkSentences();
  },
  watch: {
    
    search_keyword: function () {
      this.filterChunks();
    },
  },
};
</script>
