const _callApi = async (path, method = "get", data = {}) => {

    // const csrfToken = Cookies.get('csrftoken')
    const endPointApiUrl = Alpine.store('settings').apiUrl

    let headers = {};
    // let headers = {
    //     'X-Requested-With': 'XMLHttpRequest',
    //     'Content-Type': 'application/json'
    // };

    // if (csrfToken){
    //   headers['X-CSRFToken'] = csrfToken;
    // }

    swalShowLoading()

    let resp = null
    if (method === "get")
        resp = await axios({
            url: `${endPointApiUrl}${path}`,
            method,
            params: data,
            headers: headers
            //timeout: 10000
        })
    else
        // For other method type
        resp = await axios({
            url: `${endPointApiUrl}${path}`,
            method,
            data,
            headers: headers
            //timeout: 10000
        })
    Swal.close();
    return resp
}

const _callDownloadFileApi = async (path, data = {}) => {

    // const csrfToken = getCookie('csrftoken')
    const endPointApiUrl = Alpine.store('settings').apiUrl
    let headers = {}
    // let headers = {
    //     'X-Requested-With': 'XMLHttpRequest',
    //     'Content-Type': 'application/json'
    // };

    // if (csrfToken){
    //   headers['X-CSRFToken'] = csrfToken
    // }

    // For other method type
    return axios({
        url: `${endPointApiUrl}${path}`,
        method: 'get',
        data,
        headers: headers,
        responseType: 'blob',
        //timeout: 10000
    })
};

const apiClient = {
    account: {
        // async getMe() {
        //     const resp = await _callApi('/users/me/', 'get')
        //     return resp.data
        // },
        // async updatePassword(data) {
        //     const resp = await _callApi('/users/me-set-password/', 'post', data)
        //     return resp.data
        // },
        // async logout() {
        //     const resp = await _callApi('/auth/logout/', 'get')
        //     return resp.data
        // }
    },
    prediction: {
        async fakeNews (detectionType, userInput) {
            const resp = await _callApi('/fake-news-detection', 'post', {
                detection_type: detectionType,
                user_input: userInput
            })
            return resp.data
        }
    }
}
