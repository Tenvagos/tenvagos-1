document.addEventListener('DOMContentLoaded', () => {
    const slides = document.querySelectorAll('.slide');
    const totalSlides = slides.length;
    let currentIndex = 0;

    function showSlide(index) {
        const slider = document.querySelector('.slider');
        slider.style.transform = `translateX(-${index * 100}%)`;
    }

    function nextSlide() {
        currentIndex = (currentIndex + 1) % totalSlides;
        showSlide(currentIndex);
    }

    setInterval(nextSlide, 3000); // Cambia de slide cada 3 segundos

    showSlide(currentIndex);
});

// filtro de reservas
// document.getElementById('reservationForm').addEventListener('submit', function(event) {
//     event.preventDefault();

//     const checkin = document.getElementById('checkin').value;
//     const checkout = document.getElementById('checkout').value;

//     if (new Date(checkin) >= new Date(checkout)) {
//         alert('La fecha de salida debe ser posterior a la fecha de entrada.');
//         return;
//     }

//     alert('Las siguientes habitaciones están disponibles desde ${checkin} hasta ${checkout}.');
// });

/////////////////////////////////////////////////////////////////////////////////////////////////////////
////////////REVISAR Y ADAPTAR ///////////////////////////////////////////////////////////////////////////

/*
document.getElementById('reservation-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Evita el envío del formulario

    // Captura los datos del formulario
    const roomType = document.getElementById('room-type').value;
    const checkInDate = document.getElementById('check-in').value;
    const checkOutDate = document.getElementById('check-out').value;

    // Validar fechas
    if (new Date(checkInDate) >= new Date(checkOutDate)) {
        document.getElementById('reservation-status').textContent = 'La fecha de salida debe ser después de la fecha de entrada.';
        return;
    }

    // Verificar disponibilidad
    $.ajax({
        url: '/check_availability',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            roomType: roomType,
            checkInDate: checkInDate,
            checkOutDate: checkOutDate
        }),
        success: function(response) {
            if (response.available) {
                // Hacer la reserva
                $.ajax({
                    url: '/make_reservation',
                    type: 'POST',
                    contentType: 'application/json',
                    data: JSON.stringify({
                        roomType: roomType,
                        checkInDate: checkInDate,
                        checkOutDate: checkOutDate
                    }),
                    success: function(reservationResponse) {
                        document.getElementById('reservation-status').textContent = `Reserva exitosa! Precio total: $${reservationResponse.totalPrice.toFixed(2)}. Precio con descuento: $${reservationResponse.discountedPrice.toFixed(2)}.`;
                    }
                });
            } else {
                document.getElementById('reservation-status').textContent = 'No hay habitaciones disponibles para las fechas seleccionadas.';
            }
        }
    });
});
*/