// Smart Inventory & Dispatch Management System - Frontend JavaScript

// Configuration
const API_BASE_URL = 'http://127.0.0.1:8000/api';

// Global state
let currentPage = 'dashboard';
let hubs = [];
let inventory = [];
let vehicles = [];
let drivers = [];
let dispatches = [];

// Dispatch Database/Storage
const DISPATCH_STORAGE_KEY = 'smart_inventory_dispatches';
let dispatchDatabase = [];

// Initialize dispatch database from localStorage
function initializeDispatchDatabase() {
    try {
        const stored = localStorage.getItem(DISPATCH_STORAGE_KEY);
        if (stored) {
            dispatchDatabase = JSON.parse(stored);
        } else {
            dispatchDatabase = [];
        }
        console.log('Dispatch database initialized with', dispatchDatabase.length, 'records');
    } catch (error) {
        console.error('Error initializing dispatch database:', error);
        dispatchDatabase = [];
    }
}

// Save dispatch database to localStorage
function saveDispatchDatabase() {
    try {
        localStorage.setItem(DISPATCH_STORAGE_KEY, JSON.stringify(dispatchDatabase));
        console.log('Dispatch database saved with', dispatchDatabase.length, 'records');
    } catch (error) {
        console.error('Error saving dispatch database:', error);
    }
}

// Add new dispatch to database
function addDispatchToDatabase(dispatchData) {
    const dispatch = {
        id: 'DISP_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9),
        ...dispatchData,
        status: 'Pending',
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
        history: [{
            status: 'Pending',
            timestamp: new Date().toISOString(),
            action: 'Created'
        }]
    };
    
    dispatchDatabase.push(dispatch);
    saveDispatchDatabase();
    return dispatch;
}

// Update dispatch status in database
function updateDispatchStatus(dispatchId, newStatus, action = 'Status Updated') {
    const dispatch = dispatchDatabase.find(d => d.id === dispatchId);
    if (dispatch) {
        dispatch.status = newStatus;
        dispatch.updated_at = new Date().toISOString();
        dispatch.history.push({
            status: newStatus,
            timestamp: new Date().toISOString(),
            action: action
        });
        saveDispatchDatabase();
        return dispatch;
    }
    return null;
}

// Get dispatches by status
function getDispatchesByStatus(status) {
    return dispatchDatabase.filter(d => d.status === status);
}

// Get all dispatches
function getAllDispatches() {
    return dispatchDatabase;
}

// Clear dispatch database (for testing)
function clearDispatchDatabase() {
    if (confirm('Are you sure you want to clear all pending and in-transit dispatches? Completed dispatches will be kept.')) {
        // Keep only completed dispatches
        const completedDispatches = dispatchDatabase.filter(d => d.status === 'Completed');
        dispatchDatabase = completedDispatches;
        saveDispatchDatabase();
        dispatches = getAllDispatches();
        renderDispatchesTable();
        updateDispatchStats();
        showToast(`Cleared pending/in-transit dispatches. Kept ${completedDispatches.length} completed dispatches.`, 'info');
    }
}

// Clear ALL dispatch records (including completed ones)
function clearAllDispatchRecords() {
    if (confirm('Are you sure you want to clear ALL dispatch records including completed ones? This action cannot be undone.')) {
        dispatchDatabase = [];
        saveDispatchDatabase();
        dispatches = [];
        renderDispatchesTable();
        updateDispatchStats();
        showToast('All dispatch records cleared', 'info');
    }
}

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

async function initializeApp() {
    showLoading();
    
    try {
        // Initialize dispatch database
        initializeDispatchDatabase();
        
        // Load initial data with individual error handling
        await Promise.allSettled([
            loadDashboardStats(),
            loadHubs(),
            loadInventory(),
            loadVehicles(),
            loadDrivers(),
            loadDispatches()
        ]);
        
        // Setup event listeners
        setupEventListeners();
        
        // Show dashboard by default
        showPage('dashboard');
        
    } catch (error) {
        console.error('Error initializing app:', error);
        showToast('Error initializing application', 'error');
    } finally {
        hideLoading();
    }
}

// Event Listeners Setup
function setupEventListeners() {
    // Navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const page = link.getAttribute('data-page');
            showPage(page);
        });
    });

    // Mobile navigation toggle
    const navToggle = document.getElementById('nav-toggle');
    const navMenu = document.getElementById('nav-menu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => {
            navMenu.classList.toggle('active');
        });
    }

    // Search functionality
    setupSearchListeners();
}

function setupSearchListeners() {
    // Hub search
    const hubSearch = document.getElementById('hub-search');
    if (hubSearch) {
        hubSearch.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                searchHubs();
            }
        });
    }

    // Inventory search
    const inventorySearch = document.getElementById('inventory-search');
    if (inventorySearch) {
        inventorySearch.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                searchInventory();
            }
        });
    }

    // Vehicle search
    const vehicleSearch = document.getElementById('vehicle-search');
    if (vehicleSearch) {
        vehicleSearch.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                searchVehicles();
            }
        });
    }

    // Driver search
    const driverSearch = document.getElementById('driver-search');
    if (driverSearch) {
        driverSearch.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                searchDrivers();
            }
        });
    }
}

// Navigation Functions
function showPage(pageName) {
    // Hide all pages
    document.querySelectorAll('.page').forEach(page => {
        page.classList.remove('active');
    });

    // Show selected page
    const targetPage = document.getElementById(pageName);
    if (targetPage) {
        targetPage.classList.add('active');
    }

    // Update navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });

    const activeLink = document.querySelector(`[data-page="${pageName}"]`);
    if (activeLink) {
        activeLink.classList.add('active');
    }

    currentPage = pageName;

    // Close mobile menu
    const navMenu = document.getElementById('nav-menu');
    if (navMenu) {
        navMenu.classList.remove('active');
    }

    // Load page-specific data
    switch (pageName) {
        case 'dashboard':
            loadDashboardStats();
            break;
        case 'hubs':
            loadHubs();
            break;
        case 'inventory':
            loadInventory();
            break;
        case 'vehicles':
            loadVehicles();
            break;
        case 'drivers':
            loadDrivers();
            break;
        case 'dispatch':
            loadDispatches();
            break;
    }
}

// API Functions
async function apiCall(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    const config = { ...defaultOptions, ...options };

    try {
        const response = await fetch(url, config);
        
        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
        }

        return await response.json();
    } catch (error) {
        console.error('API call failed:', error);
        throw error;
    }
}

// Dashboard Functions
async function loadDashboardStats() {
    try {
        // Load stats from different endpoints with proper parameters
        const [hubsData, vehiclesData, driversData] = await Promise.all([
            apiCall('/hub_mangement/hubs/status?status=Active'),
            apiCall('/vehicle_mangement/vehicles/search_vehicle'),
            apiCall('/driver_mangement/drivers/search_driver')
        ]);

        // Update dashboard stats
        document.getElementById('total-hubs').textContent = hubsData.hubs?.length || 0;
        document.getElementById('total-vehicles').textContent = vehiclesData.Available_Vehicles?.length || 0;
        document.getElementById('total-drivers').textContent = driversData?.length || 0;

        // Load inventory count (simplified)
        try {
            // Count products across all hubs
            let totalProducts = 0;
            for (const hub of hubs) {
                try {
                    const inventoryData = await apiCall(`/inventory_mangement/inventory/products?hub_id=${hub.hub_id}&limit=1000`);
                    if (inventoryData && inventoryData.products) {
                        totalProducts += inventoryData.products.length;
                    }
                } catch (hubError) {
                    console.warn(`Could not load inventory for hub ${hub.hub_id}:`, hubError);
                }
            }
            document.getElementById('total-products').textContent = totalProducts;
        } catch (error) {
            console.warn('Could not load inventory count:', error);
            document.getElementById('total-products').textContent = '0';
        }

        // Load additional dashboard stats
        await loadAdditionalDashboardStats();

    } catch (error) {
        console.error('Error loading dashboard stats:', error);
        // Don't show toast for dashboard stats errors to avoid spam
        // showToast('Error loading dashboard statistics', 'error');
    }
}

async function loadAdditionalDashboardStats() {
    try {
        // Load low stock count
        let lowStockCount = 0;
        for (const hub of hubs) {
            try {
                const lowStockData = await apiCall(`/inventory_mangement/inventory/low-stock?hub_id=${hub.hub_id}`);
                if (lowStockData && Array.isArray(lowStockData)) {
                    lowStockCount += lowStockData.length;
                }
            } catch (error) {
                console.warn(`Error loading low stock for hub ${hub.hub_id}:`, error);
            }
        }
        document.getElementById('low-stock-count').textContent = lowStockCount;

        // Load expiring count
        let expiringCount = 0;
        for (const hub of hubs) {
            try {
                const expiringData = await apiCall(`/inventory_mangement/inventory/expiring-soon?hub_id=${hub.hub_id}`);
                if (expiringData && Array.isArray(expiringData)) {
                    expiringCount += expiringData.length;
                }
            } catch (error) {
                console.warn(`Error loading expiring items for hub ${hub.hub_id}:`, error);
            }
        }
        document.getElementById('expiring-count').textContent = expiringCount;

        // Load pending dispatches
        const pendingDispatches = dispatches.filter(d => d.Status === 'Pending').length;
        document.getElementById('pending-dispatches-dash').textContent = pendingDispatches;

        // Load active vehicles
        const vehiclesData = await apiCall('/vehicle_mangement/vehicles/search_vehicle');
        const activeVehicles = vehiclesData?.Available_Vehicles?.filter(v => v.Status === 'Available').length || 0;
        document.getElementById('active-vehicles').textContent = activeVehicles;

    } catch (error) {
        console.error('Error loading additional dashboard stats:', error);
    }
}

// Hub Management Functions
async function loadHubs() {
    try {
        const data = await apiCall('/hub_mangement/hubs/search');
        hubs = data.hubs || [];
        renderHubsTable();
        updateHubSelects();
    } catch (error) {
        console.error('Error loading hubs:', error);
        showToast('Error loading hubs', 'error');
    }
}

function renderHubsTable() {
    const tbody = document.getElementById('hubs-tbody');
    if (!tbody) return;

    tbody.innerHTML = '';

    if (hubs.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center">No hubs found</td></tr>';
        return;
    }

    hubs.forEach(hub => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${hub.hub_id}</td>
            <td>${hub.hub_name}</td>
            <td>${hub.hub_manager}</td>
            <td>${hub.hub_phone_number}</td>
            <td>${hub.hub_address}</td>
            <td><span class="status-badge ${hub.status.toLowerCase()}">${hub.status}</span></td>
            <td>
                <button class="btn btn-secondary" onclick="editHub('${hub.hub_id}')">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-danger" onclick="deleteHub('${hub.hub_id}', '${hub.hub_name}', '${hub.hub_manager}')">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function updateHubSelects() {
    const selects = document.querySelectorAll('#hub-select, #from-hub-select, #to-hub-select');
    selects.forEach(select => {
        const currentValue = select.value;
        select.innerHTML = '<option value="">All Hubs</option>';
        
        hubs.forEach(hub => {
            const option = document.createElement('option');
            option.value = hub.hub_id;
            option.textContent = `${hub.hub_name} (${hub.hub_id})`;
            if (hub.hub_id === currentValue) {
                option.selected = true;
            }
            select.appendChild(option);
        });
    });
}

function searchHubs() {
    const searchTerm = document.getElementById('hub-search').value.toLowerCase();
    const statusFilter = document.getElementById('hub-status-filter').value;

    let filteredHubs = hubs.filter(hub => {
        const matchesSearch = !searchTerm || 
            hub.hub_id.toLowerCase().includes(searchTerm) ||
            hub.hub_name.toLowerCase().includes(searchTerm);
        
        const matchesStatus = !statusFilter || hub.status === statusFilter;
        
        return matchesSearch && matchesStatus;
    });

    // Temporarily replace hubs array for rendering
    const originalHubs = hubs;
    hubs = filteredHubs;
    renderHubsTable();
    hubs = originalHubs;
}

function filterHubs() {
    searchHubs();
}

function showHubForm(hubId = null) {
    const isEdit = hubId !== null;
    const hub = isEdit ? hubs.find(h => h.hub_id === hubId) : null;

    const modalContent = `
        <div class="modal-header">
            <h2>${isEdit ? 'Edit Hub' : 'Add New Hub'}</h2>
            <button class="close-btn" onclick="closeModal()">&times;</button>
        </div>
        <form id="hub-form">
            <div class="form-group">
                <label for="hub-id">Hub ID *</label>
                <input type="text" id="hub-id" name="hub_id" value="${hub?.hub_id || ''}" ${isEdit ? 'readonly' : 'required'}>
            </div>
            <div class="form-group">
                <label for="hub-name">Hub Name *</label>
                <input type="text" id="hub-name" name="hub_name" value="${hub?.hub_name || ''}" required>
            </div>
            <div class="form-group">
                <label for="hub-manager">Hub Manager *</label>
                <input type="text" id="hub-manager" name="hub_manager" value="${hub?.hub_manager || ''}" required>
            </div>
            <div class="form-group">
                <label for="hub-phone">Phone Number *</label>
                <input type="tel" id="hub-phone" name="hub_phone_number" value="${hub?.hub_phone_number || ''}" required>
            </div>
            <div class="form-group">
                <label for="hub-address">Address *</label>
                <textarea id="hub-address" name="hub_address" required>${hub?.hub_address || ''}</textarea>
            </div>
            ${isEdit ? `
            <div class="form-group">
                <label for="hub-status">Status</label>
                <select id="hub-status" name="status">
                    <option value="Active" ${hub?.status === 'Active' ? 'selected' : ''}>Active</option>
                    <option value="Deactive" ${hub?.status === 'Deactive' ? 'selected' : ''}>Deactive</option>
                </select>
            </div>
            ` : ''}
            <div class="form-actions">
                <button type="button" class="btn btn-secondary" onclick="closeModal()">Cancel</button>
                <button type="submit" class="btn btn-primary">${isEdit ? 'Update' : 'Create'} Hub</button>
            </div>
        </form>
    `;

    showModal(modalContent);

    // Handle form submission
    document.getElementById('hub-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        await submitHubForm(isEdit, hubId);
    });
}

async function submitHubForm(isEdit, hubId) {
    const formData = new FormData(document.getElementById('hub-form'));
    const data = Object.fromEntries(formData.entries());

    try {
        showLoading();
        
        if (isEdit) {
            await apiCall(`/hub_mangement/hubs/update/${hubId}`, {
                method: 'PUT',
                body: JSON.stringify(data)
            });
            showToast('Hub updated successfully', 'success');
        } else {
            await apiCall('/hub_mangement/hubs/register', {
                method: 'POST',
                body: JSON.stringify(data)
            });
            showToast('Hub created successfully', 'success');
        }

        closeModal();
        await loadHubs();
        await loadDashboardStats();
        
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        hideLoading();
    }
}

function editHub(hubId) {
    showHubForm(hubId);
}

async function deleteHub(hubId, hubName, hubManager) {
    if (!confirm(`Are you sure you want to delete hub "${hubName}"?`)) {
        return;
    }

    try {
        showLoading();
        await apiCall(`/hub_mangement/hubs/delete/${hubId}?hub_name=${encodeURIComponent(hubName)}&hub_manager=${encodeURIComponent(hubManager)}`, {
            method: 'DELETE'
        });
        
        showToast('Hub deleted successfully', 'success');
        await loadHubs();
        await loadDashboardStats();
        
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        hideLoading();
    }
}

// Inventory Management Functions
async function loadInventory() {
    try {
        // Load products from all hubs
        const allProducts = [];
        
        for (const hub of hubs) {
            try {
                // Try to get product summary with quantities
                const data = await apiCall(`/inventory_mangement/inventory/products?hub_id=${hub.hub_id}&limit=1000`);
                if (data && data.products && Array.isArray(data.products)) {
                    for (const product of data.products) {
                        try {
                            // Get detailed product summary with quantities
                            const summaryData = await apiCall(`/inventory_mangement/inventory/summary?product_id=${product.Product_ID}&hub_id=${hub.hub_id}`);
                            if (summaryData) {
                                product.hub_name = hub.hub_name;
                                product.Hub_ID = hub.hub_id;
                                product.Total_Quantity = summaryData.Total_Quantity || 0;
                                product.Nearest_Expiry = summaryData.Nearest_Expiry || 'N/A';
                                allProducts.push(product);
                            }
                        } catch (summaryError) {
                            // If summary fails, use basic product data
                            product.hub_name = hub.hub_name;
                            product.Hub_ID = hub.hub_id;
                            product.Total_Quantity = 0;
                            product.Nearest_Expiry = 'N/A';
                            allProducts.push(product);
                        }
                    }
                }
            } catch (error) {
                console.warn(`Error loading inventory for hub ${hub.hub_id}:`, error);
            }
        }
        
        inventory = allProducts;
        renderInventoryTable();
        updateInventoryAlerts();
    } catch (error) {
        console.error('Error loading inventory:', error);
        showToast('Error loading inventory', 'error');
    }
}

function renderInventoryTable() {
    const tbody = document.getElementById('inventory-tbody');
    if (!tbody) return;

    tbody.innerHTML = '';

    if (inventory.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center">No inventory found</td></tr>';
        return;
    }

    inventory.forEach(item => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${item.Product_ID}</td>
            <td>${item.Product_Name}</td>
            <td>${item.hub_name || item.Hub_ID}</td>
            <td>${item.Total_Quantity || 0}</td>
            <td>${item.Nearest_Expiry || 'N/A'}</td>
            <td><span class="status-badge ${getInventoryStatus(item)}">${getInventoryStatus(item)}</span></td>
            <td>
                <button class="btn btn-secondary" onclick="viewInventoryDetails('${item.Product_ID}', '${item.Hub_ID}')">
                    <i class="fas fa-eye"></i>
                </button>
                <button class="btn btn-primary" onclick="updateInventory('${item.Product_ID}', '${item.Hub_ID}')">
                    <i class="fas fa-plus"></i>
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function getInventoryStatus(item) {
    const quantity = item.Total_Quantity || 0;
    if (quantity === 0) return 'out-of-stock';
    if (quantity < 10) return 'low-stock';
    return 'in-stock';
}

async function updateInventoryAlerts() {
    try {
        const [lowStockData, expiringData] = await Promise.all([
            apiCall('/inventory_mangement/inventory/low-stock'),
            apiCall('/inventory_mangement/inventory/expiring-soon')
        ]);

        const lowStockCount = lowStockData.low_stock?.length || 0;
        const expiringCount = expiringData.expiring_soon_items?.length || 0;

        document.getElementById('low-stock-count').textContent = `${lowStockCount} items need restocking`;
        document.getElementById('expiring-count').textContent = `${expiringCount} items expiring within 30 days`;

    } catch (error) {
        console.error('Error loading inventory alerts:', error);
    }
}

function searchInventory() {
    const searchTerm = document.getElementById('inventory-search').value.toLowerCase();
    const hubFilter = document.getElementById('hub-select').value;

    let filteredInventory = inventory.filter(item => {
        const matchesSearch = !searchTerm || 
            item.Product_ID.toLowerCase().includes(searchTerm) ||
            item.Product_Name.toLowerCase().includes(searchTerm);
        
        const matchesHub = !hubFilter || item.Hub_ID === hubFilter;
        
        return matchesSearch && matchesHub;
    });

    // Temporarily replace inventory array for rendering
    const originalInventory = inventory;
    inventory = filteredInventory;
    renderInventoryTable();
    inventory = originalInventory;
}

function showInventoryForm() {
    const modalContent = `
        <div class="modal-header">
            <h2>Add New Product</h2>
            <button class="close-btn" onclick="closeModal()">&times;</button>
        </div>
        <form id="inventory-form">
            <div class="form-group">
                <label for="inventory-hub">Hub *</label>
                <select id="inventory-hub" name="Hub_ID" required>
                    <option value="">Select Hub</option>
                </select>
            </div>
            <div class="form-group">
                <label for="product-id">Product ID *</label>
                <input type="text" id="product-id" name="Product_ID" required>
            </div>
            <div class="form-group">
                <label for="product-name">Product Name *</label>
                <input type="text" id="product-name" name="Product_Name" required>
            </div>
            <div class="form-group">
                <label for="quantity">Quantity *</label>
                <input type="number" id="quantity" name="Quantity" min="1" required>
            </div>
            <div class="form-group">
                <label for="value">Purchase Value *</label>
                <input type="number" id="value" name="Value" step="0.01" min="0" required>
            </div>
            <div class="form-group">
                <label for="selling-price">Selling Price *</label>
                <input type="number" id="selling-price" name="Selling_Price" step="0.01" min="0" required>
            </div>
            <div class="form-group">
                <label for="expiry-date">Expiry Date *</label>
                <input type="date" id="expiry-date" name="Expiry_Date" required>
            </div>
            <div class="form-group">
                <label for="brand">Brand</label>
                <input type="text" id="brand" name="Brand">
            </div>
            <div class="form-group">
                <label for="product-description">Description</label>
                <textarea id="product-description" name="Product_Description"></textarea>
            </div>
            <div class="form-actions">
                <button type="button" class="btn btn-secondary" onclick="closeModal()">Cancel</button>
                <button type="submit" class="btn btn-primary">Add Product</button>
            </div>
        </form>
    `;

    showModal(modalContent);

    // Populate hub dropdown
    const hubSelect = document.getElementById('inventory-hub');
    hubs.forEach(hub => {
        const option = document.createElement('option');
        option.value = hub.hub_id;
        option.textContent = `${hub.hub_name} (${hub.hub_id})`;
        hubSelect.appendChild(option);
    });

    // Handle form submission
    document.getElementById('inventory-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        await submitInventoryForm();
    });
}

async function submitInventoryForm() {
    const formData = new FormData(document.getElementById('inventory-form'));
    const data = Object.fromEntries(formData.entries());

    try {
        showLoading();
        await apiCall('/inventory_mangement/inventory/register', {
            method: 'POST',
            body: JSON.stringify(data)
        });
        
        showToast('Product added successfully', 'success');
        closeModal();
        await loadInventory();
        await loadDashboardStats();
        
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        hideLoading();
    }
}

function showDispatchForm() {
    const modalContent = `
        <div class="modal-header">
            <h2>Dispatch Inventory</h2>
            <button class="close-btn" onclick="closeModal()">&times;</button>
        </div>
        <form id="dispatch-form">
            <div class="form-group">
                <label for="dispatch-product-id">Product ID *</label>
                <input type="text" id="dispatch-product-id" name="Product_ID" required>
            </div>
            <div class="form-group">
                <label for="dispatch-quantity">Quantity *</label>
                <input type="number" id="dispatch-quantity" name="Quantity" min="1" required>
            </div>
            <div class="form-group">
                <label for="from-hub">From Hub *</label>
                <select id="from-hub" name="From_Hub_ID" required>
                    <option value="">Select Source Hub</option>
                </select>
            </div>
            <div class="form-group">
                <label for="to-hub">To Hub *</label>
                <select id="to-hub" name="To_Hub_ID" required>
                    <option value="">Select Destination Hub</option>
                </select>
            </div>
            <div class="form-group">
                <label for="request-ref">Request Reference</label>
                <input type="text" id="request-ref" name="Request_Ref">
            </div>
            <div class="form-actions">
                <button type="button" class="btn btn-secondary" onclick="closeModal()">Cancel</button>
                <button type="submit" class="btn btn-primary">Dispatch</button>
            </div>
        </form>
    `;

    showModal(modalContent);

    // Populate hub dropdowns
    const fromHubSelect = document.getElementById('from-hub');
    const toHubSelect = document.getElementById('to-hub');
    
    hubs.forEach(hub => {
        const fromOption = document.createElement('option');
        fromOption.value = hub.hub_id;
        fromOption.textContent = `${hub.hub_name} (${hub.hub_id})`;
        fromOption.setAttribute('data-hub-name', hub.hub_name);
        fromHubSelect.appendChild(fromOption);

        const toOption = document.createElement('option');
        toOption.value = hub.hub_id;
        toOption.textContent = `${hub.hub_name} (${hub.hub_id})`;
        toOption.setAttribute('data-hub-name', hub.hub_name);
        toHubSelect.appendChild(toOption);
    });

    // Handle form submission
    document.getElementById('dispatch-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        await submitDispatchForm();
    });
}

async function submitDispatchForm() {
    const formData = new FormData(document.getElementById('dispatch-form'));
    const data = Object.fromEntries(formData.entries());

    try {
        showLoading();
        
        // Get hub names from selected options
        const fromHubSelect = document.getElementById('from-hub');
        const toHubSelect = document.getElementById('to-hub');
        const fromHubName = fromHubSelect.selectedOptions[0]?.getAttribute('data-hub-name') || 'Unknown Hub';
        const toHubName = toHubSelect.selectedOptions[0]?.getAttribute('data-hub-name') || 'Unknown Hub';
        
        // Add dispatch to local database with proper data mapping
        const dispatchData = {
            Product_ID: data.Product_ID || 'N/A',
            Product_Name: data.Product_ID || 'Unknown Product', // Use Product_ID as name for now
            From_Hub_ID: data.From_Hub_ID || 'N/A',
            from_hub_name: fromHubName,
            To_Hub_ID: data.To_Hub_ID || 'N/A',
            to_hub_name: toHubName,
            Quantity: parseInt(data.Quantity) || 0,
            Vehicle_ID: null,
            Driver_ID: null,
            isTestDispatch: false
        };
        
        const newDispatch = addDispatchToDatabase(dispatchData);
        
        // Call backend API with original data structure
        await apiCall('/inventory_mangement/inventory/dispatch', {
            method: 'POST',
            body: JSON.stringify({
                Product_ID: data.Product_ID,
                Quantity: parseInt(data.Quantity),
                From_Hub_ID: data.From_Hub_ID,
                To_Hub_ID: data.To_Hub_ID,
                Request_Ref: data.Request_Ref || ''
            })
        });
        
        showToast('Inventory dispatched successfully', 'success');
        closeModal();
        await loadInventory();
        await loadDispatches();
        
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        hideLoading();
    }
}

function viewInventoryDetails(productId, hubId) {
    // Show detailed inventory information including batches
    const product = inventory.find(p => p.Product_ID === productId && p.Hub_ID === hubId);
    if (!product) {
        showToast('Product not found', 'error');
        return;
    }

    const modalContent = `
        <div class="modal-header">
            <h2><i class="fas fa-eye"></i> ${product.Product_Name} Details</h2>
            <button class="close-btn" onclick="closeModal()">&times;</button>
        </div>
        <div class="inventory-details">
            <div class="detail-section">
                <h3>Product Information</h3>
                <p><strong>Product ID:</strong> ${product.Product_ID}</p>
                <p><strong>Product Name:</strong> ${product.Product_Name}</p>
                <p><strong>Category:</strong> ${product.Category || 'N/A'}</p>
                <p><strong>Brand:</strong> ${product.Brand || 'N/A'}</p>
                <p><strong>Selling Price:</strong> ₹${product.Selling_Price || 'N/A'}</p>
                <p><strong>Description:</strong> ${product.Product_Description || 'N/A'}</p>
            </div>
            <div class="detail-section">
                <h3>Stock Information</h3>
                <p><strong>Hub:</strong> ${product.hub_name}</p>
                <p><strong>Total Quantity:</strong> ${product.Total_Quantity}</p>
                <p><strong>Nearest Expiry:</strong> ${product.Nearest_Expiry}</p>
            </div>
            <div id="batch-details">
                <h3>Batch Details</h3>
                <p>Loading batch information...</p>
            </div>
        </div>
        <div class="form-actions">
            <button class="btn btn-primary" onclick="closeModal()">Close</button>
        </div>
    `;

    showModal(modalContent);
    loadBatchDetails(productId, hubId);
}

async function loadBatchDetails(productId, hubId) {
    try {
        const data = await apiCall(`/inventory_mangement/inventory/batches?product_id=${productId}&hub_id=${hubId}`);
        const batchDiv = document.getElementById('batch-details');
        
        if (data && Array.isArray(data) && data.length > 0) {
            batchDiv.innerHTML = `
                <h3>Batch Details</h3>
                <div class="batch-list">
                    ${data.map(batch => `
                        <div class="batch-item">
                            <strong>Batch:</strong> ${batch.Batch_No}<br>
                            <strong>Quantity:</strong> ${batch.Quantity}<br>
                            <strong>Expiry:</strong> ${batch.Expiry_Date}<br>
                            <strong>Status:</strong> ${batch.Status}
                        </div>
                    `).join('')}
                </div>
            `;
        } else {
            batchDiv.innerHTML = '<h3>Batch Details</h3><p>No batch information available.</p>';
        }
    } catch (error) {
        document.getElementById('batch-details').innerHTML = '<h3>Batch Details</h3><p>Error loading batch information.</p>';
    }
}

function updateInventory(productId, hubId) {
    // Show form to add more inventory to existing product
    const product = inventory.find(p => p.Product_ID === productId && p.Hub_ID === hubId);
    if (!product) {
        showToast('Product not found', 'error');
        return;
    }

    const modalContent = `
        <div class="modal-header">
            <h2><i class="fas fa-plus"></i> Add Stock to ${product.Product_Name}</h2>
            <button class="close-btn" onclick="closeModal()">&times;</button>
        </div>
        <form id="update-inventory-form">
            <input type="hidden" name="Product_ID" value="${productId}">
            <input type="hidden" name="Hub_ID" value="${hubId}">
            
            <div class="form-group">
                <label for="update-quantity">Quantity to Add *</label>
                <input type="number" id="update-quantity" name="Quantity" min="1" required>
            </div>
            <div class="form-group">
                <label for="update-value">Purchase Value *</label>
                <input type="number" id="update-value" name="Value" step="0.01" min="0" required>
            </div>
            <div class="form-group">
                <label for="update-expiry-date">Expiry Date *</label>
                <input type="date" id="update-expiry-date" name="Expiry_Date" required>
            </div>
            <div class="form-group">
                <label for="update-batch-no">Batch Number (Optional)</label>
                <input type="text" id="update-batch-no" name="Batch_No">
            </div>
            <div class="form-actions">
                <button type="button" class="btn btn-secondary" onclick="closeModal()">Cancel</button>
                <button type="submit" class="btn btn-primary">Add Stock</button>
            </div>
        </form>
    `;

    showModal(modalContent);

    // Handle form submission
    document.getElementById('update-inventory-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        await submitUpdateInventoryForm();
    });
}

async function submitUpdateInventoryForm() {
    const formData = new FormData(document.getElementById('update-inventory-form'));
    const data = Object.fromEntries(formData.entries());

    try {
        showLoading();
        await apiCall('/inventory_mangement/inventory/update', {
            method: 'PUT',
            body: JSON.stringify(data)
        });
        
        showToast('Stock added successfully', 'success');
        closeModal();
        await loadInventory();
        await loadDashboardStats();
        
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        hideLoading();
    }
}

function showLowStockAlert() {
    // Create modal to show low stock items
    const modalContent = `
        <div class="modal-header">
            <h2><i class="fas fa-exclamation-triangle"></i> Low Stock Alert</h2>
            <button class="close-btn" onclick="closeModal()">&times;</button>
        </div>
        <div class="alert-content">
            <p>Items that need restocking:</p>
            <div id="low-stock-list">
                <p>Loading low stock items...</p>
            </div>
        </div>
        <div class="form-actions">
            <button class="btn btn-primary" onclick="closeModal()">Close</button>
        </div>
    `;
    
    showModal(modalContent);
    loadLowStockItems();
}

function showExpiringAlert() {
    // Create modal to show expiring items
    const modalContent = `
        <div class="modal-header">
            <h2><i class="fas fa-clock"></i> Expiring Soon Alert</h2>
            <button class="close-btn" onclick="closeModal()">&times;</button>
        </div>
        <div class="alert-content">
            <p>Items expiring within 30 days:</p>
            <div id="expiring-list">
                <p>Loading expiring items...</p>
            </div>
        </div>
        <div class="form-actions">
            <button class="btn btn-primary" onclick="closeModal()">Close</button>
        </div>
    `;
    
    showModal(modalContent);
    loadExpiringItems();
}

async function loadLowStockItems() {
    try {
        const data = await apiCall('/inventory_mangement/inventory/low-stock');
        const listDiv = document.getElementById('low-stock-list');
        
        if (data.low_stock && data.low_stock.length > 0) {
            listDiv.innerHTML = data.low_stock.map(item => `
                <div class="alert-item">
                    <strong>${item.Product_Name}</strong> (${item.Product_ID})<br>
                    <small>Hub: ${item.Hub_ID} | Quantity: ${item.Total_Quantity}</small>
                </div>
            `).join('');
        } else {
            listDiv.innerHTML = '<p style="color: green;">✅ No low stock items found!</p>';
        }
    } catch (error) {
        document.getElementById('low-stock-list').innerHTML = `<p style="color: red;">Error loading low stock items: ${error.message}</p>`;
    }
}

async function loadExpiringItems() {
    try {
        const data = await apiCall('/inventory_mangement/inventory/expiring-soon');
        const listDiv = document.getElementById('expiring-list');
        
        if (data.expiring_soon_items && data.expiring_soon_items.length > 0) {
            listDiv.innerHTML = data.expiring_soon_items.map(item => `
                <div class="alert-item">
                    <strong>${item.Product_Name}</strong> (${item.Product_ID})<br>
                    <small>Hub: ${item.Hub_ID} | Expires: ${item.Expiry_Date} | Quantity: ${item.Quantity}</small>
                </div>
            `).join('');
        } else {
            listDiv.innerHTML = '<p style="color: green;">✅ No items expiring within 30 days!</p>';
        }
    } catch (error) {
        document.getElementById('expiring-list').innerHTML = `<p style="color: red;">Error loading expiring items: ${error.message}</p>`;
    }
}

// Vehicle Management Functions
async function loadVehicles() {
    try {
        // Call the search endpoint without any parameters to get all vehicles
        const data = await apiCall('/vehicle_mangement/vehicles/search_vehicle');
        vehicles = data.Available_Vehicles || [];
        renderVehiclesTable();
        updateVehicleStats();
    } catch (error) {
        console.error('Error loading vehicles:', error);
        showToast('Error loading vehicles: ' + error.message, 'error');
    }
}

function renderVehiclesTable() {
    const tbody = document.getElementById('vehicles-tbody');
    if (!tbody) return;

    tbody.innerHTML = '';

    if (vehicles.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center">No vehicles found</td></tr>';
        return;
    }

    vehicles.forEach(vehicle => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${vehicle.Vehicle_ID}</td>
            <td>${vehicle.Vehicle_Number}</td>
            <td>${vehicle.Capacity}</td>
            <td><span class="status-badge ${vehicle.Status.toLowerCase().replace('-', '-')}">${vehicle.Status}</span></td>
            <td>
                <button class="btn btn-secondary" onclick="editVehicle('${vehicle.Vehicle_ID}')">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-danger" onclick="deleteVehicle('${vehicle.Vehicle_ID}', '${vehicle.Vehicle_Number}')">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function updateVehicleStats() {
    const available = vehicles.filter(v => v.Status === 'Available').length;
    const inTransit = vehicles.filter(v => v.Status === 'In-Transit').length;
    const maintenance = vehicles.filter(v => v.Status === 'Under-Maintenance').length;

    document.getElementById('available-vehicles').textContent = available;
    document.getElementById('in-transit-vehicles').textContent = inTransit;
    document.getElementById('maintenance-vehicles').textContent = maintenance;
}

function searchVehicles() {
    const searchTerm = document.getElementById('vehicle-search').value.toLowerCase();
    const statusFilter = document.getElementById('vehicle-status-filter').value;

    let filteredVehicles = vehicles.filter(vehicle => {
        const matchesSearch = !searchTerm || 
            vehicle.Vehicle_ID.toLowerCase().includes(searchTerm) ||
            vehicle.Vehicle_Number.toLowerCase().includes(searchTerm);
        
        const matchesStatus = !statusFilter || vehicle.Status === statusFilter;
        
        return matchesSearch && matchesStatus;
    });

    // Temporarily replace vehicles array for rendering
    const originalVehicles = vehicles;
    vehicles = filteredVehicles;
    renderVehiclesTable();
    vehicles = originalVehicles;
}

function showVehicleForm(vehicleId = null) {
    const isEdit = vehicleId !== null;
    const vehicle = isEdit ? vehicles.find(v => v.Vehicle_ID === vehicleId) : null;

    const modalContent = `
        <div class="modal-header">
            <h2>${isEdit ? 'Edit Vehicle' : 'Add New Vehicle'}</h2>
            <button class="close-btn" onclick="closeModal()">&times;</button>
        </div>
        <form id="vehicle-form">
            <div class="form-group">
                <label for="vehicle-id">Vehicle ID *</label>
                <input type="text" id="vehicle-id" name="Vehicle_ID" value="${vehicle?.Vehicle_ID || ''}" ${isEdit ? 'readonly' : 'required'}>
            </div>
            <div class="form-group">
                <label for="vehicle-number">Vehicle Number *</label>
                <input type="text" id="vehicle-number" name="Vehicle_Number" value="${vehicle?.Vehicle_Number || ''}" required>
            </div>
            <div class="form-group">
                <label for="capacity">Capacity *</label>
                <input type="number" id="capacity" name="Capacity" value="${vehicle?.Capacity || ''}" min="1" required>
            </div>
            ${isEdit ? `
            <div class="form-group">
                <label for="vehicle-status">Status</label>
                <select id="vehicle-status" name="Status">
                    <option value="Available" ${vehicle?.Status === 'Available' ? 'selected' : ''}>Available</option>
                    <option value="In-Transit" ${vehicle?.Status === 'In-Transit' ? 'selected' : ''}>In Transit</option>
                    <option value="Under-Maintenance" ${vehicle?.Status === 'Under-Maintenance' ? 'selected' : ''}>Under Maintenance</option>
                </select>
            </div>
            ` : ''}
            <div class="form-actions">
                <button type="button" class="btn btn-secondary" onclick="closeModal()">Cancel</button>
                <button type="submit" class="btn btn-primary">${isEdit ? 'Update' : 'Create'} Vehicle</button>
            </div>
        </form>
    `;

    showModal(modalContent);

    // Handle form submission
    document.getElementById('vehicle-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        await submitVehicleForm(isEdit, vehicleId);
    });
}

async function submitVehicleForm(isEdit, vehicleId) {
    const formData = new FormData(document.getElementById('vehicle-form'));
    const data = Object.fromEntries(formData.entries());

    try {
        showLoading();
        
        if (isEdit) {
            await apiCall('/vehicle_mangement/vehicles/update_vehicle', {
                method: 'PUT',
                body: JSON.stringify(data)
            });
            showToast('Vehicle updated successfully', 'success');
        } else {
            await apiCall('/vehicle_mangement/vehicles/register_vehicle', {
                method: 'POST',
                body: JSON.stringify(data)
            });
            showToast('Vehicle created successfully', 'success');
        }

        closeModal();
        await loadVehicles();
        await loadDashboardStats();
        
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        hideLoading();
    }
}

function editVehicle(vehicleId) {
    showVehicleForm(vehicleId);
}

async function deleteVehicle(vehicleId, vehicleNumber) {
    if (!confirm(`Are you sure you want to delete vehicle "${vehicleNumber}"?`)) {
        return;
    }

    try {
        showLoading();
        await apiCall('/vehicle_mangement/vehicles/delete_vehicle', {
            method: 'DELETE',
            body: JSON.stringify({
                Vehicle_ID: vehicleId,
                Vehicle_Number: vehicleNumber
            })
        });
        
        showToast('Vehicle deleted successfully', 'success');
        await loadVehicles();
        await loadDashboardStats();
        
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        hideLoading();
    }
}

// Driver Management Functions
async function loadDrivers() {
    try {
        // Call the search endpoint without any filters to get all drivers
        const data = await apiCall('/driver_mangement/drivers/search_driver?name=&license_number=&status=&hub_id=&limit=1000&skip=0');
        drivers = data || [];
        renderDriversTable();
        updateDriverStats();
    } catch (error) {
        console.error('Error loading drivers:', error);
        showToast('Error loading drivers: ' + error.message, 'error');
    }
}

function renderDriversTable() {
    const tbody = document.getElementById('drivers-tbody');
    if (!tbody) return;

    tbody.innerHTML = '';

    if (drivers.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center">No drivers found</td></tr>';
        return;
    }

    drivers.forEach(driver => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${driver.driver_id}</td>
            <td>${driver.name}</td>
            <td>${driver.age}</td>
            <td>${driver.license_number}</td>
            <td><span class="status-badge ${driver.status.toLowerCase()}">${driver.status}</span></td>
            <td>${driver.hub_id || 'N/A'}</td>
            <td>
                <button class="btn btn-secondary" onclick="editDriver('${driver.driver_id}')">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-danger" onclick="deleteDriver('${driver.driver_id}')">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function updateDriverStats() {
    const available = drivers.filter(d => d.status === 'active' || d.status === 'Available').length;
    const assigned = drivers.filter(d => d.status === 'Assigned').length;
    const retired = drivers.filter(d => d.status === 'retired' || d.status === 'Retired').length;

    document.getElementById('available-drivers').textContent = available;
    document.getElementById('assigned-drivers').textContent = assigned;
    document.getElementById('retired-drivers').textContent = retired;
}

function searchDrivers() {
    const searchTerm = document.getElementById('driver-search').value.toLowerCase();
    const statusFilter = document.getElementById('driver-status-filter').value;

    let filteredDrivers = drivers.filter(driver => {
        const matchesSearch = !searchTerm || 
            driver.driver_id.toLowerCase().includes(searchTerm) ||
            driver.name.toLowerCase().includes(searchTerm) ||
            driver.license_number.toLowerCase().includes(searchTerm);
        
        const matchesStatus = !statusFilter || driver.status === statusFilter;
        
        return matchesSearch && matchesStatus;
    });

    // Temporarily replace drivers array for rendering
    const originalDrivers = drivers;
    drivers = filteredDrivers;
    renderDriversTable();
    drivers = originalDrivers;
}

function showDriverForm(driverId = null) {
    const isEdit = driverId !== null;
    const driver = isEdit ? drivers.find(d => d.driver_id === driverId) : null;

    const modalContent = `
        <div class="modal-header">
            <h2>${isEdit ? 'Edit Driver' : 'Add New Driver'}</h2>
            <button class="close-btn" onclick="closeModal()">&times;</button>
        </div>
        <form id="driver-form">
            <div class="form-group">
                <label for="driver-name">Name *</label>
                <input type="text" id="driver-name" name="name" value="${driver?.name || ''}" required>
            </div>
            <div class="form-group">
                <label for="driver-age">Age *</label>
                <input type="number" id="driver-age" name="age" value="${driver?.age || ''}" min="18" max="50" required>
            </div>
            <div class="form-group">
                <label for="license-number">License Number *</label>
                <input type="text" id="license-number" name="license_number" value="${driver?.license_number || ''}" required>
            </div>
            <div class="form-group">
                <label for="driver-hub">Hub</label>
                <select id="driver-hub" name="hub_id">
                    <option value="">Select Hub</option>
                </select>
            </div>
            ${isEdit ? `
            <div class="form-group">
                <label for="driver-status">Status</label>
                <select id="driver-status" name="status">
                    <option value="Available" ${driver?.status === 'Available' ? 'selected' : ''}>Available</option>
                    <option value="Assigned" ${driver?.status === 'Assigned' ? 'selected' : ''}>Assigned</option>
                    <option value="On-Leave" ${driver?.status === 'On-Leave' ? 'selected' : ''}>On Leave</option>
                    <option value="Inactive" ${driver?.status === 'Inactive' ? 'selected' : ''}>Inactive</option>
                </select>
            </div>
            ` : ''}
            <div class="form-actions">
                <button type="button" class="btn btn-secondary" onclick="closeModal()">Cancel</button>
                <button type="submit" class="btn btn-primary">${isEdit ? 'Update' : 'Create'} Driver</button>
            </div>
        </form>
    `;

    showModal(modalContent);

    // Populate hub dropdown
    const hubSelect = document.getElementById('driver-hub');
    hubs.forEach(hub => {
        const option = document.createElement('option');
        option.value = hub.hub_id;
        option.textContent = `${hub.hub_name} (${hub.hub_id})`;
        if (driver && driver.hub_id === hub.hub_id) {
            option.selected = true;
        }
        hubSelect.appendChild(option);
    });

    // Handle form submission
    document.getElementById('driver-form').addEventListener('submit', async (e) => {
        e.preventDefault();
        await submitDriverForm(isEdit, driverId);
    });
}

async function submitDriverForm(isEdit, driverId) {
    const formData = new FormData(document.getElementById('driver-form'));
    const data = Object.fromEntries(formData.entries());

    if (isEdit) {
        data.driver_id = driverId;
    }

    try {
        showLoading();
        
        if (isEdit) {
            await apiCall('/driver_mangement/drivers/update_driver', {
                method: 'PUT',
                body: JSON.stringify(data)
            });
            showToast('Driver updated successfully', 'success');
        } else {
            await apiCall('/driver_mangement/drivers/register_driver', {
                method: 'POST',
                body: JSON.stringify(data)
            });
            showToast('Driver created successfully', 'success');
        }

        closeModal();
        await loadDrivers();
        await loadDashboardStats();
        
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        hideLoading();
    }
}

function editDriver(driverId) {
    showDriverForm(driverId);
}

async function deleteDriver(driverId) {
    if (!confirm(`Are you sure you want to delete this driver?`)) {
        return;
    }

    try {
        showLoading();
        await apiCall('/driver_mangement/drivers/delete_driver', {
            method: 'DELETE',
            body: JSON.stringify({
                driver_id: driverId
            })
        });
        
        showToast('Driver deleted successfully', 'success');
        await loadDrivers();
        await loadDashboardStats();
        
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        hideLoading();
    }
}

// Dispatch Management Functions
async function loadDispatches() {
    try {
        // Load dispatches from local database
        dispatches = getAllDispatches();
        renderDispatchesTable();
        updateDispatchStats();
        
        console.log('Loaded', dispatches.length, 'dispatches from database');
        
        if (dispatches.length === 0) {
            console.info('No dispatches found. Create a new dispatch to get started.');
        }
    } catch (error) {
        console.error('Error loading dispatches:', error);
        dispatches = [];
        renderDispatchesTable();
        updateDispatchStats();
    }
}

function renderDispatchesTable() {
    const tbody = document.getElementById('dispatch-tbody');
    if (!tbody) return;

    tbody.innerHTML = '';

    if (dispatches.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="9" class="text-center">
                    <div style="padding: 2rem; color: rgba(255, 255, 255, 0.8);">
                        <i class="fas fa-shipping-fast" style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;"></i>
                        <h3>No Dispatches Found</h3>
                        <p>To create a dispatch:</p>
                        <ol style="text-align: left; display: inline-block; margin: 1rem 0;">
                            <li>Go to <strong>Inventory</strong> page</li>
                            <li>Click <strong>"Dispatch"</strong> button</li>
                            <li>Select product, quantity, and destination hub</li>
                            <li>Dispatch will appear here automatically</li>
                        </ol>
                    </div>
                </td>
            </tr>
        `;
        return;
    }

    dispatches.forEach(dispatch => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${dispatch.id || 'N/A'}</td>
            <td>${dispatch.Product_Name || dispatch.Product_ID}</td>
            <td>${dispatch.from_hub_name || dispatch.From_Hub_ID}</td>
            <td>${dispatch.to_hub_name || dispatch.To_Hub_ID}</td>
            <td>${dispatch.Quantity || 0}</td>
            <td><span class="status-badge ${dispatch.status?.toLowerCase() || 'pending'}">${dispatch.status || 'Pending'}</span></td>
            <td>${dispatch.Vehicle_ID || 'Not Assigned'}</td>
            <td>${dispatch.Driver_ID || 'Not Assigned'}</td>
            <td>
                <button class="btn btn-secondary" onclick="viewDispatchDetails('${dispatch.id}')">
                    <i class="fas fa-eye"></i>
                </button>
                ${dispatch.status === 'In-Transit' ? `
                    <button class="btn btn-success" onclick="markDispatchReceived('${dispatch.id}')">
                        <i class="fas fa-check"></i>
                    </button>
                ` : ''}
            </td>
        `;
        tbody.appendChild(row);
    });
}

function updateDispatchStats() {
    const pending = dispatches.filter(d => d.status === 'Pending').length;
    const inTransit = dispatches.filter(d => d.status === 'In-Transit').length;
    const completed = dispatches.filter(d => d.status === 'Completed').length;

    console.log('Dispatch stats:', { pending, inTransit, completed, total: dispatches.length });
    console.log('All dispatches:', dispatches);

    document.getElementById('pending-dispatches').textContent = pending;
    document.getElementById('in-transit-dispatches').textContent = inTransit;
    document.getElementById('completed-dispatches').textContent = completed;
}

async function autoDispatch() {
    try {
        showLoading();
        
        // Get all pending dispatches
        const pendingDispatches = getDispatchesByStatus('Pending');
        
        if (pendingDispatches.length === 0) {
            showToast('No pending dispatches to process', 'info');
            return;
        }
        
        // Update all pending dispatches to In-Transit
        for (const dispatch of pendingDispatches) {
            updateDispatchStatus(dispatch.id, 'In-Transit', 'Auto Dispatch Started');
        }
        
        // Call backend auto dispatch
        const response = await apiCall('/vehicle_mangement/vehicles/dispatch_vehicle');
        
        showToast(`Auto dispatch completed: ${pendingDispatches.length} dispatches moved to In-Transit`, 'success');
        
        // Refresh dispatch data
        await loadDispatches();
        
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        hideLoading();
    }
}

function createTestDispatch() {
    // Create a unique sample dispatch for demonstration
    const timestamp = Date.now();
    const randomId = Math.random().toString(36).substr(2, 5);
    
    const testDispatchData = {
        Product_ID: `PROD_${timestamp}`,
        Product_Name: `Test Product ${randomId}`,
        From_Hub_ID: 'HUB_001',
        from_hub_name: 'Vijayawada Hub',
        To_Hub_ID: 'HUB_002',
        to_hub_name: 'Guntur Hub',
        Quantity: Math.floor(Math.random() * 100) + 10, // Random quantity 10-110
        Vehicle_ID: null,
        Driver_ID: null,
        isTestDispatch: true  // Mark as test dispatch
    };
    
    const newDispatch = addDispatchToDatabase(testDispatchData);
    dispatches = getAllDispatches();
    renderDispatchesTable();
    updateDispatchStats();
    showToast(`Test dispatch created: ${testDispatchData.Product_Name}`, 'success');
}

function viewDispatchDetails(dispatchId) {
    const dispatch = dispatches.find(d => d.id === dispatchId);
    if (!dispatch) {
        showToast('Dispatch not found', 'error');
        return;
    }

    const modalContent = `
        <div class="modal-header">
            <h2><i class="fas fa-shipping-fast"></i> Dispatch Details</h2>
            <button class="close-btn" onclick="closeModal()">&times;</button>
        </div>
        <div class="dispatch-details">
            <div class="detail-section">
                <h3>Dispatch Information</h3>
                <p><strong>Dispatch ID:</strong> ${dispatch.id}</p>
                <p><strong>Product:</strong> ${dispatch.Product_Name || dispatch.Product_ID}</p>
                <p><strong>Quantity:</strong> ${dispatch.Quantity}</p>
                <p><strong>Status:</strong> ${dispatch.status}</p>
            </div>
            <div class="detail-section">
                <h3>Route Information</h3>
                <p><strong>From Hub:</strong> ${dispatch.from_hub_name || dispatch.From_Hub_ID}</p>
                <p><strong>To Hub:</strong> ${dispatch.to_hub_name || dispatch.To_Hub_ID}</p>
                <p><strong>Vehicle:</strong> ${dispatch.Vehicle_ID || 'Not Assigned'}</p>
                <p><strong>Driver:</strong> ${dispatch.Driver_ID || 'Not Assigned'}</p>
            </div>
            <div class="detail-section">
                <h3>Timeline</h3>
                <p><strong>Created:</strong> ${dispatch.created_at || 'N/A'}</p>
                <p><strong>Updated:</strong> ${dispatch.updated_at || 'N/A'}</p>
            </div>
        </div>
        <div class="form-actions">
            <button class="btn btn-primary" onclick="closeModal()">Close</button>
        </div>
    `;

    showModal(modalContent);
}

async function markDispatchReceived(dispatchId) {
    if (!confirm('Mark this dispatch as received?')) {
        return;
    }

    try {
        showLoading();
        
        // Update dispatch status to Completed
        const updatedDispatch = updateDispatchStatus(dispatchId, 'Completed', 'Marked as Received');
        
        if (updatedDispatch) {
            showToast('Dispatch marked as received and completed', 'success');
            
            // Refresh dispatch data
            dispatches = getAllDispatches();
            renderDispatchesTable();
            updateDispatchStats();
        } else {
            showToast('Dispatch not found', 'error');
        }
        
    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        hideLoading();
    }
}

function showDispatchHistory() {
    const modalContent = `
        <div class="modal-header">
            <h2><i class="fas fa-history"></i> Dispatch History</h2>
            <button class="close-btn" onclick="closeModal()">&times;</button>
        </div>
        <div class="history-content">
            <div class="history-filters">
                <select id="history-status-filter">
                    <option value="">All Status</option>
                    <option value="Completed">Completed</option>
                    <option value="In-Transit">In Transit</option>
                    <option value="Pending">Pending</option>
                </select>
                <input type="date" id="history-date-from" placeholder="From Date">
                <input type="date" id="history-date-to" placeholder="To Date">
                <button class="btn btn-secondary" onclick="filterDispatchHistory()">Filter</button>
            </div>
            <div id="dispatch-history-list">
                <p>Loading dispatch history...</p>
            </div>
        </div>
        <div class="form-actions">
            <button class="btn btn-primary" onclick="closeModal()">Close</button>
        </div>
    `;

    showModal(modalContent);
    loadDispatchHistory();
}

async function loadDispatchHistory() {
    try {
        // Use current dispatches as history with proper status mapping
        const allDispatches = getAllDispatches();
        console.log('All dispatches for history:', allDispatches);
        
        const historyData = allDispatches.map(dispatch => ({
            ...dispatch,
            timestamp: dispatch.created_at || new Date().toISOString(),
            action: dispatch.status === 'Completed' ? 'Completed' : 
                   dispatch.status === 'In-Transit' ? 'In Transit' : 
                   dispatch.status === 'Pending' ? 'Pending' : 'Unknown'
        }));
        
        console.log('History data with status:', historyData);
        renderDispatchHistory(historyData);
    } catch (error) {
        document.getElementById('dispatch-history-list').innerHTML = '<p style="color: red;">Error loading dispatch history</p>';
    }
}

function renderDispatchHistory(historyData) {
    const listDiv = document.getElementById('dispatch-history-list');
    
    if (historyData.length === 0) {
        listDiv.innerHTML = '<p>No dispatch history found.</p>';
        return;
    }

    console.log('Rendering history with data:', historyData);

    listDiv.innerHTML = historyData.map(dispatch => {
        console.log('Dispatch status for rendering:', dispatch.status);
        return `
        <div class="history-item">
            <div class="history-header">
                <strong>${dispatch.Product_Name || dispatch.Product_ID}</strong>
                <span class="status-badge ${dispatch.status?.toLowerCase() || 'pending'}">${dispatch.status || 'Pending'}</span>
            </div>
            <div class="history-details">
                <p><strong>From:</strong> ${dispatch.from_hub_name || dispatch.From_Hub_ID} 
                   <strong>To:</strong> ${dispatch.to_hub_name || dispatch.To_Hub_ID}</p>
                <p><strong>Quantity:</strong> ${dispatch.Quantity} | 
                   <strong>Vehicle:</strong> ${dispatch.Vehicle_ID || 'N/A'} | 
                   <strong>Driver:</strong> ${dispatch.Driver_ID || 'N/A'}</p>
                <p><strong>Date:</strong> ${dispatch.created_at || 'N/A'}</p>
            </div>
        </div>
    `;
    }).join('');
}

function filterDispatchHistory() {
    // Implementation for filtering dispatch history
    showToast('Filter functionality coming soon', 'info');
}

// Modal Functions
function showModal(content) {
    const modalContainer = document.getElementById('modal-container');
    modalContainer.innerHTML = `
        <div class="modal" id="main-modal">
            <div class="modal-content">
                ${content}
            </div>
        </div>
    `;
    
    document.getElementById('main-modal').style.display = 'flex';
}

function closeModal() {
    const modal = document.getElementById('main-modal');
    if (modal) {
        modal.style.display = 'none';
    }
}

// Loading Functions
function showLoading() {
    document.getElementById('loading-overlay').classList.add('show');
}

function hideLoading() {
    document.getElementById('loading-overlay').classList.remove('show');
}

// Toast Notification Functions
function showToast(message, type = 'info') {
    const toastContainer = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icon = getToastIcon(type);
    toast.innerHTML = `
        <i class="${icon}"></i>
        <span>${message}</span>
    `;
    
    toastContainer.appendChild(toast);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (toast.parentNode) {
            toast.parentNode.removeChild(toast);
        }
    }, 5000);
}

function getToastIcon(type) {
    switch (type) {
        case 'success': return 'fas fa-check-circle';
        case 'error': return 'fas fa-exclamation-circle';
        case 'warning': return 'fas fa-exclamation-triangle';
        case 'info': return 'fas fa-info-circle';
        default: return 'fas fa-info-circle';
    }
}

// Utility Functions
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString();
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Global functions for onclick handlers
window.showPage = showPage;
window.showHubForm = showHubForm;
window.showInventoryForm = showInventoryForm;
window.showDispatchForm = showDispatchForm;
window.showVehicleForm = showVehicleForm;
window.showDriverForm = showDriverForm;
window.searchHubs = searchHubs;
window.filterHubs = filterHubs;
window.searchInventory = searchInventory;
window.searchVehicles = searchVehicles;
window.searchDrivers = searchDrivers;
window.editHub = editHub;
window.deleteHub = deleteHub;
window.editVehicle = editVehicle;
window.deleteVehicle = deleteVehicle;
window.editDriver = editDriver;
window.deleteDriver = deleteDriver;
window.autoDispatch = autoDispatch;
window.showLowStockAlert = showLowStockAlert;
window.showExpiringAlert = showExpiringAlert;
window.showDispatchHistory = showDispatchHistory;
window.viewDispatchDetails = viewDispatchDetails;
window.markDispatchReceived = markDispatchReceived;
window.viewInventoryDetails = viewInventoryDetails;
window.updateInventory = updateInventory;
window.loadDispatches = loadDispatches;
window.clearDispatchDatabase = clearDispatchDatabase;
window.clearAllDispatchRecords = clearAllDispatchRecords;
window.closeModal = closeModal;
