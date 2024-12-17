<template>
  <v-container>
    <h5 class="text-center">Speak More</h5>
    <h2 class="text-center">- 実践 -</h2>

    <template v-if="$vuetify.display.xs">
      <h5 class="text-center mt-4">
        作成した英文を発音しカウントしましょう。
      </h5>
      <h6 class="text-center" style="color: grey;">
        話すシチュエーションをイメージしながら発声しましょう。<br>
        詰まらず流暢に話せるまでが目安です。
      </h6>
    </template>
    <template v-else>
      <h4 class="text-center mt-4">
        作成した英文を発音しカウントしましょう。
      </h4>
      <h5 class="text-center" style="color: grey;">
        話すシチュエーションをイメージしながら発声しましょう。<br>
        詰まらず流暢に話せるまでが目安です。
      </h5>
    </template>

    <v-divider class="my-4"></v-divider>

    <v-container v-if="!supports_get_user_media" class="alert alert-danger">
      getUserMedia is not supported in this browser.
    </v-container>

    <v-carousel v-model="current_slide" hide-delimiters :show-arrows="false" height="350px">
      <v-carousel-item v-for="(chunk, index) in selected_chunks" :key="index">
        <v-sheet class="d-flex flex-column justify-center border-lg mx-3 rounded-lg">
          <v-container class="d-flex flex-column justify-center" style="word-break: break-word;">
            <div class="d-flex flex-wrap justify-space-between align-center">
              <div>
                <template v-for="used_chunk in chunk.used_chunks">
                  <v-chip size="x-small" class="ma-1"
                    @click="openChunkDetailDialog(used_chunk)" :key="used_chunk.chunk_id" v-if="true">
                    {{ used_chunk.title }}
                  </v-chip>
                </template>
              </div>
              <div class="svg-icon-wrapper">
                <svg-icon class="border rounded-circle" type="mdi" :path="mdi_dots_horizontal" @click="openChunkSentenceDetailDialog(chunk)"></svg-icon>
              </div>
            </div>
            
            <template v-if="$vuetify.display.xs">
              <div class="d-flex justify-space-between align-center mt-2">
                <h5>
                  <span v-if="!chunk.is_blind">{{ chunk.chunk_sentence }}</span>
                  <span v-else>*****</span>
                </h5>
                <div class="svg-icon-wrapper">
                  <svg-icon class="border rounded-circle" type="mdi" :path="mdi_volume_high" @click="speak(chunk.chunk_sentence)"></svg-icon>
                </div>
              </div>
              
              <div class="d-flex justify-space-between align-center mt-2 border-b" style="color: grey;">
                <h6>{{ chunk.translating_sentence }}</h6>
                <div class="svg-icon-wrapper">
                  <svg-icon class="border rounded-circle" type="mdi" :path="chunk.is_blind ? mdi_eye : mdi_eye_off"
                    @click="toggleBlind(index)"></svg-icon>
                </div>
              </div>
            </template>

            <template v-else>
              
              <div class="d-flex justify-space-between align-center mt-2">
                <h3>
                  <span v-if="!chunk.is_blind">{{ chunk.chunk_sentence }}</span>
                  <span v-else>*****</span>
                </h3>
                <div class="svg-icon-wrapper">
                  <svg-icon class="border rounded-circle" type="mdi" :path="mdi_volume_high" @click="speak(chunk.chunk_sentence)"></svg-icon>
                </div>
              </div>
              
              <div class="d-flex justify-space-between align-center mt-2 border-b" style="color: grey;">
                <h4>{{ chunk.translating_sentence }}</h4>
                <div class="svg-icon-wrapper">
                  <svg-icon class="border rounded-circle" type="mdi" :path="chunk.is_blind ? mdi_eye : mdi_eye_off"
                    @click="toggleBlind(index)"></svg-icon>
                </div>
              </div>
            </template>
          </v-container>

          <v-sheet class="d-flex justify-center align-center mt-2">
            
            <v-btn @click="decrementCount(index)" class="border d-flex justify-center" height="60px" color="secondary"
              style="width: 10%;">
              <svg-icon type="mdi" :path="mdi_minus_circle"></svg-icon>
            </v-btn>
            
            <div class="border d-flex flex-column justify-center align-center" style="width: 50%; height: 100px;">
              <h1>{{ chunk.pronounced_count }}</h1>
              <h3 class="text-green">+{{ chunk.current_session_count }}</h3>
            </div>
            
            <v-btn @click="incrementCount(index)" class="border d-flex justify-center" height="60px" color="secondary"
              style="width: 10%;">
              <svg-icon type="mdi" :path="mdi_plus_circle"></svg-icon>
            </v-btn>
          </v-sheet>

          <div class="d-flex justify-center align-center my-2">
            
            <canvas :ref="'canvas' + index" class="mt-0" style="height: 40px;"></canvas>
            
            <v-btn @click="toggleRecording(index)" :disabled="!supports_get_user_media" color="secondary">
              <svg-icon type="mdi" :path="chunk.is_recording ? mdi_stop_circle : mdi_record_circle"></svg-icon>
              {{ chunk.is_recording ? '停止' : '録音' }}
            </v-btn>
            
            <v-btn @click="playAudio(index)" :disabled="!chunk.audio_url || chunk.is_recording || is_playing"
              color="secondary">
              <svg-icon type="mdi" :path="mdi_play_circle"></svg-icon>
              再生
            </v-btn>
          </div>
        </v-sheet>
      </v-carousel-item>
    </v-carousel>

    
    <div class="d-flex justify-center align-center mt-2">
      <v-btn @click="prevSlide">
        <svg-icon type="mdi" :path="mdi_arrow_left_circle"></svg-icon>
      </v-btn>
      <span>{{ current_slide + 1 }} / {{ selected_chunks.length }}</span>
      <v-btn @click="nextSlide">
        <svg-icon type="mdi" :path="mdi_arrow_right_circle"></svg-icon>
      </v-btn>
    </div>
    <div class="d-flex justify-center align-center mt-4" color="primary">
      <v-btn @click="submitChunkSentences" color="primary">実践終了</v-btn>
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
                {{ selectedChunk.value.learning_chunk }}
              </div>
            </div>
            <div class="d-flex">
              <div class="border-b-lg border-s-lg border-e rounded-bs-lg pl-1 d-flex align-center" style="width: 110px">
                翻訳文
              </div>
              <div class="border-b-lg border-e-lg rounded-be-lg pa-2 d-flex align-center"
                style="width: calc(100% - 110px)">
                {{ selectedChunk.value.translating_chunk }}
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
                {{ selectedChunk.value.nuance }}
              </div>
            </div>
            <div class="d-flex">
              <div class="border-t border-b border-e border-s-lg pl-1 d-flex align-center" style="width: 110px">
                シチュエーション
              </div>
              <div class="border-t border-b border-e-lg pa-2 d-flex align-center" style="width: calc(100% - 110px);">
                {{ selectedChunk.value.situation }}
              </div>
            </div>
            <div class="d-flex">
              <div class="border-b-lg border-s-lg border-e rounded-bs-lg pl-1 d-flex align-center" style="width: 110px">
                備考
              </div>
              <div class="border-b-lg border-e-lg rounded-be-lg pa-2 d-flex align-center"
                style="width: calc(100% - 110px)">
                {{ selectedChunk.value.notes }}
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

    
    <v-dialog v-model="chunkSentenceDetailDialog" max-width="600" style="font-size: 12px;">
      <v-card>
        <v-card-title class="text-center" style="font-size: 16px;">詳細</v-card-title>
        <v-card-text>
          <div class="d-flex flex-column px-2">
            <div class="d-flex">
              <div class="border-t-lg border-e border-s-lg rounded-ts-lg pl-1 d-flex align-center" style="width: 110px">
                使用チャンク
              </div>
              <div class="border-t-lg border-e-lg rounded-te-lg d-flex flex-wrap align-center"
                style="width: calc(100% - 110px)">
                <template v-if="selectedChunkSentence.used_chunks.length !== 0">
                  <template v-for="used_chunk in selectedChunkSentence.used_chunks">
                    <v-chip size="small" class="ma-1" v-if="true" :key="used_chunk.chunk_id">
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
              <div class="border-t border-b border-e-lg pa-2 d-flex align-center" style="width: calc(100% - 110px);">
                {{ selectedChunkSentence.chunk_sentence }}
              </div>
            </div>
            <div class="d-flex">
              <div class="border-b-lg border-s-lg border-e rounded-bs-lg pl-1 d-flex align-center" style="width: 110px">
                翻訳文
              </div>
              <div class="border-b-lg border-e-lg rounded-be-lg pa-2 d-flex align-center"
                style="width: calc(100% - 110px)">
                {{ selectedChunkSentence.translating_sentence }}
              </div>
            </div>

            <div class="d-flex mt-4">
              <div class="border-t-lg border-e border-s-lg rounded-ts-lg pl-1 d-flex align-center" style="width: 110px">
                丁寧度<br>(自動計算)
              </div>
              <div class="border-t-lg border-e-lg rounded-te-lg d-flex align-center justify-center px-2"
                style="width: calc(100% - 110px)">
                <v-slider v-model="selectedChunkSentence.politeness" :color="politenessColor"
                  :ticks="{ 0: '低', 1: '', 2: '中', 3: '', 4: '高' }" show-ticks="always" max="4" step="0.1" tick-size="4"
                  readonly></v-slider>
              </div>
            </div>

            <div class="d-flex">
              <div class="border-t border-b border-e border-s-lg pl-1 d-flex align-center" style="width: 110px">
                シチュエーション
              </div>
              <div class="border-t border-b border-e-lg pa-2 d-flex align-center" style="width: calc(100% - 110px);">
                {{ selectedChunkSentence.situation }}
              </div>
            </div>

            <div class="d-flex">
              <div class="border-b-lg border-s-lg border-e rounded-bs-lg pl-1 d-flex align-center" style="width: 110px">
                備考
              </div>
              <div class="border-b-lg border-e-lg rounded-be-lg pa-2 d-flex align-center"
                style="width: calc(100% - 110px)">
                {{ selectedChunkSentence.notes }}
              </div>
            </div>
          </div>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text="Close" variant="plain" @click="chunkSentenceDetailDialog = false">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-container>
</template>

<script>
import SvgIcon from '@jamescoyle/vue-icon';
import { mdiPlusCircle, mdiMinusCircle, mdiRecordCircle, mdiStopCircle, mdiVolumeHigh, mdiPlayCircle, mdiArrowRightCircle, mdiArrowLeftCircle, mdiEye, mdiEyeOff, mdiDotsHorizontal } from "@mdi/js";
import { mapGetters, mapActions } from "vuex";
import { nextTick } from 'vue';

export default {
  components: {
    SvgIcon
  },
  computed: {
    ...mapGetters(['selectedChunkSentences']),
    politenessColor() {
      const politeness = this.selectedChunkSentence.politeness;
      if (politeness >= 0 && politeness < 1) return '#3F51B5'; 
      if (politeness >= 1 && politeness < 2) return '#03A9F4'; 
      if (politeness >= 2 && politeness < 3) return '#4CAF50'; 
      if (politeness >= 3 && politeness < 4) return '#FF9800'; 
      if (politeness >= 4) return '#F44336'; 
      return 'grey';
    }
  },
  data() {
    return {
      mdi_plus_circle: mdiPlusCircle,
      mdi_minus_circle: mdiMinusCircle,
      mdi_record_circle: mdiRecordCircle,
      mdi_stop_circle: mdiStopCircle,
      mdi_volume_high: mdiVolumeHigh,
      mdi_play_circle: mdiPlayCircle,
      mdi_arrow_right_circle: mdiArrowRightCircle,
      mdi_arrow_left_circle: mdiArrowLeftCircle,
      mdi_eye: mdiEye,
      mdi_eye_off: mdiEyeOff,
      mdi_dots_horizontal: mdiDotsHorizontal,

      selected_chunks: [],
      is_playing: false,
      supports_get_user_media: !!(navigator.mediaDevices && navigator.mediaDevices.getUserMedia),
      is_speaking: false,
      current_audio: null,
      current_slide: 0, 
      chunkDetailDialog: false,
      chunkSentenceDetailDialog: false,
      selectedChunk: {}, 
      selectedChunkSentence: {}, 
    };
  },
  mounted() {
    this.selected_chunks = this.selectedChunkSentences.map(chunk => ({
      ...chunk,
      audio_url: null,
      is_recording: false,
      media_recorder: null,
      audio_chunks: [],
      audio_context: null,
      analyser: null,
      data_array: null,
      buffer_length: 0,
      current_session_count: 0,
      is_blind: true 
    }));

    
    if (this.selected_chunks.length > 0) {
      this.speak(this.selected_chunks[0].chunk_sentence);
    }
  },
  methods: {
    ...mapActions(['setPracticedChunks']),  
    incrementCount(index) {
      this.selected_chunks[index].pronounced_count++;
      this.selected_chunks[index].current_session_count++;
    },
    decrementCount(index) {
      if (this.selected_chunks[index].pronounced_count > 0 && this.selected_chunks[index].current_session_count > 0) {
        this.selected_chunks[index].pronounced_count--;
      }
      if (this.selected_chunks[index].current_session_count > 0) {
        this.selected_chunks[index].current_session_count--;
      }
    },
    async startRecording(index) {
      if (this.selected_chunks[index].is_recording) return;

      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const media_recorder = new MediaRecorder(stream);
        this.selected_chunks[index].audio_chunks = [];

        const audio_context = new (window.AudioContext || window.webkitAudioContext)();
        const source = audio_context.createMediaStreamSource(stream);
        const analyser = audio_context.createAnalyser();
        source.connect(analyser);
        analyser.fftSize = 2048;
        const buffer_length = analyser.frequencyBinCount;
        const data_array = new Uint8Array(buffer_length);

        this.selected_chunks[index].media_recorder = media_recorder;
        this.selected_chunks[index].audio_context = audio_context;
        this.selected_chunks[index].analyser = analyser;
        this.selected_chunks[index].data_array = data_array;
        this.selected_chunks[index].buffer_length = buffer_length;

        media_recorder.ondataavailable = event => {
          this.selected_chunks[index].audio_chunks.push(event.data);
        };

        media_recorder.onstop = () => {
          const audio_blob = new Blob(this.selected_chunks[index].audio_chunks, { type: 'audio/wav' });
          this.selected_chunks[index].audio_url = URL.createObjectURL(audio_blob);
          audio_context.close();
          this.playAudio(index);
        };

        media_recorder.start();
        this.selected_chunks[index].is_recording = true;
        await nextTick();
        this.drawWaveform(index);
      } catch (error) {
        console.error('Error accessing media devices.', error);
      }
    },
    stopRecording(index) {
      if (this.selected_chunks[index].media_recorder && this.selected_chunks[index].media_recorder.state !== 'inactive') {
        this.selected_chunks[index].media_recorder.stop();
        this.selected_chunks[index].is_recording = false;
        
        this.incrementCount(index);
      }
    },
    toggleRecording(index) {
      if (this.selected_chunks[index].is_recording) {
        this.stopRecording(index);
      } else {
        if (this.current_audio && !this.current_audio.paused) {
          this.current_audio.pause();
          this.current_audio.currentTime = 0;
        }
        if (window.speechSynthesis.speaking) {
          window.speechSynthesis.cancel();
          this.is_speaking = false;
        }
        this.startRecording(index);
      }
    },
    playAudio(index) {
      if (this.selected_chunks[index].audio_url) {
        const audio = new Audio(this.selected_chunks[index].audio_url);
        this.current_audio = audio;
        this.is_playing = true;
        audio.onended = () => {
          this.is_playing = false;
          this.current_audio = null;
        };
        audio.play();
      }
    },
    speak(text) {
      if (this.is_speaking) return; 

      if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'en-US';

        utterance.onstart = () => {
          this.is_speaking = true;
        };

        utterance.onend = () => {
          this.is_speaking = false;
          
          
        };

        window.speechSynthesis.speak(utterance);
      } else {
        console.error('SpeechSynthesis is not supported in this browser.');
      }
    },
    toggleBlind(index) {
      this.selected_chunks[index].is_blind = !this.selected_chunks[index].is_blind;
    },
    drawWaveform(index) {
      if (!this.selected_chunks[index].analyser) return;

      const canvas = this.$refs[`canvas${index}`][0];
      const canvas_ctx = canvas.getContext('2d');
      const draw = () => {
        if (!this.selected_chunks[index].is_recording) return;

        this.selected_chunks[index].analyser.getByteTimeDomainData(this.selected_chunks[index].data_array);

        canvas_ctx.fillStyle = 'rgb(200, 200, 200)';
        canvas_ctx.fillRect(0, 0, canvas.width, canvas.height);

        canvas_ctx.lineWidth = 2;
        canvas_ctx.strokeStyle = 'rgb(0, 0, 0)';
        canvas_ctx.beginPath();

        const slice_width = canvas.width * 1.0 / this.selected_chunks[index].buffer_length;
        let x = 0;

        for (let i = 0; i < this.selected_chunks[index].buffer_length; i++) {
          const v = this.selected_chunks[index].data_array[i] / 128.0;
          const y = v * canvas.height / 2;

          if (i === 0) {
            canvas_ctx.moveTo(x, y);
          } else {
            canvas_ctx.lineTo(x, y);
          }

          x += slice_width;
        }

        canvas_ctx.lineTo(canvas.width, canvas.height / 2);
        canvas_ctx.stroke();

        requestAnimationFrame(draw);
      };

      draw();
    },
    prevSlide() {
      if (this.current_slide > 0) {
        this.current_slide--;
      } else {
        this.current_slide = this.selected_chunks.length - 1; 
      }
      
      this.speak(this.selected_chunks[this.current_slide].chunk_sentence);
    },
    nextSlide() {
      if (this.current_slide < this.selected_chunks.length - 1) {
        this.current_slide++;
      } else {
        this.current_slide = 0; 
      }
      
      this.speak(this.selected_chunks[this.current_slide].chunk_sentence);
    },
    async submitChunkSentences() {
      try {
        const formDataJSON = JSON.stringify({
          editDataList: this.selected_chunks.map(chunk => ({
            id: chunk.id,
            pronounced_count: chunk.pronounced_count,
            current_session_count: chunk.current_session_count
          }))
        });
        const response = await fetch('/api/chunk_sentences/list/update_pronounced_count', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: formDataJSON,
        });

        if (!response.ok) {
          throw new Error('Failed to update chunks');
        }

        const result = await response.json();
        console.log('Update successful:', result);
        this.setPracticedChunks(this.selected_chunks);
        this.$router.push({ name: 'Speak-More-Result' });
      } catch (error) {
        console.error('Error submitting chunks:', error);
      }
    },
    openChunkDetailDialog(chunk) {
      this.selectedChunk = chunk;
      this.chunkDetailDialog = true;
    },
    openChunkSentenceDetailDialog(chunkSentence) {
      this.selectedChunkSentence = chunkSentence;
      this.chunkSentenceDetailDialog = true;
    },
    displayPolitenessColor(politeness) {
      if (politeness === 0) return '#3F51B5'; 
      if (politeness === 1) return '#03A9F4'; 
      if (politeness === 2) return '#4CAF50'; 
      if (politeness === 3) return '#FF9800'; 
      if (politeness === 4) return '#F44336'; 
      return 'grey';
    }
  }
};
</script>

<style scoped>
.v-btn {
  margin: 0 5px;
}

.alert {
  padding: 10px;
  background-color: #f44336;
  color: white;
  text-align: center;
  margin-top: 10px;
}

canvas {
  border: 1px solid #ccc;
  margin-top: 20px;
}

.text-green {
  color: green;
}

.svg-icon-wrapper {
  display: inline-block;
  transition: transform 0.2s ease-in-out;
}

.svg-icon-wrapper:hover {
  transform: scale(1.2);
}
</style>
