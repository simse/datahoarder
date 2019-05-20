<template>
    <div class="home">
        <h1>Datahoarder</h1>

        <vk-grid class="uk-child-width-1-2 ">
            <div>
                <h2>Active sources <vk-button type="primary" size="small" v-on:click="$router.push('add-source')">Add source</vk-button></h2>

                <vk-button
                        type="link"
                        v-on:click="sync_now()">
                    <vk-icon icon="refresh"></vk-icon> Sync now
                </vk-button>

                <table class="uk-table uk-table-justify">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Size</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="source in active_sources_table" v-bind:key="source.name">
                            <td>{{ source.name }}</td>
                            <td>{{ source.size }}</td>
                            <td><vk-label :type="source.status_style">{{ source.status }}</vk-label></td>
                            <td>
                                <a v-on:click="remove_source(source.uid)">
                                    <vk-icon icon="trash"></vk-icon>
                                    Remove</a>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
            <div>
                <h2>Download activity</h2>

                <vk-table :data="download_status_table" justified>
                    <vk-table-column title="Filename" cell="filename"></vk-table-column>
                    <vk-table-column title="Progress" cell="progress"></vk-table-column>
                </vk-table>
            </div>
        </vk-grid>
    </div>
</template>

<script>
// @ is an alias to /src

import VkTableColumn from "vuikit/src/library/table/components/table--column";
export default {
    name: 'home',
    components: {VkTableColumn},
    data() {
        return {
            active_sources: null,
            download_status: null
        }
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
                    name: this_source.source.meta.friendly_name,
                    size: this.human_bytes(this_source.size),
                    status: this_source.status,
                    status_style: status_style,
                    uid: this_source.source.meta.uid
                })
            }

            return sources
        },

        download_status_table() {
            if(this.download_status === null) {
                return []
            }

            let statuses = []

            this.download_status.forEach((status) => {
                statuses.push({
                    filename: status['filename'],
                    progress: status['progress'] + '%'
                })
            })

            return statuses
        }
    },
    methods: {
        refresh_server() {

            this.axios
                .get(this.datahoarder_url + 'get-active-sources', {timeout:1000})
                .then((response) => {
                    this.active_sources = response.data
                })

            this.axios
                .get(this.datahoarder_url + 'download-status', {timeout:1000})
                .then((response) => {
                    this.download_status = response.data
                })

        },

        human_bytes(bytes) {
            let decimals = 1

            if(bytes == 0) return '0 Bytes';
            let k = 1024,
                dm = decimals <= 0 ? 0 : decimals || 2,
                sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'],
                i = Math.floor(Math.log(bytes) / Math.log(k));
            return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
        },

        remove_source(source) {
            this.axios.get(this.datahoarder_url + 'remove-source', {
                params: {
                    source_id: source
                }
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
    }
}
</script>

<style lang="scss">
    .home {
        max-width: 1250px;
        margin: 0 auto;
        padding-top: 50px;
    }
</style>
