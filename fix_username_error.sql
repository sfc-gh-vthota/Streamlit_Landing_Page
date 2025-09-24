-- =====================================
-- QUICK FIX for "KeyError: 'username'" 
-- =====================================
-- 
-- This script fixes the common "KeyError: 'username'" error that occurs
-- when Streamlit apps try to use CURRENT_USER() or CURRENT_ROLE() functions
-- without the proper READ SESSION privilege.

-- STEP 1: Use ACCOUNTADMIN role (required for granting account-level privileges)
USE ROLE ACCOUNTADMIN;

-- STEP 2: Grant READ SESSION privilege to the role that owns the Streamlit app
-- Replace 'ACCOUNTADMIN' with the actual role that owns your Streamlit app if different
GRANT READ SESSION ON ACCOUNT TO ROLE ACCOUNTADMIN;

-- If you're using a different role for your Streamlit app, use that role instead:
-- GRANT READ SESSION ON ACCOUNT TO ROLE <your_streamlit_owner_role>;

-- STEP 3: Verify the grant was applied
SHOW GRANTS ON ACCOUNT;

-- STEP 4: Refresh your Streamlit app
-- The app should now work without the "KeyError: 'username'" error

-- =====================================
-- EXPLANATION
-- =====================================
-- 
-- Streamlit apps in Snowflake run with the owner's privileges, not the caller's.
-- To use context functions like CURRENT_USER() and CURRENT_ROLE(), the owner role
-- must have the READ SESSION privilege granted at the account level.
-- 
-- This is a security feature that prevents unauthorized access to session context
-- information. The privilege must be explicitly granted by ACCOUNTADMIN.

-- =====================================
-- VERIFICATION
-- =====================================

-- Test if context functions work (run this after granting the privilege):
SELECT 
    CURRENT_USER() as current_user,
    CURRENT_ROLE() as current_role,
    CURRENT_SESSION() as current_session;

-- If the above query returns proper values instead of errors, the fix worked!

