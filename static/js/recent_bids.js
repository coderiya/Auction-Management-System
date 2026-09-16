/* ==================== GLOBAL STATE ==================== */
let currentPage = 1;
let sortOrder = 1; // 1 = ascending, -1 = descending
const scrollWrapper = document.getElementById("scrollWrapper");

export class RecentBids {
  constructor() {
    this.auth_headers = {
      "USER-ID": localStorage.getItem('USER_ID'),
      "USER-NAME": localStorage.getItem('USER_NAME'),
      'Content-Type': 'application/json'
    }
  }
  /* ==================== FETCH DATA ==================== */
  async fetchListings() {
    const searchText = document.getElementById("searchBox").value;
    const selectedCategory = document.getElementById("categoryFilter").value;

    const payload = {
      selected_category: selectedCategory,     // "" = all categories
      search_details: { text: searchText },    // search query
      sort_preferences: [{ column: "BID_START_TIME", order: sortOrder }],
      records_per_page: 6,
      current_page: currentPage
    };

    try {
      const response = await fetch("/listings", {
        method: 'POST',
        headers: this.auth_headers,
        body: JSON.stringify(payload)
      })

      const result = await response.json();
      renderListings(result.records);
      document.getElementById("pageNumber").textContent = currentPage;
    } catch (err) {
      console.error("Error fetching listings:", err);
    }
  }
}

/* ==================== RENDER CARDS ==================== */
function renderListings(items) {
  const container = document.getElementById("itemsContainer");
  container.innerHTML = "";

  if (!items || items.length === 0) {
    container.innerHTML = "<p>No results found.</p>";
    return;
  }

  items.forEach(item => {
    const card = document.createElement("div");
    card.classList.add("listing-card");

    card.innerHTML = `
      <h3>${item.BID_NAME || "Unnamed Item"}</h3>
      <p>${item.BID_DESC || "No description available."}</p>
      <p><strong>Category:</strong> ${item.BID_ITEM_CATEGORY}</p>
      <p><strong>Ongoing Price:</strong> $${item.BID_ONGOING_PRICE}</p>
      <p><strong>Start Time:</strong> ${item.BID_START_TIME}</p>
    `;

    container.appendChild(card);
  });
}

/* ==================== EVENT HANDLERS ==================== */
// Search input
document.getElementById("searchBox").addEventListener("input", () => {
  currentPage = 1;
  fetchListings();
});

// Category dropdown
document.getElementById("categoryFilter").addEventListener("change", () => {
  currentPage = 1;
  fetchListings();
});

// Sort button
document.getElementById("sortButton").addEventListener("click", () => {
  sortOrder *= -1;
  document.getElementById("sortButton").textContent =
    sortOrder === 1 ? "Sort by Start Time ⬆️" : "Sort by Start Time ⬇️";
  fetchListings();
});

// Pagination
document.getElementById("prevButton").addEventListener("click", () => {
  if (currentPage > 1) {
    currentPage--;
    fetchListings();
  }
});
document.getElementById("nextButton").addEventListener("click", () => {
  currentPage++;
  fetchListings();
});

// Horizontal scroll buttons
document.getElementById("scrollLeft").addEventListener("click", () => {
  scrollWrapper.scrollBy({ left: -300, behavior: "smooth" });
});
document.getElementById("scrollRight").addEventListener("click", () => {
  scrollWrapper.scrollBy({ left: 300, behavior: "smooth" });
});

/* ==================== INITIAL LOAD ==================== */
fetchListings();
