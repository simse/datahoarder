<template>
    <div class="add-source">
        <vk-notification :messages.sync="messages"></vk-notification>

        <vk-button-link disabled type="link" v-on:click="$router.push('/')"> Go back</vk-button-link>

        <h1>Add source</h1>
        <p>Welcome to the "Source Store", so to speak. Here you'll find hundreds of sources to fill your archive of data. And you can even add a custom source from sources with common patterns, if you dare.</p>

        <div class="new-sources">
            <h3>Available sources</h3>

            <vk-grid matched>
                <div class="source-card uk-width-1-3@m" v-for="source in new_available_sources" v-bind:key="source.meta.id">
                    <vk-card>
                        <div slot="header">
                            <div class="source-image">
                                <img :src="'http://localhost:4040/ui/img/sources/' + source.meta.id + '.png'" :alt="source.meta.friendly_name" />
                            </div>
                        </div>

                        <div slot="footer">
                            <vk-button-link disabled type="primary" :ref="source.meta.id" v-on:click="quick_add_source(source.meta.id)"> Add source</vk-button-link>
                        </div>

                        <vk-card-title>{{ source.meta.friendly_name }}</vk-card-title>
                        <p>{{ source.meta.short_description }}</p>
                    </vk-card>
                </div>
            </vk-grid>

        </div>

        <div class="loading-sources" v-if="this.available_sources === null">
            <vk-spinner ratio="1.5"></vk-spinner>
            <h3>Loading available sources...</h3>
        </div>
    </div>
</template>

<script>
    export default {
        name: "AddSource",
        data() {
            return {
                available_sources: null,
                messages: []
            }
        },
        computed: {
            new_available_sources() {
                let sources = []

                if(this.available_sources === null) {
                    return []
                }

                for(let source in this.available_sources) {
                    if(!this.available_sources[source]['meta']['active']) {
                        sources.push(this.available_sources[source])
                    }
                }

                return sources
            }
        },
        mounted() {

            this.get_available_sources()

        },
        methods: {
            get_available_sources() {

                this.axios
                    .get('http://localhost:4040/api/get-available-sources')
                    .then((response) => {
                        this.available_sources = response.data
                    })

            },

            update_button(button) {

                button.innerHTML = 'Added source'
                button.classList.remove('uk-button-primary')
                button.classList.add('uk-button-default')
                button.classList.add('disabled')

            },

            quick_add_source(source_id) {

                // Make the request
                this.axios
                    .get('http://localhost:4040/api/add-source', {
                        params: {
                            source: source_id
                        }
                    })
                    .then((response) => {
                        if(response.data.status === 'OK') {

                            // Update button state
                            this.update_button(this.$refs[source_id][0])

                            // Show notification
                            this.messages.push('Source added')

                        } else {
                            // Show notification
                            this.messages.push('Source failed to add')
                        }
                    })

            }

        }
    }
</script>

<style lang="scss" scoped>
    .add-source {
        max-width: 1250px;
        margin: 0 auto;
    }

    .disabled {
        pointer-events: none;
    }

    .uk-card-default {
        padding: 10px;
    }

    .source-image {
        padding: 15px 50px;
    }

    .loading-sources {
        display: flex;
        width: 100%;
        min-height: 300px;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }
</style>