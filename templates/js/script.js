$(document).ready(function () {
    var settings = {
        "url": "https://api.coincap.io/v2/assets",
        "method": "GET",
        "data": {limit: 20},
        "Accept-Encoding": "gzip",
        "timeout": 0,
    };

    // Object to store previous data for each coin
    let previousData = {};

    function updateData() {
        $.ajax(settings).done(function (response) {
            const btcPrice = Number(response.data[0].priceUsd).toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:2});
            const ethPrice = Number(response.data[1].priceUsd).toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:2});
            const ltcPrice = Number(response.data[19].priceUsd).toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:2});

            // Set prices for crypto-card
            $('#btc-price').text(btcPrice);
            $('#eth-price').text(ethPrice);
            $('#ltc-price').text(ltcPrice);

            // Loop through the response.data array
            response.data.forEach((coinData, i) => {
                const symbol = coinData.symbol;

                // Check if the coin's data has changed
                if (!previousData[symbol] || hasCoinDataChanged(previousData[symbol], coinData)) {
                    // Update previousData with the new data
                    previousData[symbol] = {
                        rank: coinData.rank,
                        priceUsd: coinData.priceUsd,
                        volumeUsd24Hr: coinData.volumeUsd24Hr,
                        supply: coinData.supply,
                        marketCapUsd: coinData.marketCapUsd
                    };

                    // Check if the row for this coin already exists
                    let tr = $(`tr[data-symbol="${symbol}"]`);
                    const iconUrls = [
                        "https://assets.coincap.io/assets/icons/btc@2x.png",
                        "https://assets.coincap.io/assets/icons/eth@2x.png",
                        "https://assets.coincap.io/assets/icons/usdt@2x.png",
                        "https://assets.coincap.io/assets/icons/bnb@2x.png",
                        "https://assets.coincap.io/assets/icons/sol@2x.png",
                        "https://assets.coincap.io/assets/icons/usdc@2x.png",
                        "https://assets.coincap.io/assets/icons/xrp@2x.png",
                        "https://assets.coincap.io/assets/icons/steth@2x.png",
                        "https://assets.coincap.io/assets/icons/doge@2x.png",
                        "https://assets.coincap.io/assets/icons/trx@2x.png",
                        "https://assets.coincap.io/assets/icons/ada@2x.png",
                        "https://assets.coincap.io/assets/icons/avax@2x.png",
                        "https://assets.coincap.io/assets/icons/wbtc@2x.png",
                        "https://assets.coincap.io/assets/icons/shib@2x.png",
                        "https://assets.coincap.io/assets/icons/bch@2x.png",
                        "https://assets.coincap.io/assets/icons/link@2x.png",
                        "https://assets.coincap.io/assets/icons/dot@2x.png",
                        "https://assets.coincap.io/assets/icons/dai@2x.png",
                        "https://assets.coincap.io/assets/icons/leo@2x.png",
                        "https://assets.coincap.io/assets/icons/ltc@2x.png"
                      ];
                      
                    if (tr.length === 0) {
                        // If the row doesn't exist, create it
                        tr = $('<tr></tr>').addClass('highlight').attr('data-symbol', symbol);
                        $('.coin-list tbody').append(tr);

                        // Create cells for the row
                        tr.append(`<td class="textCenter">${coinData.rank}</td>`);
                        tr.append(`<td class="textLeft">
                            <img src="${iconUrls[i]}" alt=""> 
                            ${coinData.name} <span style="color:gray">${coinData.symbol}</span>
                        </td>`);
                        tr.append(`<td class="price">$${Number(coinData.priceUsd).toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:2})}</td>`);
                        tr.append(`<td class="volumeUsd24Hr">$${Number(coinData.volumeUsd24Hr).toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:2})}</td>`);
                        tr.append(`<td class="supply">$${Number(coinData.supply).toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:2})}</td>`);
                        tr.append(`<td class="marketCapUsd">$${Number(coinData.marketCapUsd).toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:2})}</td>`);
                    } else {
                        // Update existing cells if the row already exists
                        const coinPrice = Number(coinData.priceUsd).toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:2});
                        const innerPrice = tr.find('.price').text().slice(1).toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:2});
                        if (innerPrice < coinPrice) {
                            tr.find('.price').text(`$${coinPrice}`);
                            tr.find('.price').addClass('rise');
                            setTimeout(function() {
                                tr.find('.price').removeClass('rise');
                            }, 2000);
                        } else if (innerPrice > coinPrice) {
                            tr.find('.price').text(`$${coinPrice}`);
                            tr.find('.price').addClass('fall');
                            setTimeout(function() {
                                tr.find('.price').removeClass('fall');
                            }, 2000);
                        } else {
                            tr.find('.price').text(`$${coinPrice}`);
                        }
                        tr.find('.volumeUsd24Hr').text(`$${Number(coinData.volumeUsd24Hr).toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:2})}`);
                        tr.find('.supply').text(`$${Number(coinData.supply).toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:2})}`);
                        tr.find('.marketCapUsd').text(`$${Number(coinData.marketCapUsd).toLocaleString(undefined, {minimumFractionDigits:2, maximumFractionDigits:2})}`);
                    }
                }
            });
        });
    }

    // Function to check if coin data has changed
    function hasCoinDataChanged(oldData, newData) {
        return oldData.rank !== newData.rank ||
            oldData.priceUsd !== newData.priceUsd ||
            oldData.volumeUsd24Hr !== newData.volumeUsd24Hr ||
            oldData.supply !== newData.supply ||
            oldData.marketCapUsd !== newData.marketCapUsd;
    }

    // Run updateData every 5 seconds
    setInterval(updateData, 5000);

    updateData();
});
