document.getElementById('reservationForm').addEventListener('submit', function(event) {
    var startDate = new Date(document.getElementById('start_date').value);
    var endDate = new Date(document.getElementById('end_date').value);

    if (startDate > endDate) {
        event.preventDefault();
        alert('La fecha de entrada no puede ser posterior a la fecha de salida.');
        location.reload();
    }
});
