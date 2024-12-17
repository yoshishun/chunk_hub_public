<template>
  <v-container class="graph-container" style="width: 100%;">
    <h4 class="text-center">- チャンクネットワーク -</h4>
    <h1 class="text-center"></h1>

    <iframe :src="graph_html" frameborder="0" width="100%" height="600"></iframe>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      graph_html: "",
    };
  },
  methods: {
    async loadGraphHtml() {
      try {
        const response = await fetch("/api/test/pyvis");
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        const html = await response.text();
        this.graph_html = "data:text/html;charset=utf-8," + encodeURIComponent(html);
      } catch (error) {
        console.error("Error loading graph HTML:", error);
      }
    },
  },
  async mounted() {
    await this.loadGraphHtml();
  },
};
</script>
