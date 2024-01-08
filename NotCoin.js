const axios = require('axios');

const coinBoost = 6;

async function sendCoin(count, hash, turbo = false) {
    console.log(`making coins: ${count} with hash ${hash}`);
    const data = {
        count: count,
        webAppData: "Your WebApp Data",
        hash: hash
    };

    if (turbo) {
        data.turbo = true;
    }

    const headers = {
        accept: "application/json",
        "Accept-Language": "en,en-US;q=0.9",
        auth: "1",
        Authorization: "Your Authorization",
        Connection: "keep-alive",
        "Content-Length": JSON.stringify(data).length,
        Host: "clicker-api.joincommunity.xyz",
        Origin: "https://clicker.joincommunity.xyz",
        Referer: "https://clicker.joincommunity.xyz/",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; SM-N975F Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.6099.116 Mobile Safari/537.36",
        "X-Requested-With": "org.telegram.messenger.web",
    };

    try {
        const response = await axios.post("https://clicker-api.joincommunity.xyz/clicker/core/click", JSON.stringify(data), { headers });
        return response.data;
    } catch (error) {
        console.error(error);
    }
}

function evaluateJs(string) {
    if (string === "document.querySelectorAll('body').length") {
        return 1;
    }

    return Number(eval(string));
}

function base64decode(data) {
    const buff = Buffer.from(data, 'base64');
    return buff.toString('utf-8');
}

function evaluateHash(hashes) {
    if (hashes.length === 2) {
        const first = evaluateJs(base64decode(hashes[0]));
        const second = evaluateJs(base64decode(hashes[1]));
        return first + second;
    } else {
        return evaluateJs(base64decode(hashes[0]));
    }
}

let startHash = 1;

async function main() {
    try {
        let count = coinBoost;
        const sendResult = await sendCoin(count, startHash);
        const hashes = sendResult.data[0].hash;
        startHash = evaluateHash(hashes);
        console.log(`started_hash ${startHash}`);
        console.log(`lastAvailableCoins ${sendResult.data[0].lastAvailableCoins}`);
        
        if (sendResult.data[0].lastAvailableCoins < 60) {
            console.log("coins limited. sleeping 120");
            await sleep(120000);
        }

        await sleep(2000);
    } catch(error) {
        console.error(error);
    }

    while (true) {
        try {
            let count = (Math.floor(Math.random() * (1000 - 400 + 1)) + 400) / coinBoost * coinBoost;
            const sendResult = await sendCoin(count, startHash, false);
            const hashes = sendResult.data[0].hash;
            startHash = evaluateHash(hashes);
            console.log(`started_hash ${startHash}`);
            console.log(`lastAvailableCoins ${sendResult.data[0].lastAvailableCoins}`);
            
            if (sendResult.data[0].lastAvailableCoins < 60) {
                console.log("coins limited. sleeping 120");
                await sleep(120000);
            }

            await sleep(2000);
        } catch (error) {
            console.error(error);
        }
    }
}

function sleep(ms) {
    return new Promise((resolve) => {
        setTimeout(resolve, ms);
    });
}

// start the program
main();
