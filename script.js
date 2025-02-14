async function uploadFile() {
  const fileInput = document.getElementById("file-upload");
  const file = fileInput.files[0];

  if (!file) {
    alert("Please select a file to upload.");
    return;
  }

  // Get the min confidence value from the slider
  const minConfidence = document.getElementById("min-confidence").value / 100;

  const formData = new FormData();
  formData.append("file", file);
  formData.append("minConfidence", minConfidence);

  const loader = document.getElementById("loader");
  loader.style.display = "block"; // Hiển thị loader trong khi đợi

  try {
    // Gọi API để dự đoán và nhận ID kết quả
    const response = await fetch("http://127.0.0.1:8000/predictions", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Failed to get prediction");
    }

    const data = await response.json(); // Nhận dữ liệu từ backend

    if (data.message) {
      alert(data.message); // Nếu không có đối tượng được phát hiện
      return;
    }

    const resultId = data.result_id; // Nhận result_id từ phản hồi

    // Gọi API để lấy ảnh kết quả
    const resultImageResponse = await fetch(
      `http://127.0.0.1:8000/results/${resultId}`
    );
    const resultImageBlob = await resultImageResponse.blob();
    const imageUrl = URL.createObjectURL(resultImageBlob); // Tạo URL cho ảnh

    // Hiển thị kết quả lên giao diện người dùng
    const resultContainer = document.getElementById("result-container");
    resultContainer.innerHTML = ""; // Xóa ảnh cũ
    resultContainer.innerHTML += `<img src="${imageUrl}" alt="Prediction Result">`;
    const resultSection = document.querySelector(".result-section");
    resultSection.style.display = "block"; // Hiển thị kết quả
  } catch (error) {
    console.error(error);
    alert("Error during file upload or prediction.");
  } finally {
    loader.style.display = "none"; // Ẩn loader khi xong
    // resultContainer.innerHTML = ""; // Xóa ảnh kết quả cũ
  }
}

// Hàm cập nhật giá trị phần trăm
function updateConfidenceValue() {
  const minConfidence = document.getElementById("min-confidence").value;
  document.getElementById("confidence-value").textContent = minConfidence;
}
