<template>
    <div class="home">
        <h1>Datahoarder</h1>

        <vk-grid class="uk-child-width-1-2">
            <div>
                <h2>Active sources <vk-button type="primary" size="small" v-on:click="$router.push('add-source')">Add source</vk-button></h2>

                <vk-table justified :data="active_sources_table">
                    <vk-table-column title="Name" cell="name"></vk-table-column>
                </vk-table>
            </div>
            <div>
                <h2>Download activity</h2>
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
            active_sources: null
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
                    name: this.active_sources[source].source.meta.friendly_name
                })
            }

            return sources
        }
    },
    methods: {
        refresh_server() {

            this.axios
                .get('http://localhost:4040/api/get-active-sources')
                .then((response) => {
                    this.active_sources = response.data
                })

        }
    },
    mounted() {

        this.refresh_server()

    }
}
</script>

<style lang="scss">
    .home {
        max-width: 1050px;
        margin: 0 auto;
    }
</style>
