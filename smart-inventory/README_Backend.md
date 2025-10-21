# Smart Inventory & Dispatch Management - Backend API

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Server
```bash
# Option 1: Using the startup script
python start_backend.py

# Option 2: Direct uvicorn command
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Option 3: Using Python module
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Access the API
- **API Base URL**: `http://localhost:8000`
- **Interactive Docs**: `http://localhost:8000/docs`
- **Health Check**: `http://localhost:8000/health`

## 📚 API Endpoints

### Hub Management
- `GET /api/hub_mangement/hubs/search` - Search hubs
- `POST /api/hub_mangement/hubs/register` - Register new hub
- `PUT /api/hub_mangement/hubs/update/{hub_id}` - Update hub
- `DELETE /api/hub_mangement/hubs/delete/{hub_id}` - Delete hub
- `GET /api/hub_mangement/hubs/status?status=Active` - Get hubs by status

### Inventory Management
- `GET /api/inventory_mangement/inventory/products` - Get products
- `POST /api/inventory_mangement/inventory/register` - Register product
- `PUT /api/inventory_mangement/inventory/update` - Update product
- `POST /api/inventory_mangement/inventory/dispatch` - Dispatch inventory
- `GET /api/inventory_mangement/inventory/low-stock` - Get low stock items
- `GET /api/inventory_mangement/inventory/expiring-soon` - Get expiring items

### Driver Management
- `GET /api/driver_mangement/drivers/search_driver` - Search drivers
- `POST /api/driver_mangement/drivers/register_driver` - Register driver
- `PUT /api/driver_mangement/drivers/update_driver` - Update driver
- `DELETE /api/driver_mangement/drivers/delete_driver` - Delete driver

### Vehicle Management
- `GET /api/vehicle_mangement/vehicles/search_vehicle` - Search vehicles
- `POST /api/vehicle_mangement/vehicles/register_vehicle` - Register vehicle
- `PUT /api/vehicle_mangement/vehicles/update_vehicle` - Update vehicle
- `DELETE /api/vehicle_mangement/vehicles/delete_vehicle` - Delete vehicle
- `POST /api/vehicle_mangement/vehicles/dispatch_vehicle` - Auto dispatch

### Vehicle Inventory & Dispatch
- `GET /api/vehicle_inventory/dispatches` - Get dispatches
- `POST /api/vehicle_inventory/auto_assign/{dispatch_id}` - Auto assign dispatch
- `PUT /api/vehicle_inventory/mark_dispatch_received` - Mark dispatch received

## 🧪 Testing with Postman

### 1. Import Collection
- Use the provided `smart-inventory.postman_collection.json` file
- Import it into Postman

### 2. Test Basic Endpoints
```bash
# Health Check
GET http://localhost:8000/health

# API Root
GET http://localhost:8000/api

# Get all hubs
GET http://localhost:8000/api/hub_mangement/hubs/search

# Get active hubs
GET http://localhost:8000/api/hub_mangement/hubs/status?status=Active
```

### 3. Test with Sample Data
```bash
# Register a new hub
POST http://localhost:8000/api/hub_mangement/hubs/register
Content-Type: application/json

{
  "hub_id": "HUB_TEST_001",
  "hub_name": "Test Hub",
  "hub_manager": "John Doe",
  "hub_phone_number": "1234567890",
  "hub_address": "123 Test Street, Test City",
  "status": "Active"
}
```

## 🗄️ Database

- **MongoDB**: Connected to MongoDB Atlas
- **Database**: `smart_inventory_db`
- **Collections**: Hubs, InventoryProducts, InventoryBatches, StockTransactions, Dispatches, drivers, vehicles

## 🔧 Configuration

- **MongoDB URI**: Configured in `app/core/config.py`
- **CORS**: Enabled for all origins (configure for production)
- **Logging**: Configured in `app/utiles/logger.py`

## 📁 Project Structure

```
smart-inventory/
├── main.py                          # FastAPI application entry point
├── start_backend.py                 # Server startup script
├── requirements.txt                 # Python dependencies
├── app/
│   ├── core/
│   │   └── config.py               # Configuration settings
│   ├── db/
│   │   └── mongodb.py              # Database connection
│   ├── endpoints/                  # API endpoint routers
│   ├── models/                     # Pydantic models
│   ├── services/                   # Business logic
│   └── utiles/                     # Utilities and helpers
└── README_Backend.md               # This file
```

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Failed**
   - Check MongoDB URI in `app/core/config.py`
   - Ensure MongoDB Atlas cluster is accessible

2. **Port Already in Use**
   - Change port in `start_backend.py` or use `--port 8001`

3. **Module Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python path and virtual environment

### Logs
- Server logs are displayed in the terminal
- Database connection status is shown on startup
- API requests are logged automatically

## 🔒 Security Notes

- CORS is currently set to allow all origins (`*`)
- In production, specify your frontend domain
- MongoDB credentials are in the code (move to environment variables for production)
- Add authentication/authorization as needed

## 📈 Performance

- Uses async/await for non-blocking operations
- MongoDB indexes are created automatically
- FastAPI provides automatic API documentation
- Built-in request validation with Pydantic
