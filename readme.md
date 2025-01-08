# Streamlit CSV to PostgreSQL Uploader

This Streamlit application allows users to upload CSV files and insert their contents into a PostgreSQL database. It dynamically creates tables based on the structure of the uploaded files and provides an interface to view table column names and data types.

---

## Features

- **Database Selection**: Choose from available PostgreSQL databases.
- **CSV Upload**: Upload one or multiple CSV files simultaneously.
- **Dynamic Table Creation**: Automatically creates or replaces tables based on the CSV structure.
- **Data Display**: Shows the uploaded CSV data in the application.
- **Table Structure Display**: Displays columns and data types of the created tables.

---

## Requirements

- Python 3.8+
- PostgreSQL database instance
- Required Python packages:
  - `streamlit`
  - `pandas`
  - `psycopg2-binary`
  - `sqlalchemy`

---

## Installation

1. Clone or download this repository.

2. Install the required Python packages:
   ```bash
   pip install streamlit pandas psycopg2-binary sqlalchemy
   ```

3. Update the PostgreSQL connection details in the code:
   ```python
   POSTGRES_CONFIG = {
       'host': 'localhost',
       'user': 'your_user',
       'password': 'your_password',
       'port': 5432
   }
   ```

---

## Usage

1. **Run the application**:
   ```bash
   streamlit run streamlit_app.py
   ```

2. **Open the application**:
   - Visit the URL provided by Streamlit (e.g., `http://localhost:8501`).

3. **Steps to use**:
   - Select a PostgreSQL database from the dropdown menu.
   - Upload one or more CSV files using the file uploader.
   - View the uploaded data and its structure (columns and data types) on the page.

---

## Code Overview

### Functions

1. **`get_engine(database_name)`**:
   - Creates a SQLAlchemy engine for connecting to the specified database.

2. **`get_available_databases()`**:
   - Retrieves the list of available PostgreSQL databases.

3. **`sanitize_table_name(file_name)`**:
   - Converts a file name into a valid table name (removing extensions, replacing spaces with underscores, converting to lowercase).

4. **`upload_dataframe_to_db(engine, table_name, dataframe)`**:
   - Uploads a Pandas DataFrame to the PostgreSQL database.

5. **`fetch_table_structure(engine, table_name)`**:
   - Fetches the structure (columns and data types) of a PostgreSQL table.

### User Interface

- **Database Selection**: Dropdown to select the target database.
- **CSV File Uploader**: File uploader supporting multiple files.
- **Table Display**: Data preview and table structure (columns and data types).

---

## Example Workflow

1. Select the `my_database` from the dropdown menu.
2. Upload `example_data.csv`.
3. The application:
   - Displays the CSV data.
   - Creates a table (e.g., `example_data`) in the selected database.
   - Shows the table structure:
     | Column Name | Data Type |
     |-------------|-----------|
     | id          | integer   |
     | name        | text      |
     | age         | integer   |

---

## Customization

- Modify the `POSTGRES_CONFIG` dictionary to match your PostgreSQL credentials.
- Adjust the `sanitize_table_name` function for different table naming conventions.
- Change `if_exists='replace'` in the `to_sql` method to `append` to avoid replacing existing tables.

---

## Troubleshooting

- **Error: "No databases found"**:
  - Ensure PostgreSQL is running and accessible.
  - Verify the `POSTGRES_CONFIG` credentials.

- **Error: "Error uploading data"**:
  - Check that the uploaded CSV matches the table structure if using `if_exists='append'`.

---

## Future Enhancements

- Add user authentication for database security.
- Provide options to select `if_exists` behavior (`replace`, `append`, etc.).
- Allow users to query and view data directly from the application.

---

## License

This project is licensed under the MIT License.


