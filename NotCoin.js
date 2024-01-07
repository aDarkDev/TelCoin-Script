function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
  
  function sendCoin(count, hash) {
    console.log(`making coins: ${count} with hash ${hash}`);
    const data = {
      count: count,
      webAppData: "ur",
      hash: hash
    };
  
    fetch("https://clicker-api.joincommunity.xyz/clicker/core/click", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        accept: "application/json",
        "Accept-Language": "en,en-US;q=0.9",
        auth: "1",
        Authorization: "Your Authorization",
        Connection: "keep-alive",
        Host: "clicker-api.joincommunity.xyz",
        Origin: "https://clicker.joincommunity.xyz",
        Referer: "https://clicker.joincommunity.xyz/",
        "User-Agent":
          "Mozilla/5.0 (Linux; Android 9; SM-N975F Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/120.0.6099.116 Mobile Safari/537.36",
        "X-Requested-With": "org.telegram.messenger.web"
      },
      body: JSON.stringify(data)
    })
      .then(response => response.json())
      .then(result => {
        console.log(result);
        const hashes = result.data[0].hash;
        const newHash = evaluateHash(hashes);
        console.log("new hash", newHash);
        console.log("lastAvailableCoins", result.data[0].lastAvailableCoins);
        if (result.data[0].lastAvailableCoins < 60) {
          console.log("coins limited. sleeping 120");
          sleep(120000);
        }
      })
      .catch(error => console.error("an error", error));
  }
  
  function evaluateJs(string) {
    if (string === "document.querySelectorAll('body').length") {
      return 1;
    }
    return eval(string);
  }
  
  function base64(data) {
    return Buffer.from(data, "utf-8").toString("base64");
  }
  
  function evaluateHash(hashes) {
    console.log(hashes);
    if (hashes.length === 2) {
      const first = evaluateJs(base64(hashes[0]));
      const second = evaluateJs(base64(hashes[1]));
      return first + second;
    } else {
      return evaluateJs(base64(hashes[0]));
    }
  }
  
  let startHash = 1;
  let coinBoost = 6;
  
  // First call
  let count = coinBoost;
  sendCoin(count, startHash);
  
  // Subsequent calls
  while (true) {
    count = (Math.floor(Math.random() * (1000 - 400 + 1)) + 400) / coinBoost * coinBoost;
    sendCoin(count, startHash);
    sleep(2000);
  }