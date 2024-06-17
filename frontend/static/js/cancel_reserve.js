document.querySelectorAll('.card-btn-reserve').forEach(button => {
    button.addEventListener('click', event => {
        event.preventDefault();

        const confirmation = confirm('¿Estás seguro de que querés cancelar esta reserva?');
        if (!confirmation) {
            return;
        }

        const id_user = event.target.getAttribute('data-user-id');
        const id_reserve = event.target.getAttribute('data-reserve-id');
        console.log(id_user, id_reserve)
        fetch(`https://tenvagoss.pythonanywhere.com/my_reserves/${id_user}/${id_reserve}`, {
            method: 'DELETE',
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error HTTP! status: ${response.status}`);
            }
            return response.json();
        })
        .then(json => {
            console.log(json);
            button.closest('.card-reserve').remove();
        })
        .catch(e => {
            console.log('Hubo un problema realizando la operación: ' + e.message);
        });
    });
});
