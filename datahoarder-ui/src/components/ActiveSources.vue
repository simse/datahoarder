<template>
    <div class="active-sources dashboard-card">
        <h2>Active sources <b-button variant="primary" pill size="sm" @click="$router.push('add-source')">Add source</b-button></h2>

        <div class="empty" v-if="this.active_sources_table.length < 1">
            <span>No active sources</span>
        </div>

        <div v-if="this.active_sources_table.length > 0">
            <b-table-simple class="">
                <b-tbody>
                    <tr v-for="source in active_sources_table" v-bind:key="source.uid">
                        <td>{{ source.name }}</td>
                        <td>{{ source.size }}</td>
                        <td><b-badge :variant="source.status_style">{{ source.status }}</b-badge></td>
                        <td>
                            <b-button
                                @click="delete_source(source.uid)"
                                pill
                                size="sm"
                                variant="danger">
                                <font-awesome-icon icon="trash-alt" />
                            </b-button>
                        </td>
                    </tr>
                </b-tbody>
            </b-table-simple>

            <b-button
                    variant="link"
                    @click="sync_now()">
                <font-awesome-icon icon="sync" />
                Sync now
            </b-button>
        </div>
    </div>
</template>

<script>
import HumanFunctions from '@/mixins/HumanFunctions.js';

export default {
    name: 'ActiveSources',
    mixins: [HumanFunctions],
    props: {

    },
    data() {
        return {
            active_sources: null,
            delete_modal: {
                source_name: null,
                source_uid: null,
                shown: true
            }
        }
    },
    mounted() {
        this.refresh_server()

        // Make sure server isn't refreshed twice or more per cycle
        if(window.myInterval != undefined && window.myInterval != 'undefined'){
            window.clearInterval(window.myInterval);
        }

        this.$nextTick(function () {
            window.myInterval = window.setInterval(() => {
                this.refresh_server()
            }, 1000);
        })
    },
    computed: {
        active_sources_table() {
            if(this.active_sources === null) {
                return []
            }

            let sources = []

            for(let source in this.active_sources) {
                let this_source = this.active_sources[source]
                let status_style = 'success'

                if(this_source.source == undefined) {
                    continue
                }

                if(this_source.status === 'searching' || this_source.status === 'downloading') {
                    status_style = ''
                }

                if(this_source.status === 'Unknown') {
                    status_style = 'warning'
                }

                sources.push({
                    name: this_source.source.meta.unique_name,
                    size: this.human_bytes(this_source.size),
                    status: this_source.status,
                    status_style: status_style,
                    uid: this_source.source.meta.uid
                })
            }

            return sources
        },
    },
    methods: {
        refresh_server() {
            this.axios
                .get(this.datahoarder_url + 'get-active-sources', {timeout:1000})
                .then((response) => {
                    this.active_sources = response.data
                })
        },
        sync_now() {
            this.axios
                .get(this.datahoarder_url + 'sync', {timeout:2000})
                .then(() => {
                    this.$toasted.show('Syncing sources', {
                        duration: 5000,
                        position: 'top-center'
                    })
                })
        },
        delete_source(uid) {
            this.$bvModal.msgBoxConfirm("Are you sure?", {
                centered: true
            }).then(confirmed => {
                if(confirmed) {
                    this.axios.get(this.datahoarder_url + 'remove-source', {
                        params: {
                            source_id: uid
                        }
                    }).then(() => {
                        this.$toasted.show('Deleted source.', {
                            position: 'top-center'
                        })
                    })
                }
            })
        }
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
h2 {
    button {
        margin-left: 5px;
        padding: 0.12rem 0.5rem;
    }
}

table {
    margin-top: 20px;
}
</style>
