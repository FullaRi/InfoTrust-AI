//
document.addEventListener('alpine:init', () => {

    Alpine.data('home', () => ({
        async init() {
            try {
                //this.statsData = await callApi.stats.default()

            }
            catch(err) {
                console.log(err)
                swalShowError("Impossible de traiter la requête")
            }
        },
        selectedAnalysisMethod: 'deep', // deep || online || combined
        affirmationField: "",
        selectTab (el) {
            document.querySelectorAll('.tab-option').forEach(t => {
                t.classList.remove('active');
                t.querySelector('svg').style.opacity = '0.6';
            });
            el.classList.add('active');
            el.querySelector('svg').style.opacity = '1';

            this.selectedAnalystMethod = el.dataset.tab;
        },
        onButtonAnalysisClicked () {

            const loadingMessage = `
                <div class="loading-content" style="font-size: 1.5em;color:white">
                  <p><strong>Analyse en cours...</strong></p>
                  <br />
                  <br />
                  <p>Veuillez patienter quelques secondes.</p>
                </div>
              `

            swalShowLoading(loadingMessage)

            const timeout = setTimeout(() => {
                Swal.close();
                window.location.href = `/report`
            }, 5 * 1000)

        }
    }))

})
