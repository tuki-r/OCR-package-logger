// ── Submit new package ──────────────────────────────────────────
async function submitPackage() {
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
    formData.append('delivery_company', deliveryCompany);

    submitBtn.disabled = true;
    submitBtn.textContent = '⏳ Processing...';
    resultDiv.style.display = 'none';

    try {
        const response = await fetch('http://127.0.0.1:8000/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();
        resultDiv.style.display = 'block';

        if (response.ok) {
            resultDiv.className = 'success';
            resultDiv.innerHTML = `✅ Package logged — ${data.name || 'Unknown'}, Unit ${data.unit || '?'}`;
            fileInput.value = '';
            document.getElementById('deliveryCompany').value = '';
            loadPackages(); // refresh the table
        } else {
            resultDiv.className = 'error';
            resultDiv.innerHTML = '❌ Error logging package. Please try again.';
        }

    } catch (error) {
        resultDiv.style.display = 'block';
        resultDiv.className = 'error';
        resultDiv.innerHTML = '❌ Could not connect to server.';
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Log Package';
    }
}

// ── Load and display packages ───────────────────────────────────
let currentFilter = 'all';

async function loadPackages() {
    try {
        const response = await fetch('http://127.0.0.1:8000/packages');
        const packages = await response.json();
        renderTable(packages);
    } catch (error) {
        console.error('Could not load packages:', error);
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
                        <div class="icon">📭</div>
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
window.addEventListener('load', loadPackages);