import helper from "./helper.js";

export class All_Listings {

    constructor() {
        this.auth_headers = {
            "USER-ID": localStorage.getItem('USER_ID'),
            "USER-NAME": localStorage.getItem('USER_NAME'),
            'Content-Type': 'application/json'
        };

        // GLOBAL STATE
        this.currentPage = 1;
        this.totalRecords = 0;
        this.limit = 10;
        this.sort = [{ key: "BID_START_TIME", value: '-1' }];
            this.currentCategory = "";
        this.currentSearch = "";
        this.skip = 0;
    }

    async loadCategories() {
        try {
            const res = await fetch("/api/list/categories", {
                method: 'GET',
                headers: this.auth_headers
            });

            const data = await res.json();

            const categoryFilter = document.getElementById("categoryFilter");
            categoryFilter.innerHTML = `<option value="">All Categories</option>`;

            data.data.forEach(cat => {
                const opt = document.createElement("option");
                opt.value = cat.LABEL_CODE;
                opt.textContent = cat.LABEL_NAME;
                categoryFilter.appendChild(opt);
            });
        } catch (error) {
            helper.showNotification("Failed to load categories", "error");
        }
    }

    async loadListings() {
        try {
            const searchText = document.getElementById("searchBox")?.value;
            const selectedCategory = document.getElementById("categoryFilter")?.value;
            let body = {
                "skip": this.skip,
                "limit": this.limit,
                "sort": this.sort,
                "search": '',
                "filter": {}
            }
            if (selectedCategory && selectedCategory !== "") {
                body['filter']['BID_ITEM_CATEGORY_CODE'] = selectedCategory
            }
            if (searchText) {
                body['search'] = searchText
            }
            const res = await fetch('api/list/wishlist', {
                method: "POST",
                headers: this.auth_headers,
                body: JSON.stringify(body)
            });

            const response = await res.json();
            // correct API structure
            const records = response.result.data || [];
            this.totalRecords = response.result.total || 0;

            this.renderListings(records);
            this.updatePagination();
        } catch (error) {
            helper.showNotification("Failed to load listings", "error");
        }
    }

    async loadRecentlyQuotedBids(){
        try {
            const searchText = document.getElementById("searchBox")?.value;
            const selectedCategory = document.getElementById("categoryFilter")?.value;
            let payload = {
                sort: this.sort,
                limit: this.limit,
                skip: this.skip,
                currentPage: this.currentPage,
                search: '',
                filter: {}
            }
            if (selectedCategory && selectedCategory !== "") {
                payload['filter']['BID_ITEM_CATEGORY_CODE'] = selectedCategory
            }
            if (searchText) {
                payload['search'] = searchText
            }
            const res = await fetch("/api/list/user/quotes", {
                method: 'POST',
                headers: this.auth_headers,
                body: JSON.stringify(payload)
            })
            const result = await res.json();
            this.totalRecords = result.result.total || 0;
            this.renderListings(result.result.data);
            this.updatePagination();
            document.getElementById("pageNumber").textContent = this.currentPage
        } catch (error) {
            console.log('error: ', error);
        }
    }

    async loadRecentBidListings() {
        try {
            const searchText = document.getElementById("searchBox")?.value;
            const selectedCategory = document.getElementById("categoryFilter")?.value;
            let payload = {
                sort: this.sort,
                limit: this.limit,
                skip: this.skip,
                currentPage: this.currentPage,
                search: '',
                filter: {}
            }
            if (selectedCategory) {
                payload['filter']['BID_ITEM_CATEGORY_CODE'] = selectedCategory
            }
            if (searchText) {
                payload['search'] = searchText
            }
            const res = await fetch("/api/list/listings", {
                method: 'POST',
                headers: this.auth_headers,
                body: JSON.stringify(payload)
            })
            const result = await res.json();
            this.totalRecords = result.result.total || 0;
            this.renderListings(result.result.data);
            this.updatePagination();
            document.getElementById("pageNumber").textContent = this.currentPage
        } catch (error) {
            console.log('error: ', error);
        }
    }

    renderListings(records) {
        const container = document.getElementById("itemsContainer");
        container.innerHTML = "";

        records.forEach(item => {
            const row = document.createElement("div");
            row.classList.add("listing-row");

            // <img src="${item.image_url}" class="listing-img" alt="Item">
            row.innerHTML = `

            <div class="listing-content">
                <p class="listing-title">${item.BID_NAME}</p>
                <p class="listing-meta">Description: ${item.BID_DESC}</p>

                <p class="listing-meta">
                    <strong>Category:</strong> ${item.BID_ITEM_CATEGORY_NAME} <br>
                    <!-- <strong>Seller:</strong> ${item.seller_info?.seller_name || "N/A"} -->
                    <strong>Seller Name:</strong> ${item.SELLER_NAME} <br>
                    <strong>Status:</strong> ${item.STATUS}
                </p>

                <p class="listing-status">
                    <strong>Start Price:</strong> $${item.BID_START_PRICE} <br>
                    <strong>Current Bid:</strong> $${item.BID_ONGOING_PRICE} <br>
                    <strong>Minimum Bid Amount:</strong> $${item.MINIMUM_BID_AMOUNT} <br>
                </p>

                <p class="listing-meta">
                    <strong>Start Time:</strong> ${item.BID_START_TIME}
                </p>
                <p class="listing-meta">
                    <strong>End Time:</strong> ${item.BID_END_TIME}
                </p>
            </div>
        `;

            container.appendChild(row);
        });
    }

    updatePagination() {
        const pageNumber = document.getElementById("pageNumber");
        const prevBtn = document.getElementById("prevButton");
        const nextBtn = document.getElementById("nextButton");

        pageNumber.textContent = this.currentPage;

        const totalPages = Math.ceil(this.totalRecords / this.limit);
        // <-- Disable Previous on first page
        prevBtn.disabled = (this.currentPage <= 1);

        // Disable Next when:
        // 1. totalRecords <= 10 OR
        // 2. we are on the last page
        if (this.totalRecords <= this.limit || this.currentPage >= totalPages) {
            nextBtn.disabled = true;
        } else {
            nextBtn.disabled = false;
        }
    }
}
