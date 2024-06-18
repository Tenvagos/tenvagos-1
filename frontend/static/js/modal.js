

// Función para confirmar la reserva
function confirmarReserva(descuento, id_user, id_room) {
    console.log(descuento, id_user, id_room)
    // Obtener las fechas seleccionadas
    let fechaEntrada = document.getElementById(`start_date_modal-'${id_user}'`).value;
    let fechaSalida = document.getElementById(`end_date_modal-'${id_user}'`).value;

    if (fechaEntrada > fechaSalida) {
        alert("La fecha de entrada no puede ser posterior a la fecha de salida");
        location.reload();
        return false;
    }
    // Mostrar el mensaje de confirmación
    let mensajeConfirmacion = "¿Deseas confirmar la reserva con las siguientes fechas?<br>";
    mensajeConfirmacion += "Fecha de entrada: " + fechaEntrada + "<br>";
    mensajeConfirmacion += "Fecha de salida: " + fechaSalida + "<br>";
    mensajeConfirmacion += "Monto total con descuento: $" + calcular_total_con_descuento(descuento, fechaEntrada, fechaSalida) + "<br>";


    document.getElementById('mensaje_confirmacion').innerHTML = mensajeConfirmacion;
}

// Función para realizar la reserva (simulada)
async function realizarReserva(descuento, id_user, id_room) {
    let fechaEntrada = document.getElementById(`start_date_modal-'${id_user}'`).value;
    let fechaSalida = document.getElementById(`end_date_modal-'${id_user}'`).value;
    let data = {
        id_room : id_room,
        id_user : id_user,
        start_date : fechaEntrada,
        end_date : fechaSalida,
        amount : `${calcular_total_con_descuento(descuento, fechaEntrada, fechaSalida)}`
    }
    try {
        let response = await fetch('https://tenvagoss.pythonanywhere.com/reserves', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
    
        const result = await response.json();
        alert(result.message);
        window.location.reload()
    } catch (error) {
         alert(error.message)
    }

}
const calcular_total_con_descuento = (discount, start, end) => {

    console.log(discount, start, end)
    let date1 = new Date(start);
    let date2 = new Date(end);
    let resta = date2.getTime() - date1.getTime()
    let noches = resta / (1000 * 60 * 60 * 24)
    console.log(noches)

    let precio_total = discount * noches
    return precio_total
}