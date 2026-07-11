async function submitPackage() {
    const fileInput = document.getElementById('imageInput');
    const deliveryCompanyInput = document.getElementById('deliveryCompanyInput').value;
    const resultDiv = document.getElementById('result');
    const sumbitBtn = document.getElementById('submitBtn');

    //Validation - make sure a file was selected
    if(!fileInput.files[0]) {
        alert("Please select an image file to upload.");
        return;
    }

    //Build form data to send to API
    const formData = new FormData();
    formData.append('image', fileInput.files[0]);
    formData.append('delivery_company', deliveryCompanyInput);

    //show loading state while waiting for server
    submmitBtn.disabled = true;
    submitBtn.textContent = '⏲️Processing...';
    resultDiv.style.display = 'none';

    try {
        const response = await fetch('http://127.0.0.1:8000/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        resultDiv.style.display = 'block';

        if (response.ok) {
            resultDiv.className = '';
            resultDiv.innerHTML = `
                <div class="result-row">
                    <span class="label"> Status</span>
                    span class="value"><span class="status-badge status-waiting">Waiting</span></span>
                </div>
                <div class="result-row">
                    <span class="label"> Name</span>
                    <span class="value">${data.name || 'Not found'}</span>
                </div>
                <div class="result-row">
                    <span class="label"> Unit</span>
                    <span class="value">${data.unit || 'Not found'}</span>
                </div>
                <div class="result-row">
                    <span class="label"> Phone</span>
                    <span class="value">${data.phone || 'Not found'}</span>
                </div>
                <div class="result-row">
                    <span class="label"> Delivery Company</span>
                    <span class="value">${data.delivery_company || 'Not specified'}</span>
                </div>
            `;
        }
        else {
            resultDiv.className = 'error';
            resultDiv.innerHTML = 'Error logging package.Please try again.';
        }
    } catch (error) {
        resultDiv.style.display = 'block';
        resultDiv.className = 'error';
        resultDiv.innerHTML = 'Could not connect to the server. Is it running?';
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Log Package';
            
    }
}