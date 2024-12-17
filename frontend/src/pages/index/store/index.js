import { createStore } from 'vuex';

export default createStore({
  state: {
    selectedChunkSentences: [],
    practicedChunks: [] 
  },
  mutations: {
    ADD_CHUNK(state, chunk) {
      state.selectedChunkSentences.push(chunk);
    },
    REMOVE_CHUNK(state, chunk) {
      state.selectedChunkSentences = state.selectedChunkSentences.filter(c => c.chunk_id !== chunk.chunk_id);
    },
    CLEAR_CHUNKS(state) {
      state.selectedChunkSentences = [];
    },
    SET_PRACTICED_CHUNKS(state, chunks) { 
      state.practicedChunks = chunks;
    }
  },
  actions: {
    addChunk({ commit }, chunk) {
      commit('ADD_CHUNK', chunk);
    },
    removeChunk({ commit }, chunk) {
      commit('REMOVE_CHUNK', chunk);
    },
    clearChunks({ commit }) {
      commit('CLEAR_CHUNKS');
    },
    setPracticedChunks({ commit }, chunks) { 
      commit('SET_PRACTICED_CHUNKS', chunks);
    }
  },
  getters: {
    selectedChunkSentences: state => state.selectedChunkSentences,
    practicedChunks: state => state.practicedChunks 
  }
});
