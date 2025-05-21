var updateBtns = document.getElementsByClassName('update-cart');

for (let i = 0; i < updateBtns.length; i++) {
	updateBtns[i].addEventListener('click', function () {
		var productId = this.dataset.product;
		var action = this.dataset.action;

		// Lấy số lượng nếu có (ví dụ từ modal)
		var quantity = this.dataset.qty ? parseInt(this.dataset.qty) : 1;

		console.log('productId:', productId, 'Action:', action, 'Qty:', quantity);
		console.log('USER:', user);

		if (user == 'AnonymousUser') {
			console.log('User is not authenticated');
		} else {
			updateUserOrder(productId, action, quantity);
		}
	});
}

function updateUserOrder(productId, action, quantity = 1) {
	console.log('User is authenticated, sending data...');

	var url = '/update_item/';

	fetch(url, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			'X-CSRFToken': csrftoken,
		},
		body: JSON.stringify({
			'productId': productId,
			'action': action,
			'quantity': quantity,
		}),
	})
		.then((response) => response.json())
		.then((data) => {
			location.reload();
		});
}



// var updateBtns = document.getElementsByClassName('update-cart')

// for (i = 0; i < updateBtns.length; i++) {
// 	updateBtns[i].addEventListener('click', function(){
// 		var productId = this.dataset.product
// 		var action = this.dataset.action
// 		console.log('productId:', productId, 'Action:', action)

//         console.log('USER:', user)
//         if (user == 'AnonymousUser'){
//             console.log('User is not authenticated')
//         } else {
//             updateUserOrder(productId, action)}
// 	})
// }

// function updateUserOrder(productId, action){
//     console.log('User is authenticated, sending data...')

//         var url = '/update_item/'

//         fetch(url, {
//             method:'POST',
//             headers:{
//                 'Content-Type':'application/json',
//                 'X-CSRFToken':csrftoken,
//             }, 
//             body:JSON.stringify({'productId':productId, 'action':action})
//         })
//         .then((response) => {
//         return response.json();
//         })
//         .then((data) => {
//             location.reload()
//         });
// }

