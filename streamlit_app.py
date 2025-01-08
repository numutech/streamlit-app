import streamlit as st
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

# Global PostgreSQL connection details
POSTGRES_CONFIG = {
    'host': 'localhost',
    'user': 'postgres',
    'password': 'admin',
    'port': 5432
}


def get_engine(database_name):
    """Create a SQLAlchemy engine for the selected database."""
    try:
        engine = create_engine(
            f"postgresql+psycopg2://{POSTGRES_CONFIG['user']}:{POSTGRES_CONFIG['password']}@{POSTGRES_CONFIG['host']}:{POSTGRES_CONFIG['port']}/{database_name}"
        )
        return engine
    except Exception as e:
        st.error(f"Error creating engine for database '{database_name}': {e}")
        return None


def get_available_databases():
    """Fetch the list of databases in PostgreSQL."""
    try:
        conn = psycopg2.connect(**POSTGRES_CONFIG, database="postgres")  # Connect to the default `postgres` database
        cur = conn.cursor()
        cur.execute("SELECT datname FROM pg_database WHERE datistemplate = false;")
        databases = [row[0] for row in cur.fetchall()]
        conn.close()
        return databases
    except Exception as e:
        st.error(f"Error fetching databases: {e}")
        return []


def sanitize_table_name(file_name):
    """Convert file name to a valid table name."""
    table_name = file_name.split('.')[0]  # Remove the file extension
    table_name = table_name.replace(" ", "_")  # Replace spaces with underscores
    table_name = table_name.lower()  # Convert to lowercase for consistency
    return table_name


def upload_dataframe_to_db(engine, table_name, dataframe):
    """Upload a Pandas DataFrame to the PostgreSQL database."""
    try:
        dataframe.to_sql(table_name, engine, if_exists='replace', index=False)
        st.success(f"Data uploaded successfully to table '{table_name}'.")
    except Exception as e:
        st.error(f"Error uploading data to table '{table_name}': {e}")


def fetch_table_structure(engine, table_name):
    """Fetch the structure (columns and data types) of a table."""
    query = f"""
    SELECT column_name, data_type 
    FROM information_schema.columns 
    WHERE table_name = '{table_name}';
    """
    try:
        with engine.connect() as connection:
            result = pd.read_sql(query, connection)
        return result
    except Exception as e:
        st.error(f"Error fetching structure for table '{table_name}': {e}")
        return None


# Streamlit UI
st.title("Upload CSV Files to PostgreSQL")

# Step 1: Select a database
databases = get_available_databases()
if databases:
    selected_db = st.selectbox("Select Database", databases)
else:
    st.warning("No databases found. Please check your PostgreSQL configuration.")
    st.stop()

# Step 2: Upload files
uploaded_files = st.file_uploader("Choose CSV file(s)", type=['csv'], accept_multiple_files=True)

if uploaded_files and selected_db:
    engine = get_engine(selected_db)
    if engine:
        for uploaded_file in uploaded_files:
            st.write(f"Processing file: {uploaded_file.name}")
            try:
                # Read the CSV file into a DataFrame
                dataframe = pd.read_csv(uploaded_file)
                st.dataframe(dataframe)

                # Generate sanitized table name
                table_name = sanitize_table_name(uploaded_file.name)

                # Upload DataFrame to the database
                upload_dataframe_to_db(engine, table_name, dataframe)

                # Fetch and display table structure
                table_structure = fetch_table_structure(engine, table_name)
                if table_structure is not None:
                    st.write(f"Table Structure for '{table_name}':")
                    st.dataframe(table_structure)
            except Exception as e:
                st.error(f"Error processing file {uploaded_file.name}: {e}")
