let openshopping = document.querySelector('.shopping');
let closeshopping = document.querySelector('.closeshopping');
let list = document.querySelector('.list');
let listcard = document.querySelector('.listcard');
let body = document.querySelector('body');
let total = document.querySelector('.total');
let quantity = document.querySelector('.quantity');
let route=document.querySelector('.dropdown')
openshopping.addEventListener('click', () => {
    body.classList.add('active');
    reduceOpacity(route,0);
});

closeshopping.addEventListener('click', () => {
    body.classList.remove('active');
    reduceOpacity(route,100);
});
// let openShopping = document.querySelector('.shopping');
// let closeShopping = document.querySelector('.closeShopping');
// let list = document.querySelector('.list');
// let listCard = document.querySelector('.listCard');
// let body = document.querySelector('body');
// let total = document.querySelector('.total');
// let quantity = document.querySelector('.quantity');

// openShopping.addEventListener('click', ()=>{
//     body.classList.add('active');
// })
// closeShopping.addEventListener('click', ()=>{
//     body.classList.remove('active');
// })
function reduceOpacity(element, opacity) {

    element.style.opacity = opacity;
    element.style.transitionDuration = '50ms';
  }
let products = [
    {
        id: 1,
        name: 'product 1',
        image: 'OIP (1).jpeg',
        price: 12000
    },
    {
        id: 2,
        name: 'product 2',
        image: 'OIP (2).jpeg',
        price: 12000
    },
    {
        id: 3,
        name: 'product 3',
        image: 'OIP.jpeg',
        price: 12000
    },
    // {
    //     id: 4,
    //     name: 'product 4',
    //     image: 'product-modeling-04.jpg',
    //     price: 12000
    // },
];

let listcards = [];

function initApp() {
    products.forEach((value, key) => {
        let newDiv = document.createElement('div');
        newDiv.classList.add('item');
        newDiv.innerHTML = `
            <img src="${value.image}">
            <div class="title">${value.name}</div>
            <div class="price">${value.price.toLocaleString()}</div>
            <button onclick="addToCard(${key})">Add to cart</button>
        `;
        list.appendChild(newDiv);
    });
}

initApp();
function addToCard(key){
    if(listcards[key] == null){
        // copy product form list to list card
        listcards[key] = JSON.parse(JSON.stringify(products[key]));
        listcards[key].quantity = 1;
    }
    reloadCard();
}
function reloadCard(){
    listcard.innerHTML = '';
    let count = 0;
    let totalPrice = 0;
    listcards.forEach((value, key)=>{
        totalPrice = totalPrice + value.price;
        count = count + value.quantity;
        if(value != null){
            let newDiv = document.createElement('li');
            newDiv.innerHTML = `
                <div><img src="${value.image}"/></div>
                <div>${value.name}</div>
                <div>${value.price.toLocaleString()}</div>
                <div>
                    <button onclick="changeQuantity(${key}, ${value.quantity - 1})">-</button>
                    <div class="count">${value.quantity}</div>
                    <button onclick="changeQuantity(${key}, ${value.quantity + 1})">+</button>
                </div>`;
                listcard.appendChild(newDiv);
        }
    })
    total.innerText = totalPrice.toLocaleString();
    quantity.innerText = count;
}
function changeQuantity(key, quantity){
    if(quantity == 0){
        delete listcards[key];
    }else{
        listcards[key].quantity = quantity;
        listcards[key].price = quantity * products[key].price;
    }
    reloadCard();
}

const dropdowns = document.querySelectorAll('.dropdown');
dropdowns.forEach(dropdown =>{
      const select = dropdown.querySelector('.select');
      const caret=dropdown.querySelector('.caret');
     const menu = dropdown.querySelector('.menu');
     const options=dropdown.querySelectorAll('.menu li');
     const selected = dropdown.querySelector('.selected');

     select.addEventListener('click', ()=>{
         select.classList.toggle('select-clicked');
         caret.classList.toggle('caret-rotate');
        menu.classList.toggle('menu-open');
     })
 options.forEach(option =>{
     option.addEventListener('click', () => {
         selected.innerText = option.innerText;
         select.classList.remove('select-clicked');
         caret.classList.remove('caret-rotate');
         menu.classList.remove('menu-open');
         options.forEach(option =>{
             option.classList.remove('active')
        });
         option.classList.add('active');
       });
    });
});

