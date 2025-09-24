# Streamlit Landing Page - User-Specific App Access
# This application shows users only the Streamlit applications they have access to

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Snowflake connector for Streamlit in Snowflake
from snowflake.snowpark.context import get_active_session

# Initialize Snowflake session
@st.cache_resource
def init_connection():
    """Initialize connection to Snowflake"""
    return get_active_session()

def get_current_user_info(session):
    """Get current user information with robust error handling"""
    try:
        # Try to get user info with context functions
        user_query = "SELECT CURRENT_USER() as username, CURRENT_ROLE() as current_role"
        result = session.sql(user_query).collect()
        
        if result and len(result) > 0:
            user_data = result[0].asDict()
            # Handle case sensitivity issues - Snowflake might return uppercase column names
            username = user_data.get('username') or user_data.get('USERNAME') or user_data.get('CURRENT_USER()') or 'Unknown User'
            current_role = user_data.get('current_role') or user_data.get('CURRENT_ROLE') or user_data.get('CURRENT_ROLE()') or 'Unknown Role'
            
            return {
                "username": str(username),
                "current_role": str(current_role)
            }
        else:
            return {"username": "Unknown User", "current_role": "Unknown Role"}
            
    except Exception as e:
        # Context functions might not work without proper privileges
        st.warning(f"⚠️ Unable to retrieve user context: {str(e)}")
        st.info("""
        **Note**: To display current user information, the Streamlit app owner role needs the READ SESSION privilege.
        
        Ask your administrator to run:
        ```sql
        USE ROLE ACCOUNTADMIN;
        GRANT READ SESSION ON ACCOUNT TO ROLE <streamlit_owner_role>;
        ```
        """)
        
        # Return generic info when context functions don't work
        return {
            "username": "Streamlit User", 
            "current_role": "Current Role"
        }

def get_user_streamlit_apps(session):
    """
    Get list of Streamlit applications that the current user has access to
    This queries Snowflake's system tables to find accessible Streamlit apps
    """
    
    def map_row_to_standard_format(row_dict):
        """Helper function to map row data to standard format"""
        return {
            'APP_NAME': (row_dict.get('TITLE') or row_dict.get('title') or 
                       row_dict.get('STREAMLIT_TITLE') or row_dict.get('streamlit_title') or
                       row_dict.get('APP_TITLE') or row_dict.get('app_title') or 
                       row_dict.get('NAME') or row_dict.get('name') or 
                       row_dict.get('APP_NAME') or row_dict.get('app_name') or 
                       row_dict.get('STREAMLIT_NAME') or row_dict.get('streamlit_name') or 'Unknown'),
            'INTERNAL_NAME': (row_dict.get('STREAMLIT_NAME') or row_dict.get('streamlit_name') or 
                            row_dict.get('NAME') or row_dict.get('name') or
                            row_dict.get('APP_NAME') or row_dict.get('app_name') or 'Unknown'),
            'APP_URL': (row_dict.get('STREAMLIT_URL_ID') or row_dict.get('streamlit_url_id') or
                      row_dict.get('STREAMLIT_URL') or row_dict.get('streamlit_url') or
                      row_dict.get('URL_ID') or row_dict.get('url_id') or 
                      row_dict.get('APP_URL_ID') or row_dict.get('app_url_id') or
                      row_dict.get('URL') or row_dict.get('url') or 
                      row_dict.get('APP_URL') or row_dict.get('app_url') or ''),
            'CREATED_ON': (row_dict.get('CREATED_ON') or row_dict.get('created_on') or 
                         row_dict.get('CREATED') or ''),
            'OWNER': (row_dict.get('STREAMLIT_OWNER') or row_dict.get('streamlit_owner') or 
                    row_dict.get('OWNER') or row_dict.get('owner') or 
                    row_dict.get('CREATED_BY') or row_dict.get('created_by') or 'Unknown'),
            'DESCRIPTION': (row_dict.get('COMMENT') or row_dict.get('comment') or 
                          row_dict.get('DESCRIPTION') or 'No description available'),
            'DATABASE_NAME': (row_dict.get('STREAMLIT_CATALOG') or row_dict.get('streamlit_catalog') or
                            row_dict.get('DATABASE_NAME') or row_dict.get('database_name') or 
                            row_dict.get('DB') or ''),
            'SCHEMA_NAME': (row_dict.get('STREAMLIT_SCHEMA') or row_dict.get('streamlit_schema') or
                          row_dict.get('SCHEMA_NAME') or row_dict.get('schema_name') or 
                          row_dict.get('SCHEMA') or ''),
            'ACCESS_STATUS': 'Available',
            'ACCESS_LEVEL': 'USAGE'
        }
    
    # Try multiple approaches silently
    approaches = [
        "SELECT * FROM SNOWFLAKE.INFORMATION_SCHEMA.STREAMLITS",
        "SELECT * FROM INFORMATION_SCHEMA.STREAMLITS", 
        "SHOW STREAMLITS"
    ]
    
    for query in approaches:
        try:
            result = session.sql(query).collect()
            if result:
                apps_data = []
                for row in result:
                    row_dict = row.asDict()
                    apps_data.append(map_row_to_standard_format(row_dict))
                return pd.DataFrame(apps_data)
        except:
            continue
    
    # If no real apps found, return empty DataFrame
    return pd.DataFrame()

def get_sample_apps():
    """
    Provide sample apps for demonstration if no real apps are found
    """
    return pd.DataFrame([
        {
            'APP_NAME': 'Cortex Search Entitlements Demo',
            'APP_URL': '/cortex-search-entitlements-demo',
            'CREATED_ON': datetime.now() - timedelta(days=5),
            'OWNER': 'DEMO_USER',
            'DESCRIPTION': 'Real-time transaction access with user-based entitlements and performance monitoring using Cortex Search',
            'DATABASE_NAME': 'CORTEX_SEARCH_ENTITLEMENT_DB',
            'SCHEMA_NAME': 'DYNAMIC_DEMO',
            'ACCESS_STATUS': 'Accessible',
            'ACCESS_LEVEL': 'USAGE'
        },
        {
            'APP_NAME': 'Sales Dashboard',
            'APP_URL': '/sales-dashboard',
            'CREATED_ON': datetime.now() - timedelta(days=10),
            'OWNER': 'ANALYTICS_TEAM',
            'DESCRIPTION': 'Comprehensive sales analytics and reporting dashboard with regional breakdowns',
            'DATABASE_NAME': 'SALES_DB',
            'SCHEMA_NAME': 'REPORTING',
            'ACCESS_STATUS': 'Accessible',
            'ACCESS_LEVEL': 'USAGE'
        },
        {
            'APP_NAME': 'Customer Analytics Portal',
            'APP_URL': '/customer-analytics',
            'CREATED_ON': datetime.now() - timedelta(days=15),
            'OWNER': 'MARKETING_TEAM',
            'DESCRIPTION': 'Customer behavior analysis, segmentation, and campaign performance tracking',
            'DATABASE_NAME': 'CUSTOMER_DB',
            'SCHEMA_NAME': 'ANALYTICS',
            'ACCESS_STATUS': 'Accessible',
            'ACCESS_LEVEL': 'USAGE'
        },
        {
            'APP_NAME': 'Financial Reports',
            'APP_URL': '/financial-reports',
            'CREATED_ON': datetime.now() - timedelta(days=20),
            'OWNER': 'FINANCE_TEAM',
            'DESCRIPTION': 'Monthly and quarterly financial reporting with automated insights',
            'DATABASE_NAME': 'FINANCE_DB',
            'SCHEMA_NAME': 'REPORTS',
            'ACCESS_STATUS': 'Owner',
            'ACCESS_LEVEL': 'OWNERSHIP'
        }
    ])


def main():
    """Main Streamlit application"""
    # Page configuration
    st.set_page_config(
        page_title="Streamlit App Landing Page",
        page_icon="🚀",
        layout="wide"
    )
    
    # Header
    st.title("🚀 Streamlit Applications")
    st.caption("Your accessible Streamlit applications")
    
    # Initialize connection
    session = init_connection()
    
    # Get current user info
    user_info = get_current_user_info(session)
    
    # Welcome message
    st.info(f"👋 **Welcome {user_info['username']}!** (Role: {user_info['current_role']})")
    
    # Main content area
    with st.spinner("🔍 Loading your accessible Streamlit applications..."):
        # Try to get real apps from Snowflake
        apps_df = get_user_streamlit_apps(session)
        
        # If no real apps found, use sample data
        if apps_df.empty:
            st.info("No Streamlit applications found. Showing sample apps for demonstration.")
            apps_df = get_sample_apps()
    
    # Simple apps list
    if not apps_df.empty:
        for idx, app in apps_df.iterrows():
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    st.markdown(f"**🚀 {app['APP_NAME']}**")
                    st.caption(f"Owner: {app['OWNER']} | {app['DESCRIPTION']}")
                
                with col2:
                    # Construct Snowflake Streamlit app URL using static base URL
                    if app['INTERNAL_NAME'] and app['INTERNAL_NAME'] != 'Unknown':
                        try:
                            # Static base URL for your Snowflake environment
                            base_url = "https://app.snowflake.com/sfsenorthamerica/demo387/#/streamlit-apps/STREAMLIT_APPS.LANDING_PAGE"
                            
                            # Get the actual streamlit name
                            streamlit_name = app['INTERNAL_NAME']
                            
                            # Construct the full URL by appending the streamlit name
                            full_url = f"{base_url}.{streamlit_name}"
                            
                            # Create clickable launch link
                            st.markdown(f"""
                                <a href="{full_url}" target="_blank" style="
                                    display: inline-block;
                                    background-color: #ff4b4b;
                                    color: white;
                                    padding: 0.5rem 1rem;
                                    text-decoration: none;
                                    border-radius: 0.5rem;
                                    font-weight: 500;
                                    text-align: center;
                                    width: 100%;
                                    box-sizing: border-box;
                                ">
                                    🚀 Launch
                                </a>
                            """, unsafe_allow_html=True)
                            
                        except Exception as e:
                            # Fallback to regular button if URL construction fails
                            if st.button("Launch", key=f"launch_{idx}", type="primary"):
                                st.error("Unable to construct app URL")
                    else:
                        # No streamlit name available
                        st.markdown(f"""
                            <div style="
                                display: inline-block;
                                background-color: #cccccc;
                                color: #666666;
                                padding: 0.5rem 1rem;
                                border-radius: 0.5rem;
                                font-weight: 500;
                                text-align: center;
                                width: 100%;
                                box-sizing: border-box;
                            ">
                                ⚠️ URL Not Available
                            </div>
                        """, unsafe_allow_html=True)
                        
                
                st.divider()
    else:
        st.warning("No Streamlit applications found.")
    
    # Simple footer
    st.markdown("---")
    st.caption("🚀 Streamlit Applications Landing Page | Powered by Snowflake")

if __name__ == "__main__":
    main()
