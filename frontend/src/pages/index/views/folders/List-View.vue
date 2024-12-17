<template>
  <v-container>
    <h5 class="text-center">Chunk Hub</h5>
    <h2 class="text-center">- フォルダ一覧 -</h2>

    <template v-if="$vuetify.display.xs">
      <h5 class="text-center mt-4" style="color: grey;">
        チャンク・チャンク文/フレーズのフォルダを管理します。
      </h5>
    </template>
    <template v-else>
      <h4 class="text-center mt-4" style="color: grey;">
        チャンク・チャンク文/フレーズのフォルダを管理します。
      </h4>
    </template>

    <v-divider class="mt-4"></v-divider>

    <div class="d-flex justify-center mt-4">
      <v-btn color="primary" width="50%" @click="openCreateDialog">新規フォルダ作成</v-btn>
    </div>
    
    
    <v-dialog v-model="createDialog" max-width="500">
      <v-card>
        <v-card-title>新規フォルダ作成</v-card-title>
        <v-card-text>
          <v-text-field v-model="newFolder.name" label="フォルダ名"></v-text-field>
          <v-textarea v-model="newFolder.notes" label="説明"></v-textarea>
          <v-radio-group v-model="newFolder.class" label="フォルダの種類">
            <v-radio v-for="option in folderClasses" :key="option.value" :label="option.title" :value="option.value"></v-radio>
          </v-radio-group>
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="createDialog = false">キャンセル</v-btn>
          <v-btn text @click="createFolder">作成</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    
    <div v-if="$vuetify.display.xs">
      
      <v-container class="">
        <div class="border-s-lg border-e-lg border-t-lg border-b rounded-t-lg text-center bg-primary" style="font-size: 16px;">
          チャンク
        </div>
        <div class="border-s-lg border-e-lg border-b-lg rounded-b-lg pa-4 mb-4">
          <v-row>
            <template v-for="folder_row in all_folder_rows">
              <FolderCompo :key="folder_row.id" v-if="folder_row.class == 1" :props_fid="folder_row.id"
                :props_class="folder_row.class" :total_pronounced_count="folder_row.total_pronounced_count"
                :item_count="folder_row.item_count">
                <template #folder_name>{{ folder_row.name }}</template>
                <template #create_date>{{ folder_row.create_date }}</template>
                <template #update_date>{{ folder_row.update_date }}</template>
                <template #actions>
                  <v-btn icon @click.stop="openEditDialog(folder_row)" color="primary" class="border">
                    <SvgIcon type="mdi" :path="mdi_pencil"></SvgIcon>
                  </v-btn>
                  <v-btn icon @click.stop="confirmDelete(folder_row)" color="primary" class="border">
                    <SvgIcon type="mdi" :path="mdi_delete"></SvgIcon>
                  </v-btn>
                </template>
              </FolderCompo>
            </template>
          </v-row>
        </div>
      </v-container>

      <v-container class="">
        <div class="border-s-lg border-e-lg border-t-lg border-b rounded-t-lg text-center bg-primary" style="font-size: 16px;">
          チャンク文/フレーズ
        </div>
        <div class="border-s-lg border-e-lg border-b-lg rounded-b-lg pa-4 mb-4">
          <v-row>
            <template v-for="folder_row in all_folder_rows">
              <FolderCompo :key="folder_row.id" v-if="folder_row.class == 2" :props_fid="folder_row.id"
                :props_class="folder_row.class" :total_pronounced_count="folder_row.total_pronounced_count"
                :item_count="folder_row.item_count">
                <template #folder_name>{{ folder_row.name }}</template>
                <template #create_date>{{ folder_row.create_date }}</template>
                <template #update_date>{{ folder_row.update_date }}</template>
                <template #actions>
                  <v-btn icon @click.stop="openEditDialog(folder_row)" color="primary" class="border">
                    <SvgIcon type="mdi" :path="mdi_pencil"></SvgIcon>
                  </v-btn>
                  <v-btn icon @click.stop="confirmDelete(folder_row)" color="primary" class="border">
                    <SvgIcon type="mdi" :path="mdi_delete"></SvgIcon>
                  </v-btn>
                </template>
              </FolderCompo>
            </template>
          </v-row>
        </div>
      </v-container>
    </div>

    <div v-else class="d-flex">
      
      <v-container class="" style="width: 50%;">
        <div class="border-s-lg border-e-lg border-t-lg border-b rounded-t-lg mt-4 text-center bg-primary" style="font-size: 16px;">
          チャンク
        </div>
        <div class="border-s-lg border-e-lg border-b-lg rounded-b-lg pa-4 mb-4">
          <v-row>
            <template v-for="folder_row in all_folder_rows">
              <FolderCompo :key="folder_row.id" v-if="folder_row.class == 1" :props_fid="folder_row.id"
                :props_class="folder_row.class" :total_pronounced_count="folder_row.total_pronounced_count"
                :item_count="folder_row.item_count">
                <template #folder_name>{{ folder_row.name }}</template>
                <template #create_date>{{ folder_row.create_date }}</template>
                <template #update_date>{{ folder_row.update_date }}</template>
                <template #actions>
                  <v-btn icon @click.stop="openEditDialog(folder_row)" color="primary" class="border">
                    <SvgIcon type="mdi" :path="mdi_pencil"></SvgIcon>
                  </v-btn>
                  <v-btn icon @click.stop="confirmDelete(folder_row)" color="primary" class="border">
                    <SvgIcon type="mdi" :path="mdi_delete"></SvgIcon>
                  </v-btn>
                </template>
              </FolderCompo>
            </template>
          </v-row>
        </div>
      </v-container>

      <v-container class="" style="width: 50%;">
        <div class="border-s-lg border-e-lg border-t-lg border-b rounded-t-lg mt-4 text-center bg-primary" style="font-size: 16px;">
          チャンク文/フレーズ
        </div>
        <div class="border-s-lg border-e-lg border-b-lg rounded-b-lg pa-4 mb-4">
          <v-row>
            <template v-for="folder_row in all_folder_rows">
              <FolderCompo :key="folder_row.id" v-if="folder_row.class == 2" :props_fid="folder_row.id"
                :props_class="folder_row.class" :total_pronounced_count="folder_row.total_pronounced_count"
                :item_count="folder_row.item_count">
                <template #folder_name>{{ folder_row.name }}</template>
                <template #create_date>{{ folder_row.create_date }}</template>
                <template #update_date>{{ folder_row.update_date }}</template>
                <template #actions>
                  <v-btn icon @click.stop="openEditDialog(folder_row)" color="primary" class="border">
                    <SvgIcon type="mdi" :path="mdi_pencil"></SvgIcon>
                  </v-btn>
                  <v-btn icon @click.stop="confirmDelete(folder_row)" color="primary" class="border">
                    <SvgIcon type="mdi" :path="mdi_delete"></SvgIcon>
                  </v-btn>
                </template>
              </FolderCompo>
            </template>
          </v-row>
        </div>
      </v-container>
    </div>

    
    <v-dialog v-model="editDialog" max-width="500">
      <v-card>
        <v-card-title>フォルダ編集</v-card-title>
        <v-card-text>
          <v-text-field v-model="editFolder.name" label="フォルダ名"></v-text-field>
          <v-textarea v-model="editFolder.notes" label="説明"></v-textarea>
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="editDialog = false">キャンセル</v-btn>
          <v-btn text @click="saveFolder">保存</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    
    <v-dialog v-model="deleteDialog" max-width="500">
      <v-card>
        <v-card-title>フォルダ削除確認</v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          本当に{{ folderToDelete.name }}を削除しますか？
        </v-card-text>
        <v-card-text>
          <p style="color: red;">
            ※登録されているチャンク・チャンク文/フレーズも削除されます。
          </p>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions>
          <v-btn text @click="deleteDialog = false">キャンセル</v-btn>
          <v-btn text @click="deleteFolder">削除</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    
    <v-snackbar v-model="snackbar.show" :color="snackbar.color" top>
      {{ snackbar.text }}
      <v-btn text @click="snackbar.show = false">閉じる</v-btn>
    </v-snackbar>
  </v-container>
</template>

<script>
import SvgIcon from '@jamescoyle/vue-icon';
import { mdiPencil, mdiDelete, mdiFolderMove } from "@mdi/js";
import FolderCompo from "../../components/Folder-Compo.vue";

export default {
  components: {
    FolderCompo,
    SvgIcon,
  },
  data() {
    return {
      mdi_pencil: mdiPencil,
      mdi_delete: mdiDelete,
      mdi_folder_move: mdiFolderMove,

      all_folder_rows: [],
      fid: this.$route.query.fid,
      createDialog: false,
      newFolder: {
        name: '',
        notes: '',
        class: null
      },
      folderClasses: [
        { title: 'チャンク', value: 1 },
        { title: 'チャンク文/フレーズ', value: 2 }
      ],
      editDialog: false,
      deleteDialog: false,
      moveDialog: false,
      editFolder: {
        name: '',
        notes: ''
      },
      folderToDelete: null,
      currentFolderClass: null,
      selectedChunks: [],
      selectedChunkSentences: [],
      selectedFolder: null,
      chunks: [],
      chunkSentences: [],
      folders: [],
      snackbar: {
        show: false,
        text: '',
        color: 'success'
      },
      cache: {
        folders: null,
        folderDetails: {}
      },
    };
  },
  async mounted() {
    if (!this.cache.folders) {
      await this.fetchFolders();
    } else {
      this.all_folder_rows = this.cache.folders;
    }

    await this.fetchFolderDetails();
  },
  methods: {
    openCreateDialog() {
      this.createDialog = true;
    },
    async createFolder() {
      try {
        const response = await fetch('/api/folders/list/add', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.newFolder),
        });

        if (!response.ok) {
          throw new Error('Network response was not ok');
        }

        const data = await response.json();
        console.log('Folder created:', data);
        this.createDialog = false;
        this.newFolder = { name: '', notes: '', class: null }; 
        await this.fetchFolders(true); 
        await this.fetchFolderDetails(); 
        this.showSnackbar('フォルダが正常に作成されました', 'success');
      } catch (error) {
        console.error('Error creating folder:', error);
        this.showSnackbar('フォルダの作成中にエラーが発生しました', 'error');
      }
    },
    openEditDialog(folder) {
      this.editFolder = { ...folder };
      if (!this.editFolder.notes || this.editFolder.notes === 'null') {
        this.editFolder.notes = ''; 
      }
      this.editDialog = true;
    },
    async saveFolder() {
      try {
        const response = await fetch(`/api/folders/edit`, {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(this.editFolder),
        });

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        const data = await response.json();
        console.log("Folder saved:", data);
        this.editDialog = false;
        await this.fetchFolders(true); 
        await this.fetchFolderDetails();
        this.showSnackbar('フォルダが正常に保存されました', 'success');
      } catch (error) {
        console.error("Error saving folder:", error);
        this.showSnackbar('フォルダの保存中にエラーが発生しました', 'error');
      }
    },
    confirmDelete(folder) {
      this.folderToDelete = folder;
      this.deleteDialog = true;
    },
    async deleteFolder() {
      try {
        const response = await fetch(`/api/folders/delete`, {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ id: this.folderToDelete.id }),
        });

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        const data = await response.json();
        console.log("Folder and related data deleted successfully:", data);
        this.deleteDialog = false;
        await this.fetchFolders(true); 
        await this.fetchFolderDetails();
        this.showSnackbar('フォルダが正常に削除されました', 'success');
      } catch (error) {
        console.error("Error deleting folder:", error);
        this.showSnackbar('フォルダの削除中にエラーが発生しました', 'error');
      }
    },
    async fetchFolders(updateCache = false) {
      try {
        const response = await fetch("/api/folders/list", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        });

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        const data = await response.json();
        
        this.all_folder_rows = data;

        if (updateCache) {
          this.cache.folders = data;
        }
      } catch (err) {
        console.log("List fetch エラー");
        console.error(err);
      }
    },
    async fetchFolderDetails() {
      for (const folder of this.all_folder_rows) {
        if (!this.cache.folderDetails[folder.id]) {
          try {
            
            const countResponse = await fetch(`/api/folders/total_pronounced_count?fid=${folder.id}`, {
              method: "GET",
              headers: {
                "Content-Type": "application/json",
              },
            });

            if (!countResponse.ok) {
              throw new Error("Network response was not ok");
            }

            const countData = await countResponse.json();
            folder.total_pronounced_count = countData.total_pronounced_count;

            
            const itemsResponse = await fetch(`/api/folders/item_count?fid=${folder.id}`, {
              method: "GET",
              headers: {
                "Content-Type": "application/json",
              },
            });

            if (!itemsResponse.ok) {
              throw new Error("Network response was not ok");
            }

            const itemsData = await itemsResponse.json();
            folder.item_count = itemsData.item_count;

            this.cache.folderDetails[folder.id] = {
              total_pronounced_count: countData.total_pronounced_count,
              item_count: itemsData.item_count,
            };
          } catch (err) {
            console.log("Fetch folder details error");
            console.error(err);
          }
        } else {
          folder.total_pronounced_count = this.cache.folderDetails[folder.id].total_pronounced_count;
          folder.item_count = this.cache.folderDetails[folder.id].item_count;
        }
      }
    },
    showSnackbar(text, color) {
      this.snackbar.text = text;
      this.snackbar.color = color;
      this.snackbar.show = true;
    }
  }
};
</script>

<style scoped>
.v-btn {
  margin: 0 5px;
}
</style>