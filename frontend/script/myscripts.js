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
document.getElementById('reservationForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const checkin = document.getElementById('checkin').value;
    const checkout = document.getElementById('checkout').value;
    const roomType = document.getElementById('roomType').value;

    if (new Date(checkin) >= new Date(checkout)) {
        alert('La fecha de salida debe ser posterior a la fecha de entrada.');
        return;
    }

    alert(`Reserva realizada para la habitación ${roomType} del ${checkin} al ${checkout}.`);
});



