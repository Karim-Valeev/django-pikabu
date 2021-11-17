$( document ).ready(function() {
    console.log( "ready!" );
    $('.delete-basket-button').click(function () {
        let $basket = $($(this).closest('span').closest('li'));
        let id = $basket.attr('data-id');
        let name = $basket.attr('data-name');
        let isFavourite = $basket.attr('data-is-favourite');
        let csrfToken = $('[name="csrfmiddlewaretoken"]').attr('value');
        if(isFavourite === 'True'){
            let message = 'Are you sure you want to delete your favourite basket ' + name + '?';
            let flag = window.confirm(message)
            if (flag) {
                deleteBasket($basket, id, csrfToken)
            }
        } else {
            deleteBasket($basket, id, csrfToken)
        }
    })
});

function deleteBasket($basket, id, csrfToken) {
    $.ajax({
        type: "DELETE",
        url: "http://127.0.0.1:8000/api/baskets/" + id,
        contentType: "application/json",
        dataType:'json',
        beforeSend: function (xhr) {
            xhr.setRequestHeader('X-CSRFToken', csrfToken);
        },
        success: function () {
            $basket.fadeOut('slow');
            console.log("Basket deleted")
        },
        error: function (msg) {
            console.log(msg);
        }
    });
}

