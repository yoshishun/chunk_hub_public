import { createApp } from 'vue';
import App from './Index-Layout.vue';
import router from './router';
import store from './store'; 

import 'vuetify/styles';
import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import { aliases, mdi } from 'vuetify/iconsets/mdi-svg';

import './registerServiceWorker';

const vuetify = createVuetify({
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
  components,
  directives,
});

const app = createApp(App);

router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title = to.meta.title;
  }
  next();
});

app.use(router);
app.use(store); 
app.use(vuetify);
app.mount('#app');
