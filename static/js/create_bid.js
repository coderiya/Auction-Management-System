import helper from "./helper.js";

const photoInput = document.getElementById("photoInput");
const photoPreview = document.getElementById("photoPreview");
const uploadBox = document.getElementById("photoUpload");

photoInput.addEventListener("change", previewPhotos);
uploadBox.addEventListener("dragover", e => e.preventDefault());
uploadBox.addEventListener("drop", e => {
  e.preventDefault();
  const files = Array.from(e.dataTransfer.files);
  handleFiles(files);
});

function previewPhotos() {
  handleFiles(Array.from(this.files));
}

function handleFiles(files) {
  photoPreview.innerHTML = "";
  files.slice(0, 12).forEach(file => {
    const reader = new FileReader();
    reader.onload = e => {
      const img = document.createElement("img");
      img.src = e.target.result;
      photoPreview.appendChild(img);
    };
    reader.readAsDataURL(file);
  });
}

export class Create_bid {
  constructor() {
    this.auth_headers = {
      "USER-ID": localStorage.getItem('USER_ID'),
      "USER-NAME": localStorage.getItem('USER_NAME'),
      'Content-Type': 'application/json'
    }
  }

  async listItem() {
    try {
      const params = {
          "bidName": "Mac Book",
          "bidingStartPrice": 1000,
          "bidDesc": "Mac Book",
          "bidItemCond": "Used - Good",
          "bidItemCatName": "Electronics",
          "bidItemCatCode": "ELECTRONICS",
          "bidStartTime": "2025-12-10T08:00:00",
          "bidEndTime": "2025-12-10T10:00:00",
          "bidShippingCharges": 0,
          "minimumBidAmount": 900,
      }
      // // validation - to be updated
      // // checkMandatoryFields(params)
      const response = await fetch('/bids/', {
        method: 'POST',
        headers: this.auth_headers,
        body: JSON.stringify(params)
      });
      console.log(response)
      const result = response.json();
// const response = {
//   status: 200
// }
// const result = {
//   "message": "Bid Listed Successfully"
// }
      if (response) {
        helper.showNotification(result.message, 'success');
        window.location.href = 'home'
      } else {
        helper.showNotification(result.error, 'error');
      }
    } catch (error) {
      console.log(error);
      helper.showNotification(error, 'error');
    }
  }

  async fetchListofCategory() {
    try {
      const response = await fetch('/list/categories/', {
        method: 'GET',
        headers: this.auth_headers,
      })
      if (response && response.status == 200) {
        helper.showNotification(result.message, 'success');
      } else {
        helper.showNotification(result.error, 'error');
      }
    } catch (error) {
      console.log(error);
      helper.showNotification(error, 'error');
    }
  }
}

function checkMandatoryFields(params) {
  if (!params.bidname) {
    throw "Missing bidname"
  }
  if (!params.bidingStartPrice) {
    throw "Missing bidingStartPrice"
  }
  if (!params.bidDesc) {
    throw "Missing bidDesc"
  }
  if (!params.bidItemCond) {
    throw "Missing bidItemCond"
  }
  if (!params.bidItemCatName) {
    throw "Missing bidItemCatName"
  }
  if (!params.bidItemCode) {
    throw "Missing bidItemCatCode"
  }
  if (!params.bidStartTime) {
    throw "Missing bidStartTime"
  }
  if (!params.bidEndTime) {
    throw "Missing bidEndTime"
  }
  if (!params.bidShippingCharges) {
    throw "Missing bidShippingCharges"
  }
  if (!params.minimumBidAmount) {
    throw "Missing minimumBidAmount"
  }
  return true
}
