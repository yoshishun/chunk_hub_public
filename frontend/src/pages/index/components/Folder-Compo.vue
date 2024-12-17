<template>
  <v-col cols="12" class="pb-0">
    <v-card @click="navigateToFolder" class="border">

      <v-card-title style="font-size: 16px;">
        <slot name="folder_name"></slot>
      </v-card-title>

      <div class="d-flex">
        <div class="d-flex flex-column">
          <v-card-subtitle class="d-flex align-center" >
            <svg-icon height="14px" width="14px" type="mdi" :path="mdi_account_voice"></svg-icon>
            <div class="ml-2" style="font-size: 12px;">{{ total_pronounced_count }}</div>
          </v-card-subtitle>
          <v-card-subtitle class="d-flex align-center">
            <svg-icon height="14px" width="14px" type="mdi" :path="mdi_format_list_bulleted_square"></svg-icon>
            <div class="ml-2" style="font-size: 12px;">{{ item_count }}</div>
          </v-card-subtitle>
        </div>

        <div class="d-flex flex-column">
          <v-card-subtitle class="d-flex align-center">
            <svg-icon height="14px" width="14px" type="mdi" :path="mdi_calendar_plus"></svg-icon>
            <div class="ml-2" style="font-size: 12px;">
              <slot name="create_date"></slot>
            </div>
          </v-card-subtitle>
          <v-card-subtitle class="d-flex align-center">
            <svg-icon height="14px" width="14px" type="mdi" :path="mdi_calendar_refresh"></svg-icon>
            <div class="ml-2" style="font-size: 12px;">
              <slot name="update_date"></slot>
            </div>
          </v-card-subtitle>
        </div>
      </div>

      <v-card-actions class="actions-right">
        <slot name="actions"></slot>
      </v-card-actions>
    </v-card>
  </v-col>
</template>

<script>
import SvgIcon from '@jamescoyle/vue-icon';
import { mdiCalendarPlus, mdiCalendarRefresh, mdiAccountVoice, mdiFormatListBulletedSquare } from '@mdi/js';

export default {
  components: {
    SvgIcon
  },
  data() {
    return {
      mdi_calendar_plus: mdiCalendarPlus,
      mdi_calendar_refresh: mdiCalendarRefresh,
      mdi_account_voice: mdiAccountVoice,
      mdi_format_list_bulleted_square: mdiFormatListBulletedSquare
    };
  },
  props: {
    props_fid: {
      type: String,
      required: true
    },
    props_class: {
      type: Number,
      required: true
    },
    total_pronounced_count: {
      type: Number,
      required: true
    },
    item_count: {
      type: Number,
      required: true
    }
  },
  methods: {
    navigateToFolder() {
      if (this.props_class === 1) {
        this.$router.push({ name: 'Chunks-List', query: { fid: this.props_fid } });
      } else if (this.props_class === 2) {
        this.$router.push({ name: 'Chunk-Sentences-List', query: { fid: this.props_fid } });
      }
    }
  }
};
</script>

<style scoped>
.actions-right {
  justify-content: flex-end;
}
</style>
