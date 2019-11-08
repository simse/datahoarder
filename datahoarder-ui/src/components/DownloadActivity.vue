<template>
    <div class="download-activity dashboard-card">
        <h2>Download activity</h2>

        <b-table
            :items="download_status_table"
            v-if="this.download_status_table.length > 0"
            sort-by="progress"
            thead-class="hidden_header"
            >
            <template v-slot:cell(progress)="data">
                <span v-if="data.value == -1">Checking...</span>
                <span v-if="data.value > -1">{{ data.value }}%</span>
                <b-progress v-if="data.value > -1" height="4px" :value="data.value"></b-progress>
            </template>
        </b-table>

        <div class="empty" v-if="this.download_status_table.length < 1">
            <span>No active downloads</span>
        </div>
    </div>
</template>

<script>
import HumanFunctions from '@/mixins/HumanFunctions.js';

export default {
    name: 'DownloadActivity',
    mixins: [HumanFunctions],
    props: {

    },
    data() {
        return {
            download_status: null
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
        download_status_table() {
            if(this.download_status === null) {
                return []
            }

            let statuses = []

            this.download_status.forEach((status) => {
                if(true) {
                    statuses.push({
                        filename: status['filename'].replace(/^.*[\\\/]/, ''),
                        progress: status['progress']
                    })
                }
            })

            return statuses
        }
    },
    methods: {
        refresh_server() {
            this.axios
                .get(this.datahoarder_url + 'download-status', {timeout:1000})
                .then((response) => {
                    this.download_status = response.data
                })
        },

    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style lang="scss">
.hidden_header {
    display: none !important;
}

tr:first-child td {
    border: 0;
}
</style>
