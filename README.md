------------------------------------------------------------------------
Python Project File Structure
------------------------------------------------------------------------
DRS_Python_Backend/
        ├── openApi/
        │      ├── routes/                              # Define API routes
        │      │      ├── intern_routes.py              # Routes for intern API
        │      │      
        │      ├── controllers/                         # Define API endpoints 
        │      ├── models/                              # Define data models for the API 
        │      │      ├── models.py                     # General models
        │      │      ├── student.py                    # Student model
        │      │      ├── intern.py                     # Intern model
        │      ├── services/                            # API logic
        │      │      ├── intern_service.py             # Service for intern API
        │      │      
        │
        ├── logger/
        │      ├── log_config.py                        # Logger configuration
        │      ├── log_manager.py                       # Utility functions for logging
        │      ├── custom_handler.py                    # Custom log handler
        │
        ├── process_logic/
        │      ├──                                      # Process logic files
        │
        ├── tests/
        │      ├── test_api.py                          # Test cases for API endpoints
        │      ├── test_database.py                     # Test cases for database interactions
        │      ├── test_logger.py                       # Test cases for logger
        │      ├── test_process_logic.py                # Test cases for process logic
        │
        ├── utils/
        │      ├── database/
        │      │        ├── db_config.py                # Database connection setup
        │      │        ├── migrations/                 # For database migrations
        │      │              └── (migration scripts)
        │      │
        │      ├── email/
        │
        ├── main.py                                     # Entry point of the application
        ├── requirements.txt                            # Dependencies
        ├── README.md                                   # Project documentation
        ├── .env                                        # Environment variables (gitignored)
        ├── .gitignore                                  # Files/folders to ignore in version control
