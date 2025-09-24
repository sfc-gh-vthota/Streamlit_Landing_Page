-- Streamlit Landing Page Deployment Script
-- This script creates and deploys the Streamlit landing page application

-- =============================================================================
-- STEP 1: Setup Database and Schema (Optional - modify as needed)
-- =============================================================================
use role accountadmin;
-- Create database for Streamlit applications (if it doesn't exist)
CREATE DATABASE IF NOT EXISTS STREAMLIT_APPS;

-- Create schema for the landing page
CREATE SCHEMA IF NOT EXISTS STREAMLIT_APPS.LANDING_PAGE;

-- Use the created schema
USE SCHEMA STREAMLIT_APPS.LANDING_PAGE;

-- =============================================================================
-- STEP 2: Create Stage for Application Files
-- =============================================================================

-- Create a stage to hold the Streamlit application files
CREATE STAGE IF NOT EXISTS app_stage
COMMENT = 'Stage for Streamlit Landing Page application files';

-- =============================================================================
-- STEP 3: Upload Files to Stage
-- =============================================================================

-- Upload the main application file
-- Note: You need to run these PUT commands from SnowSQL or a tool that supports file upload
-- PUT file:///path/to/your/streamlit_landing_page.py @app_stage overwrite=true;
-- PUT file:///path/to/your/requirements.txt @app_stage overwrite=true;

-- You can also use Snowsight UI to upload files to the stage

-- Verify files are uploaded correctly
LIST @app_stage;

-- =============================================================================
-- STEP 4: Create the Streamlit Application
-- =============================================================================

-- Create the Streamlit application
CREATE OR REPLACE STREAMLIT streamlit_landing_page
ROOT_LOCATION = '@app_stage'
MAIN_FILE = 'streamlit_landing_page.py'
QUERY_WAREHOUSE = 'COMPUTE_WH'  -- Replace with your warehouse name
COMMENT = 'Landing page showing user-accessible Streamlit applications';

-- =============================================================================
-- STEP 5: Grant Required Privileges (REQUIRED for proper functionality)
-- =============================================================================

-- CRITICAL: Grant READ SESSION privilege to the role that owns the Streamlit app
-- This is required for CURRENT_USER(), CURRENT_ROLE(), and other context functions to work
GRANT READ SESSION ON ACCOUNT TO ROLE ACCOUNTADMIN;

-- IMPORTANT: Grant access to SNOWFLAKE database for system views
-- This allows querying INFORMATION_SCHEMA.STREAMLITS and other system views
GRANT USAGE ON DATABASE SNOWFLAKE TO ROLE ACCOUNTADMIN;

-- If you're using a different role to own the Streamlit app, grant to that role instead:
-- GRANT READ SESSION ON ACCOUNT TO ROLE <your_streamlit_owner_role>;
-- GRANT USAGE ON DATABASE SNOWFLAKE TO ROLE <your_streamlit_owner_role>;

-- =============================================================================
-- STEP 6: Grant Access to Users/Roles  
-- =============================================================================

-- Grant usage on the Streamlit app to specific roles
-- Modify these grants based on your organization's role structure

-- Example: Grant to a general analyst role
-- GRANT USAGE ON STREAMLIT streamlit_landing_page TO ROLE ANALYST_ROLE;

-- Example: Grant to multiple roles
-- GRANT USAGE ON STREAMLIT streamlit_landing_page TO ROLE DATA_SCIENTIST_ROLE;
-- GRANT USAGE ON STREAMLIT streamlit_landing_page TO ROLE BUSINESS_ANALYST_ROLE;
-- GRANT USAGE ON STREAMLIT streamlit_landing_page TO ROLE MANAGER_ROLE;

-- Example: Grant to all users (use carefully)
-- GRANT USAGE ON STREAMLIT streamlit_landing_page TO ROLE PUBLIC;

-- =============================================================================
-- STEP 6: Verification and Testing
-- =============================================================================

-- Check if the Streamlit app was created successfully
SHOW STREAMLITS IN SCHEMA STREAMLIT_APPS.LANDING_PAGE;

-- Get the URL to access your Streamlit app
SELECT 
    name as app_name,
    url_id,
    'https://' || CURRENT_ACCOUNT() || '.snowflakecomputing.com/streamlit/' || url_id as app_url,
    owner,
    comment
FROM SNOWFLAKE.INFORMATION_SCHEMA.STREAMLITS 
WHERE name = 'STREAMLIT_LANDING_PAGE';

-- =============================================================================
-- STEP 7: Optional - Create Sample Streamlit Apps for Testing
-- =============================================================================

-- If you want to test the landing page with sample apps, you can create them:

-- Sample App 1: Sales Dashboard
/*
CREATE OR REPLACE STREAMLIT sample_sales_dashboard
ROOT_LOCATION = '@app_stage'  -- You'd need to upload a sample app file
MAIN_FILE = 'sample_sales_dashboard.py'
QUERY_WAREHOUSE = 'COMPUTE_WH'
COMMENT = 'Sample sales analytics and reporting dashboard with regional breakdowns';
*/

-- Sample App 2: Customer Analytics
/*
CREATE OR REPLACE STREAMLIT sample_customer_analytics
ROOT_LOCATION = '@app_stage'  -- You'd need to upload a sample app file
MAIN_FILE = 'sample_customer_analytics.py'
QUERY_WAREHOUSE = 'COMPUTE_WH'
COMMENT = 'Sample customer behavior analysis, segmentation, and campaign performance tracking';
*/

-- =============================================================================
-- STEP 8: Useful Queries for Management
-- =============================================================================

-- List all Streamlit apps in your account
SELECT * FROM SNOWFLAKE.INFORMATION_SCHEMA.STREAMLITS ORDER BY created_on DESC;

-- Check privileges on the landing page app
SELECT * FROM SNOWFLAKE.INFORMATION_SCHEMA.TABLE_PRIVILEGES 
WHERE table_name = 'STREAMLIT_LANDING_PAGE';

-- Monitor usage (if query history is available)
SELECT 
    query_text,
    user_name,
    role_name,
    warehouse_name,
    start_time,
    end_time,
    total_elapsed_time
FROM SNOWFLAKE.INFORMATION_SCHEMA.QUERY_HISTORY 
WHERE query_text ILIKE '%streamlit_landing_page%'
ORDER BY start_time DESC
LIMIT 100;

-- =============================================================================
-- TROUBLESHOOTING
-- =============================================================================

-- COMMON ISSUE 1: KeyError: 'username' or context function errors
-- SOLUTION: Grant READ SESSION privilege to the Streamlit app owner role
-- USE ROLE ACCOUNTADMIN;
-- GRANT READ SESSION ON ACCOUNT TO ROLE <streamlit_owner_role>;

-- COMMON ISSUE 2: "Object 'SNOWFLAKE.INFORMATION_SCHEMA.STREAMLITS' does not exist or not authorized"
-- SOLUTION: Grant access to SNOWFLAKE database for system views
-- USE ROLE ACCOUNTADMIN;
-- GRANT USAGE ON DATABASE SNOWFLAKE TO ROLE <streamlit_owner_role>;

-- If you need to update the app, you can:
-- 1. Upload new files to the stage
-- 2. Recreate the Streamlit app with CREATE OR REPLACE

-- To delete the app if needed:
-- DROP STREAMLIT IF EXISTS streamlit_landing_page;

-- To check stage contents:
-- LIST @app_stage;

-- To remove files from stage:
-- REMOVE @app_stage/streamlit_landing_page.py;

-- To verify READ SESSION privilege:
-- SHOW GRANTS ON ACCOUNT;

-- =============================================================================
-- DEPLOYMENT CHECKLIST
-- =============================================================================

/*
□ 1. Database and schema created
□ 2. Stage created for application files  
□ 3. Files uploaded to stage (streamlit_landing_page.py, requirements.txt)
□ 4. Warehouse specified and accessible
□ 5. READ SESSION privilege granted to Streamlit app owner role (CRITICAL!)
□ 6. Streamlit application created successfully
□ 7. Appropriate grants given to users/roles
□ 8. Application URL retrieved and tested
□ 9. Users can access and see their permitted applications
□ 10. No "KeyError: 'username'" or context function errors
*/

-- =============================================================================
-- NOTES
-- =============================================================================

/*
DEPLOYMENT NOTES:
- Replace 'COMPUTE_WH' with your actual warehouse name
- Adjust database/schema names as needed for your organization
- Modify role grants based on your access control requirements
- The application will automatically detect user permissions and show appropriate apps
- Test with different users/roles to verify access control works correctly

CRITICAL PRIVILEGES:
1. READ SESSION PRIVILEGE:
   - Required for CURRENT_USER(), CURRENT_ROLE() functions
   - Without this: "KeyError: 'username'" errors
   - Grant: GRANT READ SESSION ON ACCOUNT TO ROLE <streamlit_owner_role>;

2. SNOWFLAKE DATABASE ACCESS:
   - Required to query INFORMATION_SCHEMA.STREAMLITS system views
   - Without this: "Object does not exist or not authorized" errors
   - Grant: GRANT USAGE ON DATABASE SNOWFLAKE TO ROLE <streamlit_owner_role>;

Both privileges must be granted by ACCOUNTADMIN to the Streamlit app owner role

SECURITY CONSIDERATIONS:
- The app only shows Streamlit applications the user has actual access to
- It uses Snowflake's built-in permission system
- No sensitive information is exposed beyond what users already have access to
- All queries respect Snowflake's role-based access control (RBAC)
- READ SESSION privilege allows the app to identify the current user/role

MAINTENANCE:
- Update the application by uploading new files and recreating the Streamlit app
- Monitor usage through Snowflake's query history
- Adjust grants as your organization's needs change
- Verify READ SESSION privilege is maintained after role changes
*/
