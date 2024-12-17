<template>
    <v-container>
        <h1 class="text-center">ホーム</h1>

        <v-divider class="mt-4"></v-divider>

        <h3 class="text-center mt-4" style="color: grey;">
            ユーザーランキング
        </h3>

        <v-list style="word-break: break-word;" class="mt-4">
            <v-list-item v-for="(user, index) in userRankings" :key="index">

                <template v-if="$vuetify.display.xs">
                    <v-list-item-content class="d-flex flex-column">
                        <div class="d-flex flex-column">
                            <div class="d-flex justify-space-between">
                                <h5>{{ index + 1 }}. {{ user.name }}</h5>
                                <h6 style="color: grey;">総発音数: {{ user.total_pronounced_count }}</h6>
                            </div>
                        </div>
                    </v-list-item-content>
                </template>

                <template v-else>
                    <v-list-item-content class="d-flex align-center">
                        <div class="d-flex flex-column" style="width: 100%;">
                            <div class="d-flex justify-space-between">
                                <div>
                                    <h4>{{ index + 1 }}. {{ user.name }}</h4>
                                </div>
                                <div>
                                    <h5 style="color: grey;">総発音数: {{ user.total_pronounced_count }}</h5>
                                </div>
                            </div>
                        </div>
                    </v-list-item-content>
                </template>

            </v-list-item>
        </v-list>

    </v-container>
</template>

<script>
export default {
    data() {
        return {
            userRankings: [],
        };
    },
    mounted() {
        this.fetchUserRankings();
    },
    methods: {
        async fetchUserRankings() {
            try {
                const response = await fetch('/api/ranking');
                const data = await response.json();
                this.userRankings = data;
            } catch (error) {
                console.error('Error fetching user rankings:', error);
            }
        },
    },
};
</script>

<style scoped>
.v-list-item {
    border-bottom: 1px solid #ccc;
}
</style>
