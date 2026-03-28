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
        selectedAnalysisMethod: 'DEEP_LEARNING', // DEEP_LEARNING || AGENT || AGENT__DEEP_LEARNING
        affirmationField: "",
        selectTab (el) {
            document.querySelectorAll('.tab-option').forEach(t => {
                t.classList.remove('active');
                t.querySelector('svg').style.opacity = '0.6';
            });
            el.classList.add('active');
            el.querySelector('svg').style.opacity = '1';

            this.selectedAnalysisMethod = el.dataset.tab;
        },
        saveAnalystData (data) {
            const analystDataKey = Alpine.store('settings').analystDataKey;
            localStorage.setItem(analystDataKey, JSON.stringify(data));
        },
        async onButtonAnalysisClicked () {

            if (this.affirmationField.length < 20) {
                swalShowError("Le contenue à analyser est un peu trop court ! Utilisez au moins 20 caractères pour continuer. ").then(() => {});
                return;
            }

            if (this.affirmationField.length > 400) {
                swalShowError("Oups, le contenue à analyser est un peu trop long ! Il ne doit pas dépasser 400 caractères. Essayez une version plus courte.").then(() => {});
                return;
            }

            const dialogResult = await swal.fire({
              title: "InfoTrust AI",
              icon: "info",
              showCancelButton: true,
              confirmButtonText: "Continuer",
              cancelButtonText: "Annuler",
              reverseButtons: true,
              allowOutsideClick: false,
              html: `L'analyse est sur le point de démarrer. <br /> Continuer ?`
            });

            if (!dialogResult.isConfirmed){
              return;
            }

            const loadingMessage = `
                <div class="loading-content" style="font-size: 1.5em;color:white">
                  <p><strong>Analyse en cours...</strong></p>
                  <br />
                  <br />
                  <p>Veuillez patienter quelques secondes.</p>
                </div>
            `;

            swalShowLoading(loadingMessage);

            try {
                console.log("New analyst : ", "type = ", this.selectedAnalysisMethod, "/ content", this.affirmationField);
                const response = await apiClient.prediction.fakeNews(this.selectedAnalysisMethod, this.affirmationField);

                Swal.close();

                console.log(response);

                this.saveAnalystData({
                    user_input: this.affirmationField,
                    credibility_score: response.credibility_score,
                    detection_type: response.detection_type,
                    explanation: response.explanation,
                    final_decision: response.final_decision,
                    sources_for_investigation: response.sources_for_investigation,
                    status: response.status,
                    status_description: response.status_description,
                });

                window.location.href = `/report`;
            }
            catch(err) {
                if (err.response?.data?.message){
                  swalShowError(err.response.data.message);
                }
                else {
                  swalShowError("Impossible de traiter la requête");
                }
            }
        }
    }))
})
