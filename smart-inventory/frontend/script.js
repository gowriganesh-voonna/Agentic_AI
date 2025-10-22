const API_BASE_URL = 'http://localhost:8000/api';

// Utilities
const qs = (sel, el = document) => el.querySelector(sel);
const qsa = (sel, el = document) => Array.from(el.querySelectorAll(sel));

function showToast(message, type = 'info') {
	const el = qs('#toast');
	el.textContent = message;
	el.classList.add('show');
	if (type === 'error') el.style.borderColor = 'rgba(231,76,60,.35)';
	if (type === 'success') el.style.borderColor = 'rgba(39,174,96,.35)';
	clearTimeout(showToast._t);
	showToast._t = setTimeout(() => el.classList.remove('show'), 2500);
}

async function api(path, opts = {}) {
	const url = `${API_BASE_URL}${path}`;
	const init = {
		method: opts.method || 'GET',
		headers: { 'Content-Type': 'application/json', ...(opts.headers || {}) },
		body: opts.body ? JSON.stringify(opts.body) : undefined,
	};
	try {
		const res = await fetch(url, init);
		const text = await res.text();
		let data;
		try { data = text ? JSON.parse(text) : null; } catch { data = text; }
		if (!res.ok) {
			const msg = (data && (data.detail || data.message)) || res.statusText || 'Request failed';
			throw new Error(msg);
		}
		return data;
	} catch (err) {
		console.error('API error:', err);
		showToast(err.message || 'Network error', 'error');
		throw err;
	}
}

// Response helpers
function toArrayLike(value) {
	if (Array.isArray(value)) return value;
	if (!value || typeof value !== 'object') return [];
	const candidateKeys = ['items', 'data', 'results', 'list', 'hubs', 'Drivers', 'Available_Vehicles', 'vehicles', 'products', 'dispatches'];
	for (const k of candidateKeys) {
		if (Array.isArray(value[k])) return value[k];
	}
	// Sometimes object keyed by id
	if (Object.values(value).every(v => typeof v === 'object')) return Object.values(value);
	return [];
}

// Navigation
qsa('.nav-link').forEach(btn => btn.addEventListener('click', () => {
	qsa('.nav-link').forEach(b => b.classList.remove('active'));
	btn.classList.add('active');
	const target = btn.getAttribute('data-target');
	qsa('.view').forEach(v => v.classList.remove('visible'));
	qs(`#${target}`).classList.add('visible');
	if (target === 'dashboard') loadDashboard();
	if (target === 'hubs') loadHubs();
	if (target === 'inventory') loadInventory();
	if (target === 'drivers') loadDrivers();
	if (target === 'vehicles') loadVehicles();
	if (target === 'dispatches') loadDispatches();
}));

// Dashboard
async function loadDashboard() {
	// Parallel lightweight summaries
	try {
		const [hubsActive, hubsAll, lowStock, expSoon, dispatches] = await Promise.all([
			api('/hub_mangement/hubs/status?status=Active').catch(() => null),
			api('/hub_mangement/hubs/search').catch(() => null),
			api('/inventory_mangement/inventory/low-stock').catch(() => ({ low_stock: [] })),
			api('/inventory_mangement/inventory/expiring-soon').catch(() => ({ expiring_soon_items: [] })),
			api('/vehicle_inventory/dispatches').catch(() => ({ dispatches: [] })),
		]);
		const hubsArr = toArrayLike(hubsActive) || toArrayLike(hubsAll);
		const lowStockArr = toArrayLike(lowStock.low_stock || lowStock);
		const expSoonArr = toArrayLike(expSoon.expiring_soon_items || expSoon);
		const dispatchArr = toArrayLike(dispatches.dispatches || dispatches);
		
		qs('[data-stat="hubs"]').textContent = hubsArr.length || '0';
		qs('[data-stat="lowStock"]').textContent = lowStockArr.length || 0;
		qs('[data-stat="expiring"]').textContent = expSoonArr.length || 0;
		qs('[data-stat="products"]').textContent = dispatchArr.length || '0'; // Show dispatch count as products for now
	} catch (e) { /* toast already shown */ }
}

// Hubs
async function loadHubs() {
	const list = qs('#hubsList');
	list.innerHTML = '<div class="list-item"><span>Loading hubs...</span></div>';
	const status = qs('#hubStatusFilter').value;
	try {
		let hubsRes;
		if (status) hubsRes = await api(`/hub_mangement/hubs/status?status=${encodeURIComponent(status)}`);
		else hubsRes = await api('/hub_mangement/hubs/search');
		renderHubs(toArrayLike(hubsRes));
	} catch (e) {
		list.innerHTML = '<div class="list-item"><span>Failed to load hubs</span></div>';
	}
}

function renderHubs(hubs) {
	const list = qs('#hubsList');
	const q = (qs('#hubSearch').value || '').toLowerCase();
	const filtered = hubs.filter(h => !q || `${h.hub_id} ${h.hub_name}`.toLowerCase().includes(q));
	if (!filtered.length) { list.innerHTML = '<div class="list-item"><span>No hubs found</span></div>'; return; }
	list.innerHTML = '';
	filtered.forEach(h => {
		const el = document.createElement('div');
		el.className = 'list-item';
		el.innerHTML = `
			<div>
				<div><strong>${h.hub_name || h.hubId || 'Hub'}</strong> <span class="meta">#${h.hub_id || h.hubId}</span></div>
				<div class="meta">Manager: ${h.hub_manager || '-'} · Phone: ${h.hub_phone_number || '-'}</div>
				<div class="tags"><span class="tag ${h.status === 'Active' ? 'success' : ''}">${h.status || ''}</span></div>
			</div>
			<div>
				<button class="btn" data-action="edit">Edit</button>
				<button class="btn" data-action="delete">Delete</button>
			</div>`;
		el.querySelector('[data-action="edit"]').addEventListener('click', () => openHubModal(h));
		el.querySelector('[data-action="delete"]').addEventListener('click', () => deleteHub(h));
		list.appendChild(el);
	});
}

qs('#hubStatusFilter').addEventListener('change', loadHubs);
qs('#hubSearch').addEventListener('input', loadHubs);
qs('#addHubBtn').addEventListener('click', () => openHubModal());

function openHubModal(hub) {
	openModal(hub ? 'Update Hub' : 'Add Hub', `
		<form id="hubForm" class="form">
			<div class="form-row">
				<div><label>Hub ID</label><input name="hub_id" required ${hub ? 'readonly' : ''} value="${hub?.hub_id || ''}"></div>
				<div><label>Name</label><input name="hub_name" required value="${hub?.hub_name || ''}"></div>
			</div>
			<div class="form-row">
				<div><label>Manager</label><input name="hub_manager" value="${hub?.hub_manager || ''}"></div>
				<div><label>Phone</label><input name="hub_phone_number" value="${hub?.hub_phone_number || ''}"></div>
			</div>
			<div><label>Address</label><input name="hub_address" value="${hub?.hub_address || ''}"></div>
			<div class="form-row">
				<div><label>Status</label>
					<select name="status">
						<option ${!hub || hub.status==='Active' ? 'selected' : ''}>Active</option>
						<option ${hub && hub.status==='Deactive' ? 'selected' : ''}>Deactive</option>
					</select>
				</div>
				<div></div>
			</div>
			<div class="actions">
				<button type="button" class="btn" id="cancelModal">Cancel</button>
				<button type="submit" class="btn primary">${hub ? 'Update' : 'Create'}</button>
			</div>
		</form>
	`);
	qs('#cancelModal').addEventListener('click', closeModal);
	qs('#hubForm').addEventListener('submit', async (e) => {
		e.preventDefault();
		const form = e.currentTarget;
		const data = Object.fromEntries(new FormData(form).entries());
		try {
			if (hub) {
				await api(`/hub_mangement/hubs/update/${encodeURIComponent(data.hub_id)}`, { method: 'PUT', body: data });
				showToast('Hub updated', 'success');
			} else {
				await api('/hub_mangement/hubs/register', { method: 'POST', body: data });
				showToast('Hub created', 'success');
			}
			closeModal();
			loadHubs();
		} catch {}
	});
}

async function deleteHub(hub) {
	if (!confirm(`Delete hub ${hub.hub_name}?`)) return;
	try {
		await api(`/hub_mangement/hubs/delete/${encodeURIComponent(hub.hub_id)}`, { method: 'DELETE' });
		showToast('Hub deleted', 'success');
		loadHubs();
	} catch {}
}

// Inventory (basic search + actions open modals)
async function loadInventory() {
	const list = qs('#inventoryList');
	list.innerHTML = '<div class="list-item"><span>Loading inventory...</span></div>';
	
	// First get all hubs, then get products for each hub
	try {
		const hubs = await api('/hub_mangement/hubs/search');
		const hubsArr = toArrayLike(hubs);
		if (!hubsArr.length) {
			list.innerHTML = '<div class="list-item"><span>No hubs found. Please add a hub first.</span></div>';
			return;
		}
		
		// Get products from all hubs with their summaries
		const allProducts = [];
		for (const hub of hubsArr.slice(0, 5)) { // Limit to first 5 hubs to avoid too many requests
			try {
				// First get the list of products in this hub
				const products = await api(`/inventory_mangement/inventory/products?hub_id=${encodeURIComponent(hub.hub_id || hub.hubId)}`);
				const productsArr = toArrayLike(products.products || products);
				
				// For each product, get its summary (which includes quantity)
				for (const product of productsArr) {
					try {
						const summary = await api(`/inventory_mangement/inventory/summary?product_id=${encodeURIComponent(product.Product_ID)}&hub_id=${encodeURIComponent(hub.hub_id || hub.hubId)}`);
						allProducts.push({
							...product,
							...summary,
							Hub_ID: hub.hub_id || hub.hubId,
							Hub_Name: hub.hub_name || hub.hubName
						});
					} catch (e) {
						console.warn(`Failed to get summary for product ${product.Product_ID} in hub ${hub.hub_id}:`, e);
						// Fallback to basic product info without quantity
						allProducts.push({
							...product,
							Hub_ID: hub.hub_id || hub.hubId,
							Hub_Name: hub.hub_name || hub.hubName,
							Total_Quantity: 0,
							Batches_Count: 0
						});
					}
				}
			} catch (e) {
				console.warn(`Failed to load products for hub ${hub.hub_id}:`, e);
			}
		}
		
		// Store data for filtering
		list._inventoryData = allProducts;
		renderInventory(allProducts);
	} catch (e) { 
		list.innerHTML = '<div class="list-item"><span>Failed to load inventory</span></div>'; 
	}
}

function renderInventory(items) {
	const list = qs('#inventoryList');
	if (!Array.isArray(items) || !items.length) { 
		list.innerHTML = '<div class="list-item"><span>No products found. Try adding some products first.</span></div>'; 
		return; 
	}
	list.innerHTML = '';
	
	// Filter by search query
	const searchQuery = (qs('#inventorySearch').value || '').toLowerCase();
	const filtered = items.filter(p => {
		if (!searchQuery) return true;
		const name = (p.Product_Name || p.product_name || '').toLowerCase();
		const brand = (p.Brand || p.brand || '').toLowerCase();
		const hub = (p.Hub_Name || p.Hub_ID || p.hub_id || '').toLowerCase();
		return name.includes(searchQuery) || brand.includes(searchQuery) || hub.includes(searchQuery);
	});
	
	if (!filtered.length) {
		list.innerHTML = '<div class="list-item"><span>No products match your search</span></div>';
		return;
	}
	
	filtered.forEach(p => {
		const el = document.createElement('div');
		el.className = 'list-item';
		// Use the summary data which has the correct field names
		const quantity = p.Total_Quantity || 0;
		const batches = p.Batches_Count || 0;
		const expiry = p.Nearest_Expiry || '';
		
		el.innerHTML = `
			<div>
				<div><strong>${p.Product_Name || p.product_name || 'Product'}</strong> <span class="meta">#${p.Product_ID || p.product_id}</span></div>
				<div class="meta">Hub: ${p.Hub_Name || p.Hub_ID || p.hub_id || '-'} · Brand: ${p.Brand || p.brand || '-'} · Qty: <strong style="color: var(--primary);">${quantity}</strong></div>
				<div class="tags">
					<span class="tag">Batches: <strong>${batches}</strong></span>
					${expiry ? `<span class="tag warning">Expiry: ${expiry}</span>` : ''}
					${p.Category ? `<span class="tag info">${p.Category}</span>` : ''}
				</div>
			</div>
			<div>
				<button class="btn" data-action="update">Update</button>
				<button class="btn" data-action="dispatch">Dispatch</button>
			</div>`;
		el.querySelector('[data-action="update"]').addEventListener('click', () => openInventoryUpdateModal(p));
		el.querySelector('[data-action="dispatch"]').addEventListener('click', () => openDispatchModal(p));
		list.appendChild(el);
	});
}

qs('#inventorySearch').addEventListener('input', () => { 
	// Re-render existing inventory with new filter instead of reloading
	const list = qs('#inventoryList');
	const items = list._inventoryData || [];
	if (items.length) {
		renderInventory(items);
	} else {
		clearTimeout(loadInventory._t); 
		loadInventory._t = setTimeout(loadInventory, 250); 
	}
});
qs('#registerProductBtn').addEventListener('click', () => openRegisterProductModal());
qs('#updateStockBtn').addEventListener('click', () => openInventoryUpdateModal());
qs('#dispatchBtn').addEventListener('click', () => openDispatchModal());

function openRegisterProductModal() {
	openModal('Register Product', `
		<form id="regForm" class="form">
			<div class="form-row">
				<div><label>Hub ID</label><input name="Hub_ID" required></div>
				<div><label>Product ID</label><input name="Product_ID" required></div>
			</div>
			<div class="form-row">
				<div><label>Product Name</label><input name="Product_Name" required></div>
				<div><label>Brand</label><input name="Brand"></div>
			</div>
			<div class="form-row">
				<div><label>Quantity</label><input name="Quantity" type="number" min="1" required></div>
				<div><label>Value</label><input name="Value" type="number" step="0.01" min="0" required></div>
			</div>
			<div class="form-row">
				<div><label>Selling Price</label><input name="Selling_Price" type="number" step="0.01" min="0" required></div>
				<div><label>Expiry Date</label><input name="Expiry_Date" type="date" required></div>
			</div>
			<div><label>Description</label><textarea name="Product_Description" rows="3"></textarea></div>
			<div class="actions">
				<button type="button" class="btn" id="cancelModal">Cancel</button>
				<button type="submit" class="btn primary">Register</button>
			</div>
		</form>
	`);
	qs('#cancelModal').addEventListener('click', closeModal);
	qs('#regForm').addEventListener('submit', async (e) => {
		e.preventDefault();
		const data = Object.fromEntries(new FormData(e.currentTarget).entries());
		try {
			await api('/inventory_mangement/inventory/register', { method: 'POST', body: data });
			showToast('Product registered', 'success');
			closeModal();
			loadInventory();
		} catch {}
	});
}

function openInventoryUpdateModal(product) {
	openModal('Update Inventory', `
		<form id="updForm" class="form">
			<div class="form-row">
				<div><label>Hub ID</label><input name="Hub_ID" required value="${product?.Hub_ID || ''}"></div>
				<div><label>Product ID</label><input name="Product_ID" required value="${product?.Product_ID || ''}"></div>
			</div>
			<div class="form-row">
				<div><label>Quantity</label><input name="Quantity" type="number" min="1" required></div>
				<div><label>Value</label><input name="Value" type="number" step="0.01" min="0" required></div>
			</div>
			<div class="form-row">
				<div><label>Expiry Date</label><input name="Expiry_Date" type="date" required></div>
				<div><label>Batch No (optional)</label><input name="Batch_No"></div>
			</div>
			<div class="actions">
				<button type="button" class="btn" id="cancelModal">Cancel</button>
				<button type="submit" class="btn primary">Update</button>
			</div>
		</form>
	`);
	qs('#cancelModal').addEventListener('click', closeModal);
	qs('#updForm').addEventListener('submit', async (e) => {
		e.preventDefault();
		const data = Object.fromEntries(new FormData(e.currentTarget).entries());
		try {
			await api('/inventory_mangement/inventory/update', { method: 'PUT', body: data });
			showToast('Stock updated', 'success');
			closeModal();
			loadInventory();
		} catch {}
	});
}

function openDispatchModal(product) {
	openModal('Dispatch Inventory', `
		<form id="dispForm" class="form">
			<div class="form-row">
				<div><label>From Hub ID</label><input name="From_Hub_ID" required value="${product?.Hub_ID || ''}"></div>
				<div><label>To Hub ID</label><input name="To_Hub_ID" required></div>
			</div>
			<div class="form-row">
				<div><label>Product ID</label><input name="Product_ID" required value="${product?.Product_ID || ''}"></div>
				<div><label>Quantity</label><input name="Quantity" type="number" min="1" required></div>
			</div>
			<div class="actions">
				<button type="button" class="btn" id="cancelModal">Cancel</button>
				<button type="submit" class="btn primary">Dispatch</button>
			</div>
		</form>
	`);
	qs('#cancelModal').addEventListener('click', closeModal);
	qs('#dispForm').addEventListener('submit', async (e) => {
		e.preventDefault();
		const data = Object.fromEntries(new FormData(e.currentTarget).entries());
		try {
			await api('/inventory_mangement/inventory/dispatch', { method: 'POST', body: data });
			showToast('Dispatch created', 'success');
			closeModal();
			loadInventory();
		} catch {}
	});
}

// Drivers
async function loadDrivers() {
	const list = qs('#driversList');
	list.innerHTML = '<div class="list-item"><span>Loading drivers...</span></div>';
	const q = (qs('#driverSearch').value || '').trim();
	const params = new URLSearchParams();
	if (q) params.set('Driver_Name', q);
	try {
		const res = await api(`/driver_mangement/drivers/search_driver?${params.toString()}`);
		renderDrivers(toArrayLike(res));
	} catch { list.innerHTML = '<div class="list-item"><span>Failed to load drivers</span></div>'; }
}

function renderDrivers(drivers) {
	const list = qs('#driversList');
	if (!drivers.length) { list.innerHTML = '<div class="list-item"><span>No drivers found</span></div>'; return; }
	
	// Calculate status counts
	const stats = {
		available: drivers.filter(d => /active|Available/i.test(d.Status || d.status || '')).length,
		assigned: drivers.filter(d => /Assigned/i.test(d.Status || d.status || '')).length,
		total: drivers.length
	};
	
	// Update status cards
	qs('#driverStats [data-stat="available"]').textContent = stats.available;
	qs('#driverStats [data-stat="assigned"]').textContent = stats.assigned;
	qs('#driverStats [data-stat="total"]').textContent = stats.total;
	
	list.innerHTML = '';
	drivers.forEach(d => {
		const el = document.createElement('div');
		el.className = 'list-item';
		el.innerHTML = `
			<div>
				<div><strong>${d.Driver_Name || d.name}</strong> <span class="meta">#${d.Driver_ID || d.driver_id || ''}</span></div>
				<div class="meta">License: ${d.License_No || d.license_number || '-'} · Status: ${d.Status || d.status || '-'}</div>
				<div class="tags">${(d.Status||d.status)?`<span class="tag ${/active|Available/i.test(d.Status||d.status)?'success':''}">${d.Status||d.status}</span>`:''}</div>
			</div>
			<div>
				<button class="btn" data-action="edit">Edit</button>
				<button class="btn" data-action="delete">Delete</button>
			</div>`;
		el.querySelector('[data-action="edit"]').addEventListener('click', () => openDriverModal(d));
		el.querySelector('[data-action="delete"]').addEventListener('click', () => deleteDriver(d));
		list.appendChild(el);
	});
}

qs('#driverSearch').addEventListener('input', () => { clearTimeout(loadDrivers._t); loadDrivers._t = setTimeout(loadDrivers, 250); });
qs('#addDriverBtn').addEventListener('click', () => openDriverModal());

function openDriverModal(driver) {
	openModal(driver ? 'Update Driver' : 'Add Driver', `
		<form id="driverForm" class="form">
			<div class="form-row">
				<div><label>Driver ID</label><input name="Driver_ID" ${driver ? 'readonly' : ''} value="${driver?.Driver_ID || ''}"></div>
				<div><label>Name</label><input name="Driver_Name" required value="${driver?.Driver_Name || driver?.name || ''}"></div>
			</div>
			<div class="form-row">
				<div><label>Age</label><input name="Age" type="number" min="18" max="50" value="${driver?.Age || ''}"></div>
				<div><label>License No</label><input name="License_No" value="${driver?.License_No || driver?.license_number || ''}"></div>
			</div>
			<div class="form-row">
				<div><label>Contact</label><input name="Contact_Number" value="${driver?.Contact_Number || ''}"></div>
				<div><label>Status</label>
					<select name="Status">
						<option ${!driver || /Available/i.test(driver.Status||'') ? 'selected' : ''}>Available</option>
						<option ${/On-Leave/i.test(driver?.Status||'') ? 'selected' : ''}>On-Leave</option>
						<option ${/Inactive/i.test(driver?.Status||'') ? 'selected' : ''}>Inactive</option>
					</select>
				</div>
			</div>
			<div class="actions">
				<button type="button" class="btn" id="cancelModal">Cancel</button>
				<button type="submit" class="btn primary">${driver ? 'Update' : 'Create'}</button>
			</div>
		</form>
	`);
	qs('#cancelModal').addEventListener('click', closeModal);
	qs('#driverForm').addEventListener('submit', async (e) => {
		e.preventDefault();
		const data = Object.fromEntries(new FormData(e.currentTarget).entries());
		try {
			if (driver) {
				await api('/driver_mangement/drivers/update_driver', { method: 'PUT', body: data });
				showToast('Driver updated', 'success');
			} else {
				await api('/driver_mangement/drivers/register_driver', { method: 'POST', body: data });
				showToast('Driver added', 'success');
			}
			closeModal();
			loadDrivers();
		} catch {}
	});
}

async function deleteDriver(driver) {
	if (!confirm(`Delete driver ${driver.Driver_Name || driver.name}?`)) return;
	try {
		await api('/driver_mangement/drivers/delete_driver', { method: 'DELETE', body: { Driver_ID: driver.Driver_ID, Driver_Name: driver.Driver_Name } });
		showToast('Driver deleted', 'success');
		loadDrivers();
	} catch {}
}

// Vehicles
async function loadVehicles() {
	const list = qs('#vehiclesList');
	list.innerHTML = '<div class="list-item"><span>Loading vehicles...</span></div>';
	const q = (qs('#vehicleSearch').value || '').trim();
	const params = new URLSearchParams();
	if (q) params.set('Vehicle_Number', q);
	try {
		const res = await api(`/vehicle_mangement/vehicles/search_vehicle?${params.toString()}`);
		renderVehicles(toArrayLike(res));
	} catch { list.innerHTML = '<div class="list-item"><span>Failed to load vehicles</span></div>'; }
}

function renderVehicles(vehicles) {
	const list = qs('#vehiclesList');
	if (!vehicles.length) { list.innerHTML = '<div class="list-item"><span>No vehicles found</span></div>'; return; }
	
	// Calculate status counts
	const stats = {
		available: vehicles.filter(v => /Available/i.test(v.Status || '')).length,
		'in-transit': vehicles.filter(v => /In-Transit/i.test(v.Status || '')).length,
		'under-maintenance': vehicles.filter(v => /Under-Maintenance/i.test(v.Status || '')).length,
		total: vehicles.length
	};
	
	// Update status cards
	qs('#vehicleStats [data-stat="available"]').textContent = stats.available;
	qs('#vehicleStats [data-stat="in-transit"]').textContent = stats['in-transit'];
	qs('#vehicleStats [data-stat="under-maintenance"]').textContent = stats['under-maintenance'];
	qs('#vehicleStats [data-stat="total"]').textContent = stats.total;
	
	list.innerHTML = '';
	vehicles.forEach(v => {
		const el = document.createElement('div');
		el.className = 'list-item';
		el.innerHTML = `
			<div>
				<div><strong>${v.Vehicle_Number || v.vehicle_number}</strong> <span class="meta">#${v.Vehicle_ID || v.vehicle_id || ''}</span></div>
				<div class="meta">Capacity: ${v.Capacity || '-'} · Status: ${v.Status || '-'}</div>
				<div class="tags">${(v.Status)?`<span class="tag ${/Available/i.test(v.Status)?'success':''}">${v.Status}</span>`:''}</div>
			</div>
			<div>
				<button class="btn" data-action="edit">Edit</button>
				<button class="btn" data-action="delete">Delete</button>
			</div>`;
		el.querySelector('[data-action="edit"]').addEventListener('click', () => openVehicleModal(v));
		el.querySelector('[data-action="delete"]').addEventListener('click', () => deleteVehicle(v));
		list.appendChild(el);
	});
}

qs('#vehicleSearch').addEventListener('input', () => { clearTimeout(loadVehicles._t); loadVehicles._t = setTimeout(loadVehicles, 250); });
qs('#addVehicleBtn').addEventListener('click', () => openVehicleModal());

function openVehicleModal(vehicle) {
	openModal(vehicle ? 'Update Vehicle' : 'Add Vehicle', `
		<form id="vehicleForm" class="form">
			<div class="form-row">
				<div><label>Vehicle ID</label><input name="Vehicle_ID" ${vehicle ? 'readonly' : ''} value="${vehicle?.Vehicle_ID || ''}"></div>
				<div><label>Vehicle Number</label><input name="Vehicle_Number" required value="${vehicle?.Vehicle_Number || ''}"></div>
			</div>
			<div class="form-row">
				<div><label>Capacity</label><input name="Capacity" type="number" min="0" value="${vehicle?.Capacity || ''}"></div>
				<div><label>Status</label>
					<select name="Status">
						<option ${!vehicle || /Available/i.test(vehicle.Status||'') ? 'selected' : ''}>Available</option>
						<option ${/In-Transit/i.test(vehicle?.Status||'') ? 'selected' : ''}>In-Transit</option>
						<option ${/Under-Maintenance/i.test(vehicle?.Status||'') ? 'selected' : ''}>Under-Maintenance</option>
						<option ${/Unavailable/i.test(vehicle?.Status||'') ? 'selected' : ''}>Unavailable</option>
					</select>
				</div>
			</div>
			<div class="actions">
				<button type="button" class="btn" id="cancelModal">Cancel</button>
				<button type="submit" class="btn primary">${vehicle ? 'Update' : 'Create'}</button>
			</div>
		</form>
	`);
	qs('#cancelModal').addEventListener('click', closeModal);
	qs('#vehicleForm').addEventListener('submit', async (e) => {
		e.preventDefault();
		const data = Object.fromEntries(new FormData(e.currentTarget).entries());
		try {
			if (vehicle) {
				await api('/vehicle_mangement/vehicles/update_vehicle', { method: 'PUT', body: data });
				showToast('Vehicle updated', 'success');
			} else {
				await api('/vehicle_mangement/vehicles/register_vehicle', { method: 'POST', body: data });
				showToast('Vehicle added', 'success');
			}
			closeModal();
			loadVehicles();
		} catch {}
	});
}

async function deleteVehicle(vehicle) {
	if (!confirm(`Delete vehicle ${vehicle.Vehicle_Number}?`)) return;
	try {
		await api('/vehicle_mangement/vehicles/delete_vehicle', { method: 'DELETE', body: { Vehicle_ID: vehicle.Vehicle_ID, Vehicle_Number: vehicle.Vehicle_Number } });
		showToast('Vehicle deleted', 'success');
		loadVehicles();
	} catch {}
}

// Dispatches
async function loadDispatches() {
	const list = qs('#dispatchesList');
	list.innerHTML = '<div class="list-item"><span>Loading dispatches...</span></div>';
	try {
		const resp = await api('/vehicle_inventory/dispatches');
		const items = toArrayLike(resp.dispatches || resp);
		renderDispatches(items);
	} catch {
		list.innerHTML = '<div class="list-item"><span>Failed to load dispatches</span></div>';
	}
}

function renderDispatches(items) {
	const list = qs('#dispatchesList');
	if (!Array.isArray(items) || !items.length) { 
		list.innerHTML = '<div class="list-item"><span>No dispatches</span></div>'; 
		// Reset status cards
		qs('#dispatchStats [data-stat="in-progress"]').textContent = '0';
		qs('#dispatchStats [data-stat="in-transit"]').textContent = '0';
		qs('#dispatchStats [data-stat="completed"]').textContent = '0';
		qs('#dispatchStats [data-stat="total"]').textContent = '0';
		return; 
	}

	// Calculate status counts
	const stats = {
		'in-progress': items.filter(d => /In-Progress/i.test(d.Status || d.status || '')).length,
		'in-transit': items.filter(d => /In-Transit/i.test(d.Status || d.status || '')).length,
		completed: items.filter(d => /Completed/i.test(d.Status || d.status || '')).length,
		total: items.length
	};
	
	// Update status cards
	qs('#dispatchStats [data-stat="in-progress"]').textContent = stats['in-progress'];
	qs('#dispatchStats [data-stat="in-transit"]').textContent = stats['in-transit'];
	qs('#dispatchStats [data-stat="completed"]').textContent = stats.completed;
	qs('#dispatchStats [data-stat="total"]').textContent = stats.total;

	// Check if history should be shown
	const showHistory = qs('#showHistoryBtn').textContent.includes('Hide');
	
	// Split active vs history - be more inclusive
	const active = items.filter(d => {
		const status = d.Status || d.status || '';
		return /In-Progress|In-Transit|Pending/i.test(status) || !status;
	});
	const history = items.filter(d => {
		const status = d.Status || d.status || '';
		return /Completed|Cancelled|Finished/i.test(status);
	});

	list.innerHTML = '';

	const section = (title, rows) => {
		if (!rows.length) return;
		const wrapper = document.createElement('div');
		wrapper.innerHTML = `<div class="section-header"><h2>${title}</h2><div class="actions"><span class="meta">${rows.length} items</span></div></div>`;
		rows.forEach(d => {
			const el = document.createElement('div');
			el.className = 'list-item';
			const status = d.Status || d.status || 'In-Progress';
			const qty = d.Quantity || d.quantity || '';
			const driver = d.driver_assigned || d.Driver_Assigned || d.Driver_Name || d.driver_name || '';
			const vehicle = d.vehicle_assigned || d.Vehicle_Assigned || d.Vehicle_Number || d.vehicle_number || '';
			const productId = d.Product_ID || d.product_id || '';
			const fromHub = d.From_Hub_ID || d.from_hub || '';
			const toHub = d.To_Hub_ID || d.to_hub || '';
			const dispatchId = d.dispatch_id || d.id || '';
			
			// Format status with icons and colors
			const statusConfig = {
				'In-Progress': { icon: 'fa-clock', class: 'warning', text: 'In Progress' },
				'In-Transit': { icon: 'fa-truck', class: 'info', text: 'In Transit' },
				'Completed': { icon: 'fa-check-circle', class: 'success', text: 'Completed' },
				'Cancelled': { icon: 'fa-times-circle', class: 'danger', text: 'Cancelled' }
			};
			const statusInfo = statusConfig[status] || { icon: 'fa-question', class: 'warning', text: status };
			
			// Format driver/vehicle status
			const driverStatus = driver === 'Not Assigned' ? '—' : driver;
			const vehicleStatus = vehicle === 'Not Assigned' ? '—' : vehicle;
			const hasAssignment = driver !== 'Not Assigned' && vehicle !== 'Not Assigned';
			
			el.innerHTML = `
				<div>
					<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 12px;">
						<div style="background: var(--primary); color: white; padding: 8px; border-radius: 10px; font-size: 12px; font-weight: 600;">
							<i class="fa-solid fa-box"></i>
						</div>
						<div>
							<div style="font-size: 18px; font-weight: 700; color: var(--text); margin-bottom: 4px;">
								${productId || 'Unknown Product'}
							</div>
							<div style="color: var(--muted); font-size: 13px; font-family: monospace;">
								#${dispatchId || 'N/A'}
							</div>
						</div>
					</div>
					
					<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 12px;">
						<div>
							<div class="meta"><i class="fa-solid fa-warehouse"></i> From: <strong>${fromHub || 'N/A'}</strong></div>
							<div class="meta"><i class="fa-solid fa-warehouse"></i> To: <strong>${toHub || 'N/A'}</strong></div>
						</div>
						<div>
							<div class="meta"><i class="fa-solid fa-cubes"></i> Quantity: <strong>${qty}</strong></div>
							<div class="meta"><i class="fa-solid fa-clock"></i> ${d.timestamp ? new Date(d.timestamp).toLocaleString() : 'N/A'}</div>
						</div>
					</div>
					
					<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 12px;">
						<div>
							<div class="meta">
								<i class="fa-solid fa-user"></i> Driver: 
								<strong style="color: ${hasAssignment ? 'var(--success)' : 'var(--muted)'}">
									${driverStatus}
								</strong>
							</div>
						</div>
						<div>
							<div class="meta">
								<i class="fa-solid fa-truck"></i> Vehicle: 
								<strong style="color: ${hasAssignment ? 'var(--success)' : 'var(--muted)'}">
									${vehicleStatus}
								</strong>
							</div>
						</div>
					</div>
					
					<div class="tags">
						<span class="tag ${statusInfo.class}">
							<i class="fa-solid ${statusInfo.icon}"></i>
							${statusInfo.text}
						</span>
						${hasAssignment ? '<span class="tag success"><i class="fa-solid fa-check"></i> Assigned</span>' : ''}
					</div>
				</div>
				<div style="display: flex; flex-direction: column; gap: 8px;">
					${/In-Progress|Pending/i.test(status) || !status ? 
						'<button class="btn" data-action="auto" style="background: linear-gradient(90deg, #f39c12, #e67e22); border: 0; color: white; font-weight: 600;"><i class="fa-solid fa-magic"></i> Auto Assign</button>' : ''}
					${/In-Transit/i.test(status) ? 
						'<button class="btn" data-action="received" style="background: linear-gradient(90deg, #27ae60, #2ecc71); border: 0; color: white; font-weight: 600;"><i class="fa-solid fa-check-circle"></i> Mark Received</button>' : ''}
				</div>`;
			const auto = el.querySelector('[data-action="auto"]');
			if (auto) auto.addEventListener('click', () => autoAssign(d));
			const recv = el.querySelector('[data-action="received"]');
			if (recv) recv.addEventListener('click', () => markReceived(d));
			wrapper.appendChild(el);
		});
		list.appendChild(wrapper);
	};

	// Show dispatches based on history toggle
	if (active.length) section('Active Dispatches', active);
	if (showHistory && history.length) section('Dispatch History', history);
	if (!active.length && (!showHistory || !history.length)) {
		list.innerHTML = '<div class="list-item"><span>No dispatches found</span></div>';
	}
}

// Global auto-assign trigger (vehicle/driver allocation). Backend expects GET for this endpoint per docs.
qs('#autoAssignBtn').addEventListener('click', async () => {
	try {
		await api('/vehicle_mangement/vehicles/dispatch_vehicle', { method: 'GET' });
		showToast('Auto-dispatch triggered', 'success');
		loadDispatches();
	} catch {}
});

// Show history toggle
qs('#showHistoryBtn').addEventListener('click', () => {
	const btn = qs('#showHistoryBtn');
	const isHistory = btn.textContent.includes('Hide');
	btn.innerHTML = isHistory ? '<i class="fa-solid fa-history"></i> Show History' : '<i class="fa-solid fa-eye-slash"></i> Hide History';
	loadDispatches();
});

function getDispatchId(d) {
	return d.dispatch_id || d.Dispatch_ID || d.id || d.DispatchId || d.Dispatch_ID || '';
}

async function autoAssign(d) {
	const id = getDispatchId(d);
	if (!id) { showToast('Missing dispatch id', 'error'); return; }
	try {
		await api(`/vehicle_inventory/auto_assign/${encodeURIComponent(id)}`, { method: 'POST' });
		showToast('Assigned', 'success');
		loadDispatches();
	} catch {}
}
async function markReceived(d) {
	const id = getDispatchId(d);
	if (!id) { showToast('Missing dispatch id', 'error'); return; }
	try {
		await api('/vehicle_inventory/mark_dispatch_received', { method: 'PUT', body: { dispatch_id: id } });
		showToast('Marked received', 'success');
		loadDispatches();
	} catch {}
}

// Modal helpers
function openModal(title, bodyHTML) {
	qs('#modalTitle').textContent = title;
	qs('#modalBody').innerHTML = bodyHTML;
	qs('#modal').classList.remove('hidden');
}
function closeModal() { qs('#modal').classList.add('hidden'); }
qs('#modalClose').addEventListener('click', closeModal);

// Alert functionality
async function loadLowStockAlerts() {
	try {
		const response = await api('/inventory_mangement/inventory/low-stock');
		const items = toArrayLike(response.low_stock || response);
		renderAlertModal('Low Stock Alerts', items, 'warning');
	} catch (e) {
		showToast('Failed to load low stock alerts', 'error');
	}
}

async function loadExpiringAlerts() {
	try {
		const response = await api('/inventory_mangement/inventory/expiring-soon');
		const items = toArrayLike(response.expiring_soon_items || response);
		renderAlertModal('Expiring Soon Alerts', items, 'danger');
	} catch (e) {
		showToast('Failed to load expiring alerts', 'error');
	}
}

function renderAlertModal(title, items, type) {
	if (!items || !items.length) {
		openModal(title, `
			<div style="text-align: center; padding: 20px;">
				<i class="fa-solid fa-check-circle" style="font-size: 48px; color: var(--success); margin-bottom: 16px;"></i>
				<h3 style="color: var(--text); margin-bottom: 8px;">No Alerts</h3>
				<p style="color: var(--muted);">All products are in good condition!</p>
			</div>
		`);
		return;
	}

	let itemsHTML = '';
	items.forEach(item => {
		const productName = item.Product_Name || item.product_name || 'Unknown Product';
		const productId = item.Product_ID || item.product_id || 'N/A';
		const hubId = item.Hub_ID || item.hub_id || 'N/A';
		const quantity = item.Total_Quantity || item.quantity || item.Quantity || 'N/A';
		const expiry = item.Expiry_Date || item.expiry_date || item.Nearest_Expiry || '';
		
		itemsHTML += `
			<div class="alert-item">
				<div class="alert-header">
					<div class="alert-product">
						<strong>${productName}</strong>
						<span class="meta">#${productId}</span>
					</div>
					<div class="alert-quantity ${type}">${quantity}</div>
				</div>
				<div class="alert-details">
					<div class="meta">Hub: ${hubId}</div>
					${expiry ? `<div class="meta">Expiry: ${expiry}</div>` : ''}
				</div>
			</div>
		`;
	});

	openModal(title, `
		<div class="alert-container">
			<div class="alert-summary">
				<i class="fa-solid ${type === 'warning' ? 'fa-exclamation-triangle' : 'fa-clock'}" style="color: var(--${type}); font-size: 24px;"></i>
				<span style="margin-left: 12px; font-weight: 600; color: var(--text);">${items.length} ${type === 'warning' ? 'Low Stock' : 'Expiring'} Items</span>
			</div>
			<div class="alert-list">
				${itemsHTML}
			</div>
		</div>
	`);
}

// Add click handlers for alert cards
document.addEventListener('DOMContentLoaded', () => {
	qs('#stat-low-stock').addEventListener('click', loadLowStockAlerts);
	qs('#stat-expiring').addEventListener('click', loadExpiringAlerts);
});

// Initial load
loadDashboard();

