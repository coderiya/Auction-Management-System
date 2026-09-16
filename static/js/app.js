// user register

// import helper from "./helper";

import helper from "./helper.js";

export class Home {

  constructor() {
    this.auth_headers = {
      "USER-ID": localStorage.getItem('USER_ID'),
      "USER-NAME": localStorage.getItem('USER_NAME'),
      'Content-Type': 'application/json'
    };
  }

  //  Fetch dashboard stats
  // load count of active bid, purchase history, watching (= active bids in wishlist of the logged in user)
  async loadStats() {
    try {
      const response = await fetch("/api/list/stats", {
        method: 'GET',
        headers: this.auth_headers
      });
      const result = await response.json();

      const stats = result.data[0];

      const activeBidsStats = document.getElementById("activeBids")
      activeBidsStats.textContent = stats.activeBids;
      document.getElementById("purchaseHistory").textContent = stats.purchaseHistory || 0;
      // document.getElementById("bidsInProgress").textContent = stats.bidsInProgress;
      document.getElementById("watching").textContent = stats.watchlist;
      console.log('------end-------')
    } catch (error) {
      console.log(error)
      helper.showNotification("Failed to load statistics for logged in User", "error")
    }
  }

  // Fetch categories
  async loadCat() {
    try {
      console.log('Fetching categories...');
      const response = await fetch("api/list/categories", {
        method: 'GET',
        headers: this.auth_headers
      });
      // const response = await fetch("http://127.0.0.1:8080/api/list/categories");
      const result = await response.json();

      // The array is inside result.data
      const categories = result.data;
      console.log(categories)

      // Find container where you want to insert cards
      const container = document.getElementById("category-panel");

      container.innerHTML = ""; // Clear previous

      // Loop and create blocks
      categories.forEach(cat => {
        const card = document.createElement("div");
        card.className = "category-card";

        // Convert label to lowercase and remove spaces for file naming consistency
        const imgName = cat.LABEL_CODE.toLowerCase().replace(/\s+/g, '_');
        console.log(imgName)
        // const imgPath = `/static/public/${imgName}.png`;
        const imgPath = `./../static/public/${imgName}.png`
        console.log(imgPath)

        card.innerHTML = `
          <!-- <img src="${imgPath}" alt="${cat.LABEL_CODE}" class="emoji-img" onerror="this.src='static/public'"> -->
          <h4>${cat.LABEL_NAME}</h4>
          <p>${cat.ITEM_COUNT} items</p>
        `;
        card.onclick = () => {
          const url = `/viewRecentBids?category=${cat.LABEL_CODE}&name=${encodeURIComponent(cat.LABEL_NAME)}`;
          console.log("Redirect URL:", url);
          window.location.href = url;
        };
        container.appendChild(card);
      });


      // Optional: handle block sizing or scroll
      adjustLayout(categories.length);

    } catch (err) {
      console.error("Error loading categories:", err);
    }
  }

  //  Fetch recently placed auctions
  async loadRecentAuctions() {
    try {
      const res = await fetch("api/list/listings", {
        method: 'POST',
        headers: this.auth_headers,
        body: JSON.stringify({})
      });
      // const res = await fetch("http://127.0.0.1:8080/api/list/listings");
      const result = await res.json();
      const auctions = result.result.data;

      const container = document.getElementById("auction-panel");
      container.innerHTML = "";

      auctions.forEach(a => {
        const card = document.createElement("div");
        card.className = "auction-card";
        if (a.STATUS == 'ON_GOING') { }
        if (a.STATUS == 'NOT_STARTED') { }
        const diffMilliseconds = Math.abs(new Date(a.BID_END_TIME).getTime() - (new Date()).getTime())

        const secondsInMinute = 60;
        const minutesInHour = 60;
        const hoursInDay = 24;
        const millisecondsInSecond = 1000;

        let totalSeconds = Math.floor(diffMilliseconds / millisecondsInSecond);

        const days = Math.floor(totalSeconds / (secondsInMinute * minutesInHour * hoursInDay));
        totalSeconds -= days * (secondsInMinute * minutesInHour * hoursInDay);

        const hours = Math.floor(totalSeconds / (secondsInMinute * minutesInHour));
        totalSeconds -= hours * (secondsInMinute * minutesInHour);

        const minutes = Math.floor(totalSeconds / secondsInMinute);
        const seconds = totalSeconds % secondsInMinute;

        // <p class="auction-bids">${a.NUM_OF_BIDS} bids</p>
        card.innerHTML = `
          <div class="auction-top">
            <div class="auction-title">${a.BID_NAME}</div>
            ${a.tag ? `<span class="auction-tag">${a.tag}</span>` : ""}
          </div>

          <div class="auction-body">
            <p class="auction-desc">${a.BID_DESC}</p>
            <p class="auction-price">$${parseFloat(a.BID_ONGOING_PRICE).toLocaleString()}</p>
            <p class="auction-time">${days} days, ${hours} hours, ${minutes} minutes, ${seconds} seconds</p>

            <button class="bid-btn" onclick="goToBid('${a.BID_ID}')">
              Place Bid
            </button>
          </div>
        `;

        container.appendChild(card);
      });

    } catch (err) {
      console.error("Error loading auctions:", err);
    }
  }
}




function adjustLayout(count) {
  const container = document.getElementById("category-panel");

  if (count <= 4) {
    container.style.justifyContent = 'space-evenly';
    for (let card of container.children) {
      card.style.flex = '1 1 20%';
    }
  } else {
    container.style.overflowX = 'auto';
    for (let card of container.children) {
      card.style.flex = '0 0 180px';
    }
  }
}

export function goToBid(bidId) {
  console.log("Navigating to bid page:", bidId);
  window.location.href = `/bid/${bidId}`;
}

window.goToBid = goToBid;

