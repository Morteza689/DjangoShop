function sendProductComment(productId) {
    var comment = $('#commentText').val();
    var isSuggested = $('#is_suggested')[0].checked

    if (comment.length < 10) {


        Swal.fire({
                title: 'اعلان',
                text: 'متن شما خیلی کم است',
                icon:'error' ,
                showCancelButton: false,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'باشه'
            })



    } else {
        $.get('/products/add-product-comment', {
            product_comment: comment,
            product_id: productId,
            is_suggested: isSuggested
        }).then(res => {
            $('#comments_area').html(res)
            $('#commentText').val('');
            $('#parent_id').val('');
            document.getElementById('comments_area').scrollIntoView({behavior: "smooth"});
        })
    }
}


function filterProduct() {
    const start_price = $('#skip-value-lower').val().replace(',', '');
    const end_price = $('#skip-value-upper').val().replace(',', '');
    $('#start_price').val(start_price);
    $('#end_price').val(end_price);
    $('#search_product_box').val()
    $('#filter_form').submit();
}
function productS(){
    $('#search_product_box').val()
    $('#search_form').submit();
}



function fillPage(page) {
    $('#page').val(page)
    $('#filter_form').submit();
}

function addProductToOrder2(productId) {
    const productConut = 1
    $.get('/order/add-to-order/', {
        product_id: productId,
        count: productConut,
    }).then(res => {
        if (res.status === 'not_auth') {
            Swal.fire({
                title: 'اعلان',
                text: res.text,
                icon: res.icon,
                showCancelButton: false,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: res.confirm_button_text
            }).then((result) => {
                if (result.isConfirmed) {
                    window.location.href = '/login'
                }
            })
        }
    })
}


function addProductToOrder(productId) {
    const productConut = $('#product_count').val();
    $.get('/order/add-to-order/', {
        product_id: productId,
        count: productConut,
    }).then(res => {
        Swal.fire({
            title: 'اعلان',
            text: res.text,
            icon: res.icon,
            showCancelButton: false,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: res.confirm_button_text
        }).then((result) => {
            if (result.isConfirmed && res.status === 'not_auth') {
                window.location.href = '/login'
            }
        })
    })
}


function removeOrderDetail(detailId) {
    $.get('/user/remove-order-detail/', {
        'detail_id': detailId
    }).then(res => {
        if (res.status === 'success') {
            $('#order-detail-content').html(res.body)
            Swal.fire({
                title: 'اعلان',
                text: 'با موفقیت حذف شد',
                icon: 'success',
                showCancelButton: false,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'ممنون'
            })
        }
    })
}


function changeOrderDetailCount(detailId, state) {
    console.log(detailId, state)
    $.get('/user/change-order-detail/', {
        'detail_id': detailId,
        'state': state
    }).then(res => {
        $('#order-detail-content').html(res.body)
        if (res.count = 0) {
            $('#order-detail-content').html(res.body)
        }
    })
}

function getAddressId() {
    const addressId = document.querySelector('input[name="customRadio"]:checked').dataset.customRadioId
    $.get('/user/get-address-id/', {
        'address_id': addressId,
    })
}


let kosSubmit = false;
function kos(e){
    if(kosSubmit) e.preventDefault();
    kosSubmit = true;
}

