
const Toast = Swal.mixin({
    toast: true,
    position: "top-end",
    showConfirmButton: false,
    timer: 3000,
    timerProgressBar: true,
    didOpen: (toast) => {
        toast.onmouseenter = Swal.stopTimer;
        toast.onmouseleave = Swal.resumeTimer;
    }
});

const swalShowError = (msg) => {
    return Swal.fire({
        icon: 'error',
        title: "Erreur !",
        html: msg,
        topLayer: true
    })
}

const swalShowSuccess = (title, msg) => {
    return Swal.fire({
        icon: 'success',
        title: title,
        html: msg,
        topLayer: true
    })
}

const swalShowLoading = (message) => {
    Swal.fire({
    title: "",
    html: message,
    color: "#3D5A8A",
    background: "none",
    showConfirmButton: false,
    allowOutsideClick: false
    //backdrop: "rgba(0,0,123,0.4)"
  });
  Swal.showLoading();
};

const swalCloseLoading = () => {
  Swal.close();
  Swal.hideLoading();
};


const appEvent = {
    'REFRESH_xxxx': 'refresh-xxx',
}



