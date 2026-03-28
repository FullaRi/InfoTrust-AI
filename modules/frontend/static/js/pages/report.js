//
document.addEventListener('alpine:init', () => {

    Alpine.data('report', () => ({
        async init() {
            try {
                const analystDataKey = Alpine.store('settings').analystDataKey;

                if (!localStorage.getItem(analystDataKey)) {
                    window.location.href = `/`;
                    return;
                }

                this.loadAnalystData();
            }
            catch(err) {
                console.log(err)
                swalShowError("Oups, une erreur est survenue. Merci de merci de ressayer plus tard.")
            }
        },
        analystData: {
            user_input: "",
            credibility_score: 0,
            detection_type: "",
            explanation: "",
            final_decision: "",
            sources_for_investigation: [],
            status: "",
            status_description: ""
        },
        loadAnalystData () {
            const analystDataKey = Alpine.store('settings').analystDataKey;
            const analystData = JSON.parse(localStorage.getItem(analystDataKey));

            console.log("Loaded Analyst data : ", analystData);

            this.analystData.user_input = analystData.user_input;
            this.analystData.credibility_score = analystData.credibility_score;
            this.analystData.detection_type = analystData.detection_type;
            this.analystData.explanation = analystData.explanation;
            this.analystData.final_decision = analystData.final_decision;
            this.analystData.sources_for_investigation = analystData.sources_for_investigation;
            this.analystData.status = analystData.status;
            this.analystData.status_description = analystData.status_description;

            localStorage.removeItem(analystDataKey);
        },
        getStatusColor (detection_type, status) {
            const s = status.toUpperCase().trim();

            const mapping = {

                'AGENT__DEEP_LEARNING': {
                    'VERIFIED': 'badge-success',   // Vert
                    'MIXED': 'badge-info',        // Bleu
                    'WARNING': 'badge-warning',    // Orange
                    'FALSE': 'badge-error',       // Rouge
                    'UNCERTAIN': 'badge-ghost'     // Gris transparent
                    },


                'AGENT': {
                    'HIGHLY CREDIBLE': 'badge-success',
                    'MODERATELY CREDIBLE': 'badge-info',
                    'LOW CREDIBILITY': 'badge-warning',
                    'VERY LIKELY FAKE': 'badge-error',
                    'UNVERIFIABLE': 'badge-ghost'
                },


                'DEEP_LEARNING': {
                    'CREDIBLE': 'badge-success',
                    'MIXED': 'badge-warning',
                    'NOT CREDIBLE': 'badge-error'
                }
            };

            const colorClass = mapping[detection_type]?.[s] || 'badge-neutral';

            return colorClass;
        },
        getDetectionTypeDescription (detectionType) {
            if (detectionType === "DEEP_LEARNING")
                return "Analyse Sémantique";
            else if (detectionType === "AGENT")
                return "Vérification Factuelle";
            else if (detectionType === "AGENT__DEEP_LEARNING")
                return "Analyse Complète";
            else
                return ""
        },
        getHostname(url) {
            try {
                const hostname = new URL(url).hostname;
                const parts = hostname.split('.');

                // Handle special cases like .co.uk, .com.au, etc.
                if (parts.length >= 3 && (parts[parts.length - 2] === 'co' ||
                    parts[parts.length - 2] === 'com' ||
                    parts[parts.length - 2] === 'gov')) {
                  return parts[parts.length - 3];
                }

                // For standard domains like google.com
                return parts[parts.length - 2];
                } catch (e) {
                return null;
            }
        }
    }))

})
