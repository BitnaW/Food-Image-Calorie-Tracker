# Project Structure Documentation

## Architecture Overview

The Food Image Calorie Tracker is built using clean architecture principles with clear separation of concerns across four main layers:

```
Calorie_Tracker/
├── main.py                 # Streamlit app entry point
├── pages/                  # UI Pages Layer (Presentation)
│   ├── 1_Login.py         # Authentication page
│   ├── 2_User_Info.py     # User profile page
│   └── 3_Log_Calories.py  # Calorie logging page
├── domain/                 # Domain Layer (Business Models)
│   ├── user.py            # User entity
│   ├── calorie_entry.py   # CalorieEntry entity
│   └── image_recognition_result.py  # ImageRecognitionResult entity
├── database/              # Data Access Layer
│   ├── connection.py      # Database connection management
│   └── schema.py          # Database schema definition
├── backend/               # Business Logic Layer
│   └── image_recognition.py  # Image processing services
└── utils/                 # Utilities
    ├── auth.py           # Authentication utilities
    └── session.py        # Session management
```

## Layer Descriptions

### 1. **Domain Layer** (`domain/`)
Contains pure business entities with no external dependencies.

**Files:**
- `user.py`: User entity with credentials and profile info
- `calorie_entry.py`: CalorieEntry entity representing logged meals
- `image_recognition_result.py`: ImageRecognitionResult and FoodItemDetection entities

**Purpose:** Define the core data structures that flow through the entire application.

### 2. **Database Layer** (`database/`)
Handles all database operations and schema management.

**Files:**
- `connection.py`: SQLite connection pool and query execution
- `schema.py`: Database schema definition with create table statements

**Purpose:** Abstract database operations so business logic doesn't depend on implementation details.

### 3. **Backend Layer** (`backend/`)
Contains business logic for image processing and calorie extraction.

**Files:**
- `image_recognition.py`: ImageProcessor, LabelRecognizer, VisualEstimator classes

**Purpose:** 
- LabelRecognizer: OCR-based extraction from nutritional labels
- VisualEstimator: ML-based calorie estimation from food images

### 4. **UI Pages** (`pages/`)
Streamlit pages for user interaction. Each page is a separate file automatically discovered by Streamlit.

**Files:**
- `1_Login.py`: User registration and authentication
- `2_User_Info.py`: User profile viewing and editing
- `3_Log_Calories.py`: Image upload and manual calorie entry

**Purpose:** Present user interfaces and collect user input.

### 5. **Utilities** (`utils/`)
Cross-cutting concerns used across multiple layers.

**Files:**
- `session.py`: Streamlit session state management for authentication
- `auth.py`: Password hashing, verification, and input validation

**Purpose:** Provide reusable utility functions.

## Data Flow

### User Login Flow
```
Login.py (UI) 
  → AuthValidator.validate_username/password
  → PasswordManager.verify_password
  → SessionManager.set_user
  → DatabaseConnection.fetch_one (from database)
```

### Calorie Logging Flow
```
Log_Calories.py (UI)
  → ImageProcessor.process_image
    → LabelRecognizer.recognize OR VisualEstimator.recognize
    → ImageRecognitionResult
  → CalorieEntry domain object created
  → DatabaseConnection.execute (save to database)
```

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Calories Table
```sql
CREATE TABLE calories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    calories REAL NOT NULL,
    food_name TEXT,
    food_type TEXT,
    quantity REAL,
    unit TEXT,
    source TEXT CHECK(source IN ('label', 'estimate')),
    image_path TEXT,
    notes TEXT,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

### Indexes
- `idx_calories_user_id`: Fast queries by user
- `idx_calories_logged_at`: Fast queries by date
- `idx_users_username`: Fast user lookup

## Design Patterns Used

1. **Singleton Pattern**: Database connection (`get_database()`)
2. **Strategy Pattern**: Image recognition strategies (LabelRecognizer, VisualEstimator)
3. **Session Pattern**: Streamlit session state for authentication
4. **Repository Pattern**: Database operations abstraction

## Extension Points

### Adding New Image Recognition Methods
1. Create new class inheriting from `ImageRecognizer` in `backend/image_recognition.py`
2. Implement `recognize()` method returning `ImageRecognitionResult`
3. Add to `ImageProcessor.process_image()` method

### Adding User Profile Fields
1. Add field to `User` dataclass in `domain/user.py`
2. Add column to `users` table in `database/schema.py`
3. Update `2_User_Info.py` page to display and edit new field

### Adding Calorie Entry Features
1. Add field to `CalorieEntry` dataclass in `domain/calorie_entry.py`
2. Add column to `calories` table in `database/schema.py`
3. Update `3_Log_Calories.py` page to accept and display new field

## Development Workflow

1. **Make changes to domain models** → Update database schema
2. **Implement business logic** → Add to backend layer
3. **Update UI pages** → Add forms or displays to pages
4. **Test end-to-end** → Run `streamlit run main.py` and verify flows

## TODO Implementation Guide

### Database Integration TODO
```python
# In pages/1_Login.py
def signup(username, email, password):
    user = User(username=username, email=email, password_hash=PasswordManager.hash_password(password))
    db = get_database()
    db.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", 
               (user.username, user.email, user.password_hash))
    # Return created user with id
```

### Image Recognition TODO
```python
# In backend/image_recognition.py
class LabelRecognizer(ImageRecognizer):
    def recognize(self, image_bytes):
        # Use pytesseract or Google Vision API
        extracted_calories = extract_calories_via_ocr(image_bytes)
        return ImageRecognitionResult(success=True, extracted_calories=extracted_calories, ...)
```

## Running the Application

```bash
cd Calorie_Tracker
pip install streamlit pillow
streamlit run main.py
```

Visit `http://localhost:8501` in your browser.
