<template>
  <v-container>
    <h5 class="text-center">- 統計 -</h5>
    <h2 class="text-center">学習分析</h2>
    <canvas id="chunk_chart"></canvas>
    <canvas id="chunk_sentence_chart"></canvas>
    <canvas id="chunk_pronounced_chart"></canvas>
    <canvas id="chunk_sentence_pronounced_chart"></canvas>
  </v-container>
</template>

<script>
import Chart from 'chart.js';

export default {
  data() {
    return {
      dates: [],
      chunk_registration_data: [],
      chunk_sentence_registration_data: [],
      chunk_pronounced_data: [],
      chunk_sentence_pronounced_data: []
    }
  },
  methods: {
    async fetchData() {
      try {
        const response = await fetch('/api/statistics', {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
          },
        });
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        this.dates = data.dates;
        this.chunk_registration_data = data.chunkRegistration;
        this.chunk_sentence_registration_data = data.chunkSentenceRegistration;
        this.chunk_pronounced_data = data.chunkPronounced;
        this.chunk_sentence_pronounced_data = data.chunkSentencePronounced;
        this.renderChunkChart();
        this.renderChunkSentenceChart();
        this.renderChunkPronouncedChart();
        this.renderChunkSentencePronouncedChart();
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    renderChunkChart() {
      const ctx = document.getElementById('chunk_chart').getContext('2d');
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: this.dates,
          datasets: [{
            label: '日毎のチャンク登録数',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1,
            data: this.chunk_registration_data
          }]
        },
        options: {
          scales: {
            x: {
              title: {
                display: true,
                text: '日付',
                align: 'center',
                padding: 10,
              }
            },
            y: {
              title: {
                display: true,
                text: 'チャンク数',
                align: 'center',
                padding: 10
              },
              beginAtZero: true
            }
          }
        }
      });
    },
    renderChunkSentenceChart() {
      const ctx = document.getElementById('chunk_sentence_chart').getContext('2d');
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: this.dates,
          datasets: [{
            label: '日毎のチャンク文/フレーズ登録数',
            backgroundColor: 'rgba(153, 102, 255, 0.2)',
            borderColor: 'rgba(153, 102, 255, 1)',
            borderWidth: 1,
            data: this.chunk_sentence_registration_data
          }]
        },
        options: {
          scales: {
            x: {
              title: {
                display: true,
                text: '日付',
                align: 'center',
                padding: 10,
              }
            },
            y: {
              title: {
                display: true,
                text: 'チャンク文/フレーズ数',
                align: 'center',
                padding: 10
              },
              beginAtZero: true
            }
          }
        }
      });
    },
    renderChunkPronouncedChart() {
      const ctx = document.getElementById('chunk_pronounced_chart').getContext('2d');
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: this.dates,
          datasets: [{
            label: '日毎のチャンク発声回数',
            backgroundColor: 'rgba(255, 159, 64, 0.2)',
            borderColor: 'rgba(255, 159, 64, 1)',
            borderWidth: 1,
            data: this.chunk_pronounced_data
          }]
        },
        options: {
          scales: {
            x: {
              title: {
                display: true,
                text: '日付',
                align: 'center',
                padding: 10,
              }
            },
            y: {
              title: {
                display: true,
                text: '発声回数',
                align: 'center',
                padding: 10
              },
              beginAtZero: true
            }
          }
        }
      });
    },
    renderChunkSentencePronouncedChart() {
      const ctx = document.getElementById('chunk_sentence_pronounced_chart').getContext('2d');
      new Chart(ctx, {
        type: 'bar',
        data: {
          labels: this.dates,
          datasets: [{
            label: '日毎のチャンク文/フレーズ発声回数',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            borderColor: 'rgba(75, 192, 192, 1)',
            borderWidth: 1,
            data: this.chunk_sentence_pronounced_data
          }]
        },
        options: {
          scales: {
            x: {
              title: {
                display: true,
                text: '日付',
                align: 'center',
                padding: 10,
              }
            },
            y: {
              title: {
                display: true,
                text: '発声回数',
                align: 'center',
                padding: 10
              },
              beginAtZero: true
            }
          }
        }
      });
    }
  },
  async mounted() {
    await this.fetchData();
  },
};
</script>
