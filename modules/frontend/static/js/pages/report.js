//
document.addEventListener('alpine:init', () => {

    Alpine.data('report', () => ({
        async init() {
            try {
                //this.statsData = await callApi.stats.default()

            }
            catch(err) {
                console.log(err)
                swalShowError("Impossible de traiter la requête")
            }
        },
        statsData: {},
    }))

})
