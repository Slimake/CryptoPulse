document.addEventListener("DOMContentLoaded", function () {
    // Fetch cryptocurrency prices (dummy data for example)
    const btcPrice = 45000;
    const ethPrice = 3000;
    const ltcPrice = 150;

    document.getElementById('btc-price').textContent = btcPrice.toLocaleString();
    document.getElementById('eth-price').textContent = ethPrice.toLocaleString();
    document.getElementById('ltc-price').textContent = ltcPrice.toLocaleString();
});

function subscribe() {
    alert("Thank you for subscribing to CryptoPulse!");
}

