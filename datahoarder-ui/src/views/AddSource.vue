<template>
    <div class="add-source">
        <b-button variant="link" @click="$router.push('/')" class="back"><font-awesome-icon icon="arrow-left" /> Go back</b-button>

        <h1 class="title">Add source</h1>
        <p>Welcome to the "Source Store", so to speak.
            Here you'll find hundreds of sources to fill your archive of data.
            And you can even add a custom source from sources with common patterns, if you dare.</p>

        <b-row>

            <b-col cols="3">
                <h2>Categories</h2>

                <b-nav vertical>
                    <b-nav-item 
                        :active="current_cat === null"
                        @click="change_cat(null)"
                    >All</b-nav-item>

                    <b-nav-item
                        v-on:click="change_cat(cat)"
                        v-for="cat in categories"
                        v-bind:key="cat"
                        :active="current_cat === cat"
                        >{{ cat_friendly_name(cat) }}</b-nav-item>
                </b-nav>
            </b-col>

            <b-col cols="9">
                <div class="new-sources">
                    <h2>{{ page_subtitle }}</h2>

                    <b-row no-gutters v-match-heights="{el:['.source-card']}">
                        <b-col
                            cols="6"
                            v-for="source in sources"
                            v-bind:key="source.id">

                            <div class="source-card">
                                <div class="source-image">
                                    <img 
                                        :src="'/ui/img/sources/' + source.id + '.png'"
                                        :alt="source.friendly_name" />
                                </div>

                                <div class="meta">
                                    <h4 class="source-title">{{ source.friendly_name }}</h4>
                                    <p class="source-desc">{{ source.short_description }}</p>

                                    <b-button 
                                        pill 
                                        variant="primary" 
                                        size="sm"
                                        :ref="source.id"
                                        @click="add_source_modal(source.id)"
                                    >Add source</b-button>
                                </div>
                            </div>
                        </b-col>
                    </b-row>

                </div>

                <div class="loading-sources" v-if="this.available_sources === null">
                    <vk-spinner ratio="1.5"></vk-spinner>
                    <h3>Loading available sources...</h3>
                </div>

                <b-modal
                    v-model="source_modal.show"
                    :title="source_modal.title">

                    <div>
                        <form>
                            <div class="uk-margin" v-for="(arg, index) in this.source_modal.args" :key="arg.name">
                                <b-form-group
                                    v-if="arg.type == 'str'"
                                    :label="arg.friendly_name ? arg.friendly_name : arg.name"
                                    description=""
                                >
                                    <b-form-input
                                        v-model="source_modal.args[index].value"
                                        type="text"
                                    ></b-form-input>
                                </b-form-group>

                                <label v-if="arg.type == 'boolean'">
                                    <b-form-checkbox v-model="source_modal.args[index].value">{{ arg.friendly_name ? arg.friendly_name : arg.name }}</b-form-checkbox>
                                </label>

                                <label v-if="arg.type == 'select'">
                                    {{ arg.friendly_name ? arg.friendly_name : arg.name }}:
                                    <b-form-select v-model="source_modal.args[index].value" :options="arg.options" :multiple="arg.multiple"></b-form-select>
                                </label>
                            </div>
                        </form>
                    </div>

                    <div slot="modal-ok">
                        <span @click="add_source(source_modal.id, source_modal.args)">Add source</span>
                    </div>
                </b-modal>

            </b-col>

        </b-row>
    </div>
</template>

<script>
    export default {
        name: "AddSource",
        data() {
            return {
                available_sources: null,
                current_cat: null,
                max_height: 0,
                source_modal: {
                    show: false,
                    title: '',
                    args: {},
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
                        this.$toasted.show('Source failed to add')
                    }
                })
            },

            add_source_modal(source_id) {
                let source = this.available_sources.filter(obj => {
                    return obj.id === source_id
                })[0]

                let required_args = source['args']
                required_args.forEach(arg => {
                    arg.value = arg.default
                });

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
h2 {
    font-size: 1.4rem;
    margin-bottom: 20px;
}

.add-source {
    max-width: 1250px;
    margin: 0 auto;
}

.disabled {
    pointer-events: none;
}

.loading-sources {
    display: flex;
    width: 100%;
    min-height: 300px;
    justify-content: center;
    align-items: center;
    flex-direction: column;
}

.source-card {
    background: #fff;
    padding: 17px;
    border-radius: 8px;
    box-shadow: 0px 7px 20px 0px rgba(0,5,61,0.05);
    display: flex;
    align-items: center;
    margin-right: 20px;
    min-height: 155px;

    .btn {
        padding: 2px 8px;
    }

    .source-title {
        font-size: 1.1rem;
    }

    .source-image {
        margin-right: 20px;

        img {
            max-height: 80px;
        }
    }
}

.back {
    padding-left: 0px;
    margin: 20px 0;
}
</style>
