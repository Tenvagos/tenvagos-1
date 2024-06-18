window.onload = function() {
    var hoy = new Date();
    var dd = String(hoy.getDate()).padStart(2, '0');
    var mm = String(hoy.getMonth() + 1).padStart(2, '0');
    var yyyy = hoy.getFullYear();

    hoy = yyyy + '-' + mm + '-' + dd;
    document.getElementById("start_date").setAttribute("min", hoy);
    document.getElementById("end_date").setAttribute("min", hoy);
}
