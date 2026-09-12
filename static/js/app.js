let currentPackageID = null;
let currentFilter = 'all';


async function submitPackage () {
    const fileInput = document.getElementById('imageInput');
    const deliveryCompany = document.getElementById('deliveryCompany').value;
    const resultDiv = document.getElementById('result');
    const submitBtn = document.getElementById('submitBtn');

    if (!fileInput.files[0]) {
        alert('Please select or take a photo first');
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    const packageImageInput = document.getElementById('packageImageInput');
    if (packageImageInput.files[0]) {
        formData.append('package_image', packageImageInput.files[0]);
    }
    formData.append('delivery_company', deliveryCompany);

    submitBtn.disabled = true;
    submitBtn.textContent = 'Processing...';
    resultDiv.style.display = 'none';

    try {
        const response = await fetch('http://localhost:8000/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        resultDiv.style.display = 'block';

        if (response.ok) {
            resultDiv.className = 'success';
            resultDiv.innerHTML = `:) Package logged — ${data.name || 'Unknown'}, Unit ${data.unit || '?'}`;
            fileInput.value = '';
            document.getElementById('deliveryCompany').value = '';
            loadPackages(); // refresh the table
        } else {
            resultDiv.className = 'error';
            resultDiv.innerHTML = ' :( Error logging package. Please try again.';
        }

    } catch (error) {
        resultDiv.style.display = 'block';
        resultDiv.className = 'error';
        resultDiv.innerHTML = ' :( Could not connect to server.';
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Log Package';
    }
}


// ── Load and display packages ───────────────────────────────────


async function loadPackages() {
    try {
        const response = await fetch('http://localhost:8000/packages');
        const packages = await response.json();
        renderTable(packages);
    } catch (error) {
        console.error(':( Could not load packages:', error);
    }
}

function renderTable(packages) {
    const tbody = document.getElementById('packageTableBody');
    const filtered = packages.filter(p => {
        if (currentFilter === 'all') return true;
        if (currentFilter === 'waiting') return p.Status === 'Waiting';
        if (currentFilter === 'collected') return p.Status === 'Collected';
    });

    if (filtered.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="7">
                    <div class="empty-state">
                        <div class="icon">.</div>
                        No packages found
                    </div>
                </td>
            </tr>`;
        return;
    }

    tbody.innerHTML = filtered.map(p => `
        <tr>
            <td>${p.DateLogged || '—'}</td>
            <td>${p.DeliveryComp_Name || '—'}</td>
            <td>${p.ResidentName || '—'}</td>
            <td>${p.Unit || '—'}</td>
            <td>${p.PhoneNumber || '—'}</td>
            <td><span class="badge ${p.Status === 'Collected' ? 'badge-collected' : 'badge-waiting'}">${p.Status}</span></td>
            <td>${p.CollectedBy || '—'}</td>
            <td>${p.Relation || '—'}</td>
            <td>${p.DateCollected || '—'}</td>
            <td><button class="btn btn-secondary" onclick="openModal(${p.ID})">Manage</button></td>
        </tr> 
    `).join('');
}

function setFilter(filter) {
    currentFilter = filter;
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById('tab-' + filter).classList.add('active');
    loadPackages();
}

// Load packages when page opens

function openModal(packageID) {
    currentPackageID = packageID;

    document.getElementById('collectedByInput').value = '';
    document.getElementById('relationshipSelect').value = '';
    document.getElementById('imageContainer').style.display = 'none';
    document.getElementById('stickerImage').src = '';

    document.getElementById('manageModal').style.display = 'block';
}

function closeModal() {
    document.getElementById('manageModal').style.display = 'none';
    currentPackageID = null;
}

async function viewImage(type = 'sticker') {
    if (!currentPackageID) return;

    try {
        const response = await fetch (`http://localhost:8000/packages/${currentPackageID}/image?type=${type}`);
        const data = await response.json();

        if (response.ok && data.image) {
            document.getElementById('imageLabel').textContent = type === 'sticker' ? 'Courier Sticker' : 'Package Photo';
            document.getElementById('stickerImage').src = `data:image/jpeg;base64,${data.image}`;
            document.getElementById('imageContainer').style.display = 'block';
        } else {
            alert('No image found');
        }
    } catch (error) {
        alert('Could not load image');
    }
    
}
 
async function confirmCollected () {
    const collectedBy = document.getElementById('collectedByInput').value.trim();
    const relation = document.getElementById('relationshipSelect').value;
    
    if (!collectedBy) {
        alert('Please enter the name of the person collecting');
        return;
    }

    if (!relation) {
        alert('Please select a relationship');
        return;
    }

    const formData = new FormData();
    formData.append('collected_by', collectedBy);
    formData.append('relation', relation)

    try {
        const response = await fetch (`http://localhost:8000/packages/${currentPackageID}/collect`, {
            method: 'PUT',
            body: formData
        });

        if (response.ok) {
            closeModal();
            loadPackages();
        } else {
            alert('Failed to mark as collected');
        }
    } catch (error) {
        alert('Could not connect to server');
    }
}

async function confirmPackage() {
    if(!confirm('Are you sure you want to delte this log? This cant be undone.')) return;
    
    try {
        const response = await fetch (`http://localhost:8000/packages/${currentPackageID}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            closeModal();
            loadPackages();
        } else {
            alert('Failed to delete package');
        }
    } catch (error) {
        alert('Could not connect to server');
    }
}

document.getElementById('manageModal').addEventListener('click', function(e) {
    if (e.target === this) closeModal();
});

window.addEventListener('load', loadPackages);