-- Deploy Sample Streamlit Apps
-- This script creates multiple simple Streamlit apps to showcase the landing page functionality

-- =============================================================================
-- SETUP: Use the same schema as the landing page
-- =============================================================================

USE ROLE ACCOUNTADMIN;
USE SCHEMA STREAMLIT_APPS.LANDING_PAGE;

-- Verify we're in the right place
SELECT CURRENT_DATABASE(), CURRENT_SCHEMA();

-- =============================================================================
-- STEP 1: Upload all app files to the stage
-- =============================================================================

-- List current stage contents
LIST @app_stage;

-- Upload the sample app files using PUT command (run these from SnowSQL or similar)
-- Replace '/path/to/your/' with your actual file path

/*
PUT file:///path/to/your/simple_data_explorer.py @app_stage overwrite=true;
PUT file:///path/to/your/simple_calculator.py @app_stage overwrite=true;
PUT file:///path/to/your/simple_chart_maker.py @app_stage overwrite=true;
PUT file:///path/to/your/simple_survey_form.py @app_stage overwrite=true;
PUT file:///path/to/your/simple_text_analyzer.py @app_stage overwrite=true;
*/

-- Alternative: Use Snowsight UI to upload files to @app_stage

-- Verify all files are uploaded
LIST @app_stage;

-- =============================================================================
-- STEP 2: Create Sample Streamlit Apps
-- =============================================================================

-- 1. Data Explorer App
CREATE OR REPLACE STREAMLIT simple_data_explorer
ROOT_LOCATION = '@app_stage'
MAIN_FILE = 'simple_data_explorer.py'
QUERY_WAREHOUSE = 'COMPUTE_WH'  -- Replace with your warehouse name
COMMENT = 'Simple data explorer with filtering and basic metrics';

-- 2. Calculator App  
CREATE OR REPLACE STREAMLIT simple_calculator
ROOT_LOCATION = '@app_stage'
MAIN_FILE = 'simple_calculator.py'
QUERY_WAREHOUSE = 'COMPUTE_WH'  -- Replace with your warehouse name
COMMENT = 'Basic calculator with standard mathematical operations';

-- 3. Chart Maker App
CREATE OR REPLACE STREAMLIT simple_chart_maker
ROOT_LOCATION = '@app_stage'
MAIN_FILE = 'simple_chart_maker.py'
QUERY_WAREHOUSE = 'COMPUTE_WH'  -- Replace with your warehouse name
COMMENT = 'Create simple charts (bar, line, area) with sample data';

-- 4. Survey Form App
CREATE OR REPLACE STREAMLIT simple_survey_form
ROOT_LOCATION = '@app_stage'
MAIN_FILE = 'simple_survey_form.py'  
QUERY_WAREHOUSE = 'COMPUTE_WH'  -- Replace with your warehouse name
COMMENT = 'Sample survey form with validation and various input types';

-- 5. Text Analyzer App
CREATE OR REPLACE STREAMLIT simple_text_analyzer
ROOT_LOCATION = '@app_stage'
MAIN_FILE = 'simple_text_analyzer.py'
QUERY_WAREHOUSE = 'COMPUTE_WH'  -- Replace with your warehouse name
COMMENT = 'Analyze text with statistics, word frequency, and reading time estimates';

-- =============================================================================
-- STEP 3: Grant Required Privileges
-- =============================================================================

-- Grant READ SESSION privilege (if not already done)
GRANT READ SESSION ON ACCOUNT TO ROLE ACCOUNTADMIN;

-- Grant access to SNOWFLAKE database for system views (if not already done)
GRANT USAGE ON DATABASE SNOWFLAKE TO ROLE ACCOUNTADMIN;

-- =============================================================================
-- STEP 4: Grant Access to Users/Roles
-- =============================================================================

-- Grant usage on all sample apps to appropriate roles
-- Modify these grants based on your organization's role structure

-- Example: Grant to analyst role
-- GRANT USAGE ON STREAMLIT simple_data_explorer TO ROLE ANALYST_ROLE;
-- GRANT USAGE ON STREAMLIT simple_calculator TO ROLE ANALYST_ROLE;
-- GRANT USAGE ON STREAMLIT simple_chart_maker TO ROLE ANALYST_ROLE;
-- GRANT USAGE ON STREAMLIT simple_survey_form TO ROLE ANALYST_ROLE;
-- GRANT USAGE ON STREAMLIT simple_text_analyzer TO ROLE ANALYST_ROLE;

-- Example: Grant to all users (use carefully)
-- GRANT USAGE ON STREAMLIT simple_data_explorer TO ROLE PUBLIC;
-- GRANT USAGE ON STREAMLIT simple_calculator TO ROLE PUBLIC;
-- GRANT USAGE ON STREAMLIT simple_chart_maker TO ROLE PUBLIC;
-- GRANT USAGE ON STREAMLIT simple_survey_form TO ROLE PUBLIC;
-- GRANT USAGE ON STREAMLIT simple_text_analyzer TO ROLE PUBLIC;

-- =============================================================================
-- STEP 5: Verification
-- =============================================================================

-- List all Streamlit apps in the schema
SHOW STREAMLITS IN SCHEMA STREAMLIT_APPS.LANDING_PAGE;

-- Get URLs for all apps
SELECT 
    name as app_name,
    url_id,
    'https://' || CURRENT_ACCOUNT() || '.snowflakecomputing.com/streamlit/' || url_id as app_url,
    owner,
    comment
FROM SNOWFLAKE.INFORMATION_SCHEMA.STREAMLITS 
WHERE database_name = 'STREAMLIT_APPS' 
  AND schema_name = 'LANDING_PAGE'
ORDER BY name;

-- Check grants on the apps
SELECT * FROM SNOWFLAKE.INFORMATION_SCHEMA.TABLE_PRIVILEGES 
WHERE table_schema = 'LANDING_PAGE'
  AND table_name IN (
    'SIMPLE_DATA_EXPLORER',
    'SIMPLE_CALCULATOR', 
    'SIMPLE_CHART_MAKER',
    'SIMPLE_SURVEY_FORM',
    'SIMPLE_TEXT_ANALYZER',
    'STREAMLIT_LANDING_PAGE'
  );

-- =============================================================================
-- STEP 6: Test Your Landing Page
-- =============================================================================

-- Now launch your streamlit_landing_page app
-- It should show all the sample apps you just created!

-- =============================================================================
-- SAMPLE APP DESCRIPTIONS
-- =============================================================================

/*
Your landing page will now show these apps:

1. 📊 Simple Data Explorer
   - Shows sample sales data with filtering
   - Basic metrics and data table
   - Demonstrates data manipulation

2. 🧮 Simple Calculator  
   - Basic mathematical operations
   - Input validation
   - Quick calculation shortcuts

3. 📈 Simple Chart Maker
   - Create bar, line, and area charts
   - Sample data generation
   - Chart customization options

4. 📝 Simple Survey Form
   - Various input types (text, select, slider, checkbox)
   - Form validation
   - Results summary display

5. 📝 Simple Text Analyzer
   - Text statistics and analysis
   - Word frequency analysis  
   - Reading time estimates
   - Complexity indicators
*/

-- =============================================================================
-- CLEANUP (if needed)
-- =============================================================================

-- To remove all sample apps if needed:
/*
DROP STREAMLIT IF EXISTS simple_data_explorer;
DROP STREAMLIT IF EXISTS simple_calculator;
DROP STREAMLIT IF EXISTS simple_chart_maker;
DROP STREAMLIT IF EXISTS simple_survey_form; 
DROP STREAMLIT IF EXISTS simple_text_analyzer;
*/

-- =============================================================================
-- DEPLOYMENT CHECKLIST FOR SAMPLE APPS
-- =============================================================================

/*
□ 1. All 5 sample app files uploaded to @app_stage
□ 2. All 5 Streamlit apps created successfully  
□ 3. Warehouse name updated in all CREATE STREAMLIT statements
□ 4. READ SESSION privilege granted (for user context functions)
□ 5. SNOWFLAKE database access granted (for system views)
□ 6. Appropriate usage grants given to users/roles
□ 7. All app URLs retrieved and accessible
□ 8. Landing page tested and shows all sample apps
□ 9. Individual sample apps tested and working
□ 10. Users can navigate between apps successfully
*/



