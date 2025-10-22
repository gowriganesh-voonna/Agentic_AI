## Smart Inventory Frontend

### Run
- Start backend: http://localhost:8000
- Open this file: `frontend/index.html` in your browser (no build step).

### Configure
If your API runs elsewhere, edit `frontend/script.js` and set:

```
const API_BASE_URL = 'http://localhost:8000/api';
```

### Features
- Dashboard stats (active hubs, low stock, expiring soon)
- Hub management: search, filter by status, create, update, delete
- Inventory: register product, update stock, dispatch, search
- Drivers: register, update, delete, search
- Vehicles: register, update, delete, search, auto-dispatch trigger
- Dispatches: list, auto-assign, mark received

### Notes
- This is a pure HTML/CSS/JS SPA; keep the backend CORS open to allow requests from file:// origin.

