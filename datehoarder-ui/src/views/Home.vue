<template>
    <div class="home">
        <h1>Datahoarder</h1>

        <vk-grid class="uk-child-width-1-2">
            <div>
                <h2>Active sources <vk-button type="primary" size="small" v-on:click="$router.push('add-source')">Add source</vk-button></h2>

                <vk-table justified :data="active_sources_table">
                    <vk-table-column title="Name" cell="name"></vk-table-column>
                    <vk-table-column title="Size" cell="size"></vk-table-column>
                </vk-table>
            </div>
            <div>
                <h2>Download activity</h2>

                <vk-table :data="download_status_table">
                    <vk-table-column title="Filename" cell="filename"></vk-table-column>
                    <vk-table-column title="Progress" cell="progress"></vk-table-column>
                </vk-table>
            </div>
        </vk-grid>
    </div>
</template>

<script>
// @ is an alias to /src

export default {
    name: 'home',
    components: {},
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
                sources.push({
                    name: this.active_sources[source].source.meta.friendly_name,
                    size: this.human_bytes(this.active_sources[source].size)
                })
            }

            return sources
        },

        download_status_table() {

            if(this.download_status === null) {
                return []
            }

            let status = []

            for(let filename in this.download_status) {

                status.push({
                    filename: filename,
                    progress: this.download_status[filename] + '%'
                })

            }

            return status

        }
    },
    methods: {
        refresh_server() {

            this.axios
                .get('http://localhost:4040/api/get-active-sources')
                .then((response) => {
                    this.active_sources = response.data
                })

            this.axios
                .get('http://localhost:4040/api/download-status')
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

        }
    },
    mounted() {

        this.refresh_server()

        this.$nextTick(function () {
            window.setInterval(() => {
                this.refresh_server()
            }, 10000);
        })

    }
}
</script>

<style lang="scss">
    .home {
        max-width: 1050px;
        margin: 0 auto;
    }
</style>
