(()=>{
const socket = io();

socket.emit('trigger');

const coinName = document.querySelector('#name');
const price = document.querySelector('#price');
const marketCap = document.querySelector('#market-cap');
const dayPercentChange = document.querySelector('#day-percent-change');

const percentChange = () => {
    dayPercentChange.innerText < 0 ? dayPercentChange.className += 'text-danger' : dayPercentChange.className += 'text-success' ;
}

socket.on('update', response => {

    price.innerText = response['quotes']['USD']['price'].toFixed(3);
    marketCap.innerText = new Intl.NumberFormat().format(response['quotes']['USD']['market_cap']);
    dayPercentChange.innerText = response['quotes']['USD']['percent_change_24h'];
    coinName.innerText = response['name'];


    console.log(response['quotes']['USD']['price'])

});

percentChange();


})();

