document.addEventListener('DOMContentLoaded', (event) => {
    let discount = document.getElementById('reservationForm').getAttribute('data-discount')
    let id_user = document.getElementById('reservationForm').getAttribute('data-userID')
    document.getElementById('reservationForm').addEventListener('submit', function (event) {
        event.preventDefault();
        const startDate = document.getElementById('start_date').value;
        const endDate = document.getElementById('end_date').value;
        fetch(`https://tenvagoss.pythonanywhere.com/rooms?start_date="${startDate}"&end_date="${endDate}"`, {
            method: 'GET'
        })
            .then(response => response.json())
            .then(data => {
                const results = document.getElementById('results');
                results.innerHTML = ''; // Limpiar resultados anteriores
                if(data.length){
                    data.forEach(room => {
                        const div = document.createElement('div');
                        div.className = 'room';
                        div.innerHTML = ` <div class="card-reserve">
                                        <img src="../static/${room.url_imagen}" alt=" Imagen de la reserva" class="card-img-reserve">
                                        <div class="card-content-reserve">
                                            <h3 class="card-title-reserve">${room.room_name}</h3>
                                            <h4>${room.stars}<i class="bi bi-star-fill"></i></h4>
                                            <p class=""> ${room.description}</p>
                                            <p class="">Capacidad: ${room.capacity} personas</p>
                                            <p class="card-amount-reserve"> $ <del>${room.price}</del>   ${calcular_descuento(room.price, discount)}/noche</p>
                                         <button class="card-btn complete-btn" id="button-reservar" onclick="addReserve({ id_room: ${room.id_room}, start_date: '${startDate}', end_date: '${endDate}', id_user: ${id_user} ,amount : '${calcular_total_con_descuento(room.price, discount, startDate, endDate)}' })">Reservar</button>
                                        </div>
                                    </div>`;
                        results.appendChild(div);
                    });
                } else {
                    const div = document.createElement('div');
                    div.className = 'room';
                    div.innerHTML = ` <div class="reservationFrom" style="background-color: white; padding:25px; border-radius: 5px">
                                            <h3>No hay habitaciones disponibles entre las fechas seleccionadas!</h3>
                                    </div>
                                </div>`;
                    results.appendChild(div);
                }

            })
            .catch(error => console.error('Error:', error));
    });
});

const calcular_descuento = (price, discount)=>{
    let total = parseInt(price) - parseInt(price)*parseInt(discount)/100
    return total
}

const calcular_total_con_descuento = (price, discount, start, end) => {

let precio_por_noche = calcular_descuento(price, discount)
let date1 = new Date(start);
let date2 = new Date(end);
let resta = date2.getTime() - date1.getTime()
let noches = resta / (1000 * 60 * 60 * 24)

let precio_total = precio_por_noche*noches
return precio_total
}
const addReserve = async(data)=>{
    let response = await fetch('https://tenvagoss.pythonanywhere.com/reserves', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    if (!response.ok) {
        throw new Error(`Error en la petición: ${response.status}`);
    }

    const result = await response.json();
    alert('Reserva creada:', result);
    window.location.reload()

}

