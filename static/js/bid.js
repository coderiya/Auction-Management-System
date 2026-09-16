
export class BidDetails {
    constructor() {
        this.auth_headers = {
            "USER-ID": localStorage.getItem('USER_ID'),
            "USER-NAME": localStorage.getItem('USER_NAME'),
            'Content-Type': 'application/json'
        }
    }

    async fetchBid() { }

    async loadBidDetails() {
        try {
            const bid_id = document.body.getAttribute("data-bidid");
            const url = `/bids/${bid_id}`;
            const res = await fetch(url, {
                method: 'GET',
                headers: this.auth_headers
            });

            const result = await res.json();
            const data = result.data;

            const bidId = document.body.getAttribute("data-bidid");
            console.log("Loaded Bid ID:", bidId);

            document.getElementById("bidName").textContent = data.BID_NAME;
            document.getElementById("currentPrice").textContent = data.BID_ONGOING_PRICE;
            document.getElementById("bidCat").textContent = data.BID_ITEM_CAT_NAME;
            document.getElementById("timeLeft").textContent = data.BID_END_TIME;

        } catch (err) {
            console.error("Error loading bid:", err);
        }
    }

    async subDet(){
        try{
            const bidId = document.body.getAttribute("data-bidid");
            const amount = document.getElementById("bidAmount").value.trim();

            const payload = {
                bid_id: bidId,
                bid_amount: amount
            };
            const url = `/bids/quote/${bidId}`;
            const response = await fetch(url, {
                method: 'POST',
                headers: this.auth_headers,
                body: JSON.stringify(payload)
            });
            const result = await response.json();
            const userDetails = result.data;
            // window.location.href = 'home'
        } catch(error){
            console.log(error)
        }
    }
}
