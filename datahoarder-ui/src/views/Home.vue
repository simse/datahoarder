<template>
    <div class="home">
        <h1 class="title">Dashboard</h1>

        <div class="no-connection" :class="{'active': this.no_connection}">
            <b-spinner label="Loading..." style="width: 3rem; height: 3rem;margin-bottom: 40px;"></b-spinner>

            <h1>Lost connection to Datahoarder!</h1>
            <p>I'll keep trying to reconnect, while you figure out what's wrong.</p>
        </div>

        <b-row>
            <b-col>
                <ActiveSources />
                
            </b-col>
            <b-col>
                <DownloadActivity />
            </b-col>
        </b-row>
    </div>
</template>

<script>
import ActiveSources from '@/components/ActiveSources'
import DownloadActivity from '@/components/DownloadActivity'

// @ is an alias to /src
export default {
    name: 'home',
    components: {
        ActiveSources,
        DownloadActivity
    },
    data() {
        return {
            
        }
    },
    computed: {
        
    },
    methods: {
        verify_connection() {
            this.axios
                .get(this.datahoarder_url, {timeout:2000})
                .then(() => {
                    this.no_connection = false
                })
                .catch(() => {
                    this.no_connection = true
                })
        },
    },
    mounted() {
        // Make sure server isn't refreshed twice or more per cycle
        if(window.myInterval != undefined && window.myInterval != 'undefined'){
            window.clearInterval(window.myInterval);
        }

        this.$nextTick(function () {
            window.myInterval = window.setInterval(() => {
                this.verify_connection()
            }, 1000);
        })
    }
}
</script>

<style lang="scss">
.no-connection {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.8);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: #fff;
    opacity: 0;
    transition: opacity .2s;
    z-index: -20;

    &.active {
        opacity: 1;
        z-index: 1000;
    }

    h1 {
        font-weight: 300;
    }
}

.home {
    max-width: 1400px;
    margin: 0 auto;
    padding-top: 50px;
}

.title {
    font-weight: 800;
    margin-bottom: 35px;
}

.dashboard-card {
    background: #fff;
    padding: 22px;
    border-radius: 8px;
    box-shadow: 0px 7px 20px 0px rgba(0,5,61,0.05);

    h2 {
        font-size: 1.4rem;
        margin-bottom: 20px;
    }
}

.empty {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100px;
    height: 90%;

    span {
        opacity: .5;
        font-size: 1.2rem;
    }
}
</style>
