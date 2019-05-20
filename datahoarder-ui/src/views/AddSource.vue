<template>
    <div class="add-source">

        <vk-notification :messages.sync="messages"></vk-notification>

        <vk-button-link disabled type="link" v-on:click="$router.push('/')"> Go back</vk-button-link>

        <h1>Add source</h1>
        <p>Welcome to the "Source Store", so to speak.
            Here you'll find hundreds of sources to fill your archive of data.
            And you can even add a custom source from sources with common patterns, if you dare.</p>

        <vk-grid>

            <div class="uk-width-1-6@m">

                <vk-nav>
                    <vk-nav-item-header title="Categories"></vk-nav-item-header>

                    <vk-nav-item
                            title="All"
                            v-on:click="change_cat(null)"
                            :active="current_cat === null"
                    ></vk-nav-item>

                    <vk-nav-item
                            :title="cat_friendly_name(cat)"
                            v-on:click="change_cat(cat)"
                            v-for="cat in categories"
                            v-bind:key="cat"
                            :active="current_cat === cat"
                    ></vk-nav-item>
                </vk-nav>

            </div>

            <div class="uk-width-5-6@m">



                <div class="new-sources">
                    <h3>{{ page_subtitle }}</h3>

                    <vk-grid matched v-vk-height-match="'.uk-card-body > div'">
                        <div class="source-card uk-width-1-3@m"
                             v-for="source in sources"
                             v-bind:key="source.id">
                            <div class="uk-card uk-card-default">

                                <div class="uk-card-header">
                                    <div class="source-image">
                                        <img :src="'/ui/img/sources/' + source.id + '.png'"
                                             :alt="source.friendly_name" />
                                    </div>
                                </div>

                                <div class="uk-card-body">
                                    <div>
                                        <h3 class="uk-card-title">{{ source.friendly_name }}</h3>

                                        <vk-label>{{ cat_friendly_name(source.category) }}</vk-label>

                                        <p>{{ source.short_description }}</p>
                                    </div>

                                </div>


                                <div class="uk-card-footer">
                                    <vk-button-link type="primary"
                                                    :ref="source.id"
                                                    v-on:click="quick_add_source(source.id)"
                                    >Add source</vk-button-link>
                                    <vk-button-link type="link"
                                                    v-on:click="add_source_modal(source.id)"
                                    >Customize</vk-button-link>
                                </div>
                            </div>
                        </div>
                    </vk-grid>

                </div>

                <div class="loading-sources" v-if="this.available_sources === null">
                    <vk-spinner ratio="1.5"></vk-spinner>
                    <h3>Loading available sources...</h3>
                </div>

                <vk-modal overflow-auto :show="this.source_modal.show">
                    <vk-modal-title slot="header">{{ this.source_modal.title }}</vk-modal-title>

                    <div>

                        <form>
                            <label>
                                Source arguments (JSON):
                                <textarea class="uk-textarea" v-model="source_modal.args_data"></textarea>
                            </label>
                        </form>

                    </div>

                    <div slot="footer">

                        <vk-button-link
                                type="primary"
                                v-on:click="add_source(source_modal.id, source_modal.args_data)"
                        >Add source</vk-button-link>

                    </div>
                </vk-modal>

            </div>

        </vk-grid>
    </div>
</template>

<script>
    export default {
        name: "AddSource",
        data() {
            return {
                available_sources: null,
                messages: [],
                current_cat: null,
                max_height: 0,
                source_modal: {
                    show: false,
                    title: '',
                    args: {},
                    args_data: '',
                    id: ''
                }
            }
        },
        computed: {
            passive_sources() {
                let sources = []

                if(this.available_sources === null) {
                    return []
                }

                for(let source in this.available_sources) {
                    if(!this.available_sources[source]['active']) {
                        sources.push(this.available_sources[source])
                    }
                }

                return sources
            },

            sources() {
                let cat_sources = []

                if(this.current_cat === null) {
                    return this.passive_sources
                } else {
                    for(let source in this.passive_sources) {
                        if(this.passive_sources[source]['category'] === this.current_cat) {
                            cat_sources.push(this.passive_sources[source])
                        }
                    }
                }

                return cat_sources
            },

            categories() {
                let cats = []

                if(this.available_sources === null) {
                    return []
                }

                for(let source in this.available_sources) {
                    let cat = this.available_sources[source]['category']

                    if(!cats.includes(cat)) {
                        cats.push(cat)
                    }
                }

                return cats
            },

            page_subtitle() {
                if(this.current_cat === null) {
                    return 'All available sources'
                } else {
                    return this.cat_friendly_name(this.current_cat) + ' sources'
                }
            }
        },
        mounted() {

            this.get_available_sources()

        },
        methods: {
            get_available_sources() {
                this.axios
                    .get(this.datahoarder_url + 'get-available-sources')
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
                .get(this.datahoarder_url + 'add-source', {
                    params: {
                        source: source_id
                    }
                })
                .then((response) => {
                    if(response.data.status === 'OK') {
                        // Update button state
                        this.update_button(this.$refs[source_id][0])

                        // Show notification
                        this.$toasted.show('Source added: ' + source_id, {
                            duration: 5000,
                            position: 'top-center'
                        })
                    } else {
                        // Show notification
                        this.messages.push('Source failed to add')
                    }
                })
            },

            add_source_modal(source_id) {
                let source = this.available_sources.filter(obj => {
                    return obj.id === source_id
                })[0]

                let required_args = source['args']

                this.source_modal.show = true
                this.source_modal.title = 'Customize ' + source['friendly_name']
                this.source_modal.args = required_args
                this.source_modal.id = source_id
            },

            add_source(source_id, args) {
                this.axios
                    .get(this.datahoarder_url + 'add-source', {
                        params: {
                            source: source_id,
                            args: args
                        }
                    })
                    .then((response) => {
                        if(response.data.status === 'OK') {
                            // Update button state
                            this.update_button(this.$refs[source_id][0])

                            // Show notification
                            this.$toasted.show('Source added: ' + source_id, {
                                duration: 5000,
                                position: 'top-center'
                            })
                        } else {
                            // Show notification
                            this.messages.push('Source failed to add')
                        }
                    })

            },

            change_cat(cat) {

                this.current_cat = cat

            },

            cat_friendly_name(cat) {

                return cat.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())

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

    .uk-card-footer {
        margin-top: auto;
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
