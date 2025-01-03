$(document).ready(function () {
    // Run updateData every 5 seconds
    setInterval(updateData, 5000);
    updateData();
});

function updateData() {
    // coincap API
    var settings = {
        "url": "https://api.coincap.io/v2/assets",
        "method": "GET",
        "data": {limit: 100},
        "Accept-Encoding": "gzip",
        "timeout": 0,
    };

    // Object to store previous data for each coin
    let previousData = {};

    $.ajax(settings).done(function (response) {
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
      
                if (tr.length === 0) {
                    // If the row doesn't exist, create it
                    tr = $('<tr></tr>').addClass('highlight').attr('data-symbol', symbol);
                    $('.coin-list tbody').append(tr);

                    // Create cells for the row
                    tr.append(`<td class="textCenter">${coinData.rank}</td>`);
                    tr.append(`<td class="textLeft">
                        <img src="${iconUrls[coinData.symbol]}" alt=""> 
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

const iconUrls = {
    "BTC": "https://assets.coincap.io/assets/icons/btc@2x.png",
    "ETH": "https://assets.coincap.io/assets/icons/eth@2x.png",
    "USDT": "https://assets.coincap.io/assets/icons/usdt@2x.png",
    "BNB": "https://assets.coincap.io/assets/icons/bnb@2x.png",
    "SOL": "https://assets.coincap.io/assets/icons/sol@2x.png",
    "USDC": "https://assets.coincap.io/assets/icons/usdc@2x.png",
    "XRP": "https://assets.coincap.io/assets/icons/xrp@2x.png",
    "STETH": "https://assets.coincap.io/assets/icons/steth@2x.png",
    "DOGE": "https://assets.coincap.io/assets/icons/doge@2x.png",
    "TRX": "https://assets.coincap.io/assets/icons/trx@2x.png",
    "ADA": "https://assets.coincap.io/assets/icons/ada@2x.png",
    "AVAX": "https://assets.coincap.io/assets/icons/avax@2x.png",
    "WBTC": "https://assets.coincap.io/assets/icons/wbtc@2x.png",
    "SHIB": "https://assets.coincap.io/assets/icons/shib@2x.png",
    "BCH": "https://assets.coincap.io/assets/icons/bch@2x.png",
    "LINK": "https://assets.coincap.io/assets/icons/link@2x.png",
    "DOT": "https://assets.coincap.io/assets/icons/dot@2x.png",
    "DAI": "https://assets.coincap.io/assets/icons/dai@2x.png",
    "LEO": "https://assets.coincap.io/assets/icons/leo@2x.png",
    "LTC": "https://assets.coincap.io/assets/icons/ltc@2x.png",
    "NEAR": "https://assets.coincap.io/assets/icons/near@2x.png",
    "ICP": "https://assets.coincap.io/assets/icons/icp@2x.png",
    "FET": "https://assets.coincap.io/assets/icons/fet@2x.png",
    "UNI": "https://assets.coincap.io/assets/icons/uni@2x.png",
    "XMR": "https://assets.coincap.io/assets/icons/xmr@2x.png",
    "STX": "https://assets.coincap.io/assets/icons/stx@2x.png",
    "ETC": "https://assets.coincap.io/assets/icons/etc@2x.png",
    "XLM": "https://assets.coincap.io/assets/icons/xlm@2x.png",
    "AAVE": "https://assets.coincap.io/assets/icons/aave@2x.png",
    "OKB": "https://assets.coincap.io/assets/icons/okb@2x.png",
    "FIL": "https://assets.coincap.io/assets/icons/fil@2x.png",
    "CRO": "https://assets.coincap.io/assets/icons/cro@2x.png",
    "VET": "https://assets.coincap.io/assets/icons/vet@2x.png",
    "FTM": "https://assets.coincap.io/assets/icons/ftm@2x.png",
    "GRT": "https://assets.coincap.io/assets/icons/grt@2x.png",
    "RUNE": "https://assets.coincap.io/assets/icons/rune@2x.png",
    "INJ": "https://assets.coincap.io/assets/icons/inj@2x.png",
    "AR": "https://assets.coincap.io/assets/icons/ar@2x.png",
    "THETA": "https://assets.coincap.io/assets/icons/theta@2x.png",
    "MKR": "https://assets.coincap.io/assets/icons/mkr@2x.png",
    "HNT": "https://assets.coincap.io/assets/icons/hnt@2x.png",
    "ATOM": "https://assets.coincap.io/assets/icons/atom@2x.png",
    "ALGO": "https://assets.coincap.io/assets/icons/algo@2x.png",
    "MATIC": "https://assets.coincap.io/assets/icons/matic@2x.png",
    "LDO": "https://assets.coincap.io/assets/icons/ldo@2x.png",
    "BSV": "https://assets.coincap.io/assets/icons/bsv@2x.png",
    "QNT": "https://assets.coincap.io/assets/icons/qnt@2x.png",
    "KCS": "https://assets.coincap.io/assets/icons/kcs@2x.png",
    "FLOW": "https://assets.coincap.io/assets/icons/flow@2x.png",
    "HBAR": "https://assets.coincap.io/assets/icons/hbar@2x.png",
    "GT": "https://assets.coincap.io/assets/icons/gt@2x.png",
    "EOS": "https://assets.coincap.io/assets/icons/eos@2x.png",
    "AXS": "https://assets.coincap.io/assets/icons/axs@2x.png",
    "GALA": "https://assets.coincap.io/assets/icons/gala@2x.png",
    "CKB": "https://assets.coincap.io/assets/icons/ckb@2x.png",
    "NEO": "https://assets.coincap.io/assets/icons/neo@2x.png",
    "XTZ": "https://assets.coincap.io/assets/icons/xtz@2x.png",
    "AKT": "https://assets.coincap.io/assets/icons/akt@2x.png",
    "CFX": "https://assets.coincap.io/assets/icons/cfx@2x.png",
    "EGLD": "https://assets.coincap.io/assets/icons/egld@2x.png",
    "XEC": "https://assets.coincap.io/assets/icons/xec@2x.png",
    "PENDLE": "https://assets.coincap.io/assets/icons/pendle@2x.png",
    "SAND": "https://assets.coincap.io/assets/icons/sand@2x.png",
    "MINA": "https://assets.coincap.io/assets/icons/mina@2x.png",
    "MANA": "https://assets.coincap.io/assets/icons/mana@2x.png",
    "CHZ": "https://assets.coincap.io/assets/icons/chz@2x.png",
    "NEXO": "https://assets.coincap.io/assets/icons/nexo@2x.png",
    "OM": "https://assets.coincap.io/assets/icons/om@2x.png",
    "AIOZ": "https://assets.coincap.io/assets/icons/aioz@2x.png",
    "CAKE": "https://assets.coincap.io/assets/icons/cake@2x.png",
    "ROSE": "https://assets.coincap.io/assets/icons/rose@2x.png",
    "KLAY": "https://assets.coincap.io/assets/icons/klay@2x.png",
    "SUPER": "https://assets.coincap.io/assets/icons/super@2x.png",
    "LPT": "https://assets.coincap.io/assets/icons/lpt@2x.png",
    "DEXE": "https://assets.coincap.io/assets/icons/dexe@2x.png",
    "TUSD": "https://assets.coincap.io/assets/icons/tusd@2x.png",
    "IOTA": "https://assets.coincap.io/assets/icons/miota@2x.png",
    "ZEC": "https://assets.coincap.io/assets/icons/zec@2x.png",
    "FTT": "https://assets.coincap.io/assets/icons/ftt@2x.png",
    "TFUEL": "https://assets.coincap.io/assets/icons/tfuel@2x.png",
    "COMP": "https://assets.coincap.io/assets/icons/comp@2x.png",
    "IOTX": "https://assets.coincap.io/assets/icons/iotx@2x.png",
    "GNO": "https://assets.coincap.io/assets/icons/gno@2x.png",
    "KAVA": "https://assets.coincap.io/assets/icons/kava@2x.png",
    "RAY": "https://assets.coincap.io/assets/icons/ray@2x.png",
    "FEI": "https://assets.coincap.io/assets/icons/fei@2x.png",
    "SNX": "https://assets.coincap.io/assets/icons/snx@2x.png",
    "NXM": "https://assets.coincap.io/assets/icons/nxm@2x.png",
    "1INCH": "https://assets.coincap.io/assets/icons/1inch@2x.png",
    "TWT": "https://assets.coincap.io/assets/icons/twt@2x.png",
    "CELO": "https://assets.coincap.io/assets/icons/celo@2x.png",
    "CRV": "https://assets.coincap.io/assets/icons/crv@2x.png",
    "RSR": "https://assets.coincap.io/assets/icons/rsr@2x.png",
    "WOO": "https://assets.coincap.io/assets/icons/woo@2x.png",
    "XDC": "https://assets.coincap.io/assets/icons/xdc@2x.png",
    "KSM": "https://assets.coincap.io/assets/icons/ksm@2x.png",
    "AMP": "https://assets.coincap.io/assets/icons/amp@2x.png",
    "GLM": "https://assets.coincap.io/assets/icons/glm@2x.png",
    "HOT": "https://assets.coincap.io/assets/icons/hot@2x.png",
    "DASH": "https://assets.coincap.io/assets/icons/dash@2x.png",
    "ZRX": "https://assets.coincap.io/assets/icons/zrx@2x.png",
    "ANKR": "https://assets.coincap.io/assets/icons/ankr@2x.png",
    "ZIL": "https://assets.coincap.io/assets/icons/zil@2x.png",
    "BAT": "https://assets.coincap.io/assets/icons/bat@2x.png",
    "ELF": "https://assets.coincap.io/assets/icons/elf@2x.png",
    "JST": "https://assets.coincap.io/assets/icons/jst@2x.png",
    "SC": "https://assets.coincap.io/assets/icons/sc@2x.png",
    "ANT": "https://assets.coincap.io/assets/icons/ant@2x.png",
    "ENJ": "https://assets.coincap.io/assets/icons/enj@2x.png",
    "QTUM": "https://assets.coincap.io/assets/icons/qtum@2x.png"
};
