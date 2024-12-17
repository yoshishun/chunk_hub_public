import { createRouter, createWebHistory } from 'vue-router';

import LoginView from '../views/account/Login-View.vue'; 
import RegisterView from '../views/account/Register-View.vue'; 
import ProfileView from '../views/account/Profile-View.vue'; 

import IndexView from '../views/Index-View.vue'; 
import NotFoundView from '../views/NotFound-View.vue'; 

import PyvisView from '../views/Pyvis-View.vue'; 

import FoldersListView from '../views/folders/List-View.vue'; 

import ChunksListView from '../views/chunks/List-View.vue'; 
import ChunksListAddView from '../views/chunks/Add-View.vue'; 
import ChunksListEditView from '../views/chunks/Edit-View.vue'; 

import ChunkSentencesListView from '../views/chunk_sentences/List-View.vue'; 
import ChunkSentencesListCreateView from '../views/chunk_sentences/Create-View.vue'; 
import ChunkSentencesListEditView from '../views/chunk_sentences/Edit-View.vue'; 

import SpeakMoreSelectView from '../views/speak_more/Select-View.vue'; 
import SpeakMorePracticeView from '../views/speak_more/Practice-View.vue'; 
import SpeakMoreResultView from '../views/speak_more/Result-View.vue';  

import StatisticsView from '../views/Statistics-View.vue'; 

import UsageView from '../views/Usage-View.vue'; 

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { name: 'Login', path: '/account/login', component: LoginView, meta:{title: 'ログイン'}}, 
    { name: 'Register', path: '/account/register', component: RegisterView, meta:{title: 'アカウント登録'}}, 
    { name: 'Profile', path: '/account/profile', component: ProfileView, meta:{title: 'プロフィール'}}, 

    { name: 'Index', path: '/', component: IndexView, meta:{title: 'ホーム'}}, 
    { name: 'NotFound', path: '/:catchAll(.*)', component: NotFoundView, meta:{title: 'ページが見つかりません'}}, 

    { name: 'Pyvis', path: '/pyvis', component: PyvisView, meta:{title: 'チャンクネットワーク'}}, 

    { name: 'Folders-List', path: '/folders/list', component: FoldersListView, meta:{title: 'フォルダリスト'}}, 

    { name: 'Chunks-List', path: '/chunks/list', component: ChunksListView, meta:{title: 'チャンクリスト'}}, 
    { name: 'Chunks-List-Add', path: '/chunks/list/add', component: ChunksListAddView, meta:{title: 'チャンク追加'}}, 
    { name: 'Chunks-List-Edit', path: '/chunks/list/edit', component: ChunksListEditView, meta:{title: 'チャンク編集'}}, 

    { name: 'Chunk-Sentences-List', path: '/chunk_sentences/list', component: ChunkSentencesListView, meta:{title: 'チャンク文/フレーズリスト'}}, 
    { name: 'Chunk-Sentences-List-Create', path: '/chunk_sentences/list/create', component: ChunkSentencesListCreateView, meta:{title: 'チャンク文/フレーズリスト追加'}}, 
    { name: 'Chunk-Sentences-List-Edit', path: '/chunk_sentences/list/edit', component: ChunkSentencesListEditView, meta:{title: 'チャンク文/フレーズリスト編集'}}, 

    { name: 'Speak-More-Select', path: '/speak_more/select', component: SpeakMoreSelectView, meta:{title: '発声練習選択'}},
    { name: 'Speak-More-Practice', path: '/speak_more/practice', component: SpeakMorePracticeView, meta:{title: '発声練習'}},
    { name: 'Speak-More-Result', path: '/speak_more/result', component: SpeakMoreResultView, meta:{title: '発声練習結果'}},
    
    { name: 'Statistics', path: '/statistics', component: StatisticsView, meta:{title: '学習統計'}}, 

    { name: 'Usage', path: '/usage', component: UsageView, meta:{title: '使い方'}}, 
  ],
});

export default router;
