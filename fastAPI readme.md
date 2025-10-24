# Traveloggia FastAPI

FastAPI Python framework - rewrite of 15 year old ASP.NET Web API services

## Quick Start

### Prerequisites
- Python 3.14+ 
- SQL Server database access

### Setup & Run Local Development Server

1. **Activate virtual environment:**
   ```bash
   venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure database connection:**
   - Update `.env` file with your SQL Server connection string
   ```
   DATABASE_URL=mssql+pyodbc://username:password@server/database?driver=ODBC+Driver+17+for+SQL+Server
   ```

4. **Run the FastAPI development server:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the API:**
   - **API Base URL:** http://localhost:8000
   - **Interactive Docs:** http://localhost:8000/docs
   - **Health Check:** http://localhost:8000/health

### Production Deployment

**Vercel:** Automatically deploys from `master` branch
- **Production URL:** https://traveloggia-fastapi.vercel.app
- **API Docs:** https://traveloggia-fastapi.vercel.app/docs

### API Endpoints

#### Authentication
- `POST /ValidateMember` - Member login validation

#### Maps & Travel Data
- `GET /api/Maps/{id}` - Get latest map for member
- `GET /api/MapList/{id}` - Get all maps for member
- `GET /api/SelectMap/{id}` - Get specific map by ID

#### Sites (Locations)
- `GET /api/SiteList/{id}` - Get sites for a map
- `GET /api/ScheduledSites/{id}` - Get scheduled sites
- `POST /api/Sites` - Create new site
- `PUT /api/Sites/{id}` - Update site
- `DELETE /api/Sites/{id}` - Delete site (soft delete)

#### Photos
- `GET /api/Photos/{id}` - Get photos for site
- `POST /api/Photos` - Upload new photo
- `PUT /api/Photos/{id}` - Update photo
- `DELETE /api/Photos/{id}` - Delete photo

#### Journals
- `GET /api/Journals/{id}` - Get journals for site
- `POST /api/Journals` - Create journal entry
- `PUT /api/Journals/{id}` - Update journal
- `DELETE /api/Journals/{id}` - Delete journal

#### Devices
- `GET /api/Devices` - Get all devices
- `POST /api/Devices` - Register new device
- `PUT /api/Devices/{id}` - Update device
- `DELETE /api/Devices/{id}` - Remove device

### Migration Notes

This FastAPI rewrite replaces legacy ASP.NET Web API services with:
- ✅ Modern Python FastAPI framework
- ✅ SQLAlchemy ORM for database operations  
- ✅ Pydantic schemas for request/response validation
- ✅ Automatic OpenAPI documentation
- ✅ CORS support for web clients
- ✅ Modern async/await patterns

**Backup:** Original endpoints preserved in `main.bak.py`

### postgresql://postgres:RKgkSkUNjzSzZKhHCvgJfHWbjHgkDSua@metro.proxy.rlwy.net:17197/railway
