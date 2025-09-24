# Streamlit Landing Page - User-Specific App Access

A comprehensive Streamlit application that serves as a landing page, showing users only the Streamlit applications they have access to based on their Snowflake permissions.

## Features

### 🚀 Core Functionality
- **User-Specific Access**: Shows only Streamlit apps the current user has permissions to access
- **Real-Time Permissions**: Queries Snowflake system tables to determine actual access rights
- **Multiple Access Levels**: Distinguishes between owned apps, accessible apps, and restricted access
- **Interactive UI**: Beautiful card-based layout with hover effects and responsive design

### 🎯 User Experience
- **Smart Search**: Search across app names, descriptions, and owners
- **Advanced Filtering**: Filter by access level (Owner, Accessible, Check Access)
- **Flexible Sorting**: Sort by creation date or alphabetically
- **Quick Overview**: Summary metrics showing total apps, owned apps, and accessible apps
- **One-Click Launch**: Direct links to launch each application

### 🛡️ Security & Permissions
- **Permission-Based Display**: Only shows apps the user can actually access
- **Role-Aware**: Considers current Snowflake role when determining access
- **Fallback Mechanism**: Gracefully handles different Snowflake configurations
- **Demo Mode**: Shows sample apps when no real apps are available

## Quick Start

### Prerequisites
- Snowflake account with Streamlit enabled
- Python 3.8+ (for local development)
- Required Python packages (see requirements.txt)

### Installation

1. **Clone or download the files:**
   ```bash
   # Main files:
   # - streamlit_landing_page.py
   # - requirements.txt
   # - deploy_to_snowflake.sql
   
   # Sample apps (optional):
   # - simple_data_explorer.py
   # - simple_calculator.py
   # - simple_chart_maker.py
   # - simple_survey_form.py
   # - simple_text_analyzer.py
   # - deploy_sample_apps.sql
   ```

2. **For local development:**
   ```bash
   pip install -r requirements.txt
   streamlit run streamlit_landing_page.py
   ```

3. **For Snowflake deployment:**
   - Upload the `streamlit_landing_page.py` file to a Snowflake stage
   - Create the Streamlit app using Snowflake's CREATE STREAMLIT command
   - Reference the stage location and main file
   
4. **Deploy sample apps (optional):**
   - Run `deploy_sample_apps.sql` to create 5 sample Streamlit apps
   - This populates your landing page with example applications

### Snowflake Deployment Example

```sql
-- Create a stage for your Streamlit app
CREATE STAGE IF NOT EXISTS streamlit_apps.landing_page;

-- Upload your files to the stage (using SnowSQL or Snowsight)
PUT file://streamlit_landing_page.py @streamlit_apps.landing_page overwrite=true;
PUT file://requirements.txt @streamlit_apps.landing_page overwrite=true;

-- Create the Streamlit application
CREATE STREAMLIT streamlit_landing_page
ROOT_LOCATION = '@streamlit_apps.landing_page'
MAIN_FILE = 'streamlit_landing_page.py'
QUERY_WAREHOUSE = 'your_warehouse_name';

-- Grant access to roles that should use the landing page
GRANT USAGE ON STREAMLIT streamlit_landing_page TO ROLE analyst_role;
```

## 📱 Sample Apps

This project includes 5 ready-to-deploy sample Streamlit apps to showcase the landing page functionality:

### 1. 📊 Simple Data Explorer
- **File**: `simple_data_explorer.py`
- **Purpose**: Demonstrate data filtering and basic analytics
- **Features**: Sample sales data, filters, metrics display

### 2. 🧮 Simple Calculator
- **File**: `simple_calculator.py`
- **Purpose**: Basic mathematical operations with validation
- **Features**: Standard math operations, error handling, quick calculations

### 3. 📈 Simple Chart Maker
- **File**: `simple_chart_maker.py`
- **Purpose**: Create and display different chart types
- **Features**: Bar/Line/Area charts, dynamic data generation, statistics

### 4. 📝 Simple Survey Form
- **File**: `simple_survey_form.py`
- **Purpose**: Comprehensive form with validation
- **Features**: Multiple input types, validation, results summary

### 5. 📝 Simple Text Analyzer
- **File**: `simple_text_analyzer.py`
- **Purpose**: Text analysis with statistics and insights
- **Features**: Word frequency, reading time, complexity analysis

### Deploying Sample Apps

Run the `deploy_sample_apps.sql` script to create all 5 sample apps:

```sql
-- Execute the deployment script
USE ROLE ACCOUNTADMIN;
USE SCHEMA STREAMLIT_APPS.LANDING_PAGE;

-- Follow the instructions in deploy_sample_apps.sql
```

**Result**: Your landing page will show all sample apps with launch buttons!

See `SAMPLE_APPS.md` for detailed documentation of each sample app.

## How It Works

### Permission Detection
The app queries Snowflake's system tables to determine which Streamlit applications the current user can access:

1. **INFORMATION_SCHEMA.STREAMLITS**: Gets list of all Streamlit apps in the account
2. **INFORMATION_SCHEMA.TABLE_PRIVILEGES**: Checks user and role-based permissions
3. **Access Logic**: Combines ownership and privilege information to determine access level

### Access Levels
- **👑 Owner**: User created or owns the application
- **✅ Accessible**: User has usage permissions granted
- **🔍 Check Access**: Permissions need verification

### Fallback Behavior
If the advanced permission queries fail (due to different Snowflake configurations), the app:
- Falls back to simpler queries
- Shows sample applications for demonstration
- Provides helpful error messages and troubleshooting tips

## Customization

### Adding Your Own Apps
To showcase your specific Streamlit applications, modify the `get_sample_apps()` function:

```python
def get_sample_apps():
    return pd.DataFrame([
        {
            'APP_NAME': 'Your App Name',
            'APP_URL': '/your-app-url',
            'CREATED_ON': datetime.now(),
            'OWNER': 'YOUR_USERNAME',
            'DESCRIPTION': 'Description of your app',
            'DATABASE_NAME': 'YOUR_DB',
            'SCHEMA_NAME': 'YOUR_SCHEMA',
            'ACCESS_STATUS': 'Accessible',
            'ACCESS_LEVEL': 'USAGE'
        },
        # Add more apps...
    ])
```

### Styling Customization
The app uses custom CSS that can be modified in the `main()` function:
- Colors and themes
- Card layouts and hover effects
- Responsive breakpoints
- Typography and spacing

### Query Customization
Modify the SQL queries in `get_user_streamlit_apps()` to:
- Filter specific databases or schemas
- Include additional metadata
- Implement custom permission logic

## Troubleshooting

### Common Issues

1. **No apps showing up**:
   - Check if you have any Streamlit apps deployed
   - Verify your role has appropriate permissions
   - Review the Snowflake error messages in the app

2. **Permission errors**:
   - Ensure your role has access to INFORMATION_SCHEMA tables
   - Check if you need ACCOUNTADMIN privileges for full visibility
   - Contact your Snowflake administrator for proper grants

3. **App not loading**:
   - Verify all dependencies are installed
   - Check the Snowflake warehouse is running
   - Ensure the stage and files are properly uploaded

### Debug Mode
The app includes comprehensive error handling and will show:
- Detailed error messages for permission issues
- Fallback options when queries fail
- Helpful suggestions for resolving access problems

## Architecture

### Components
- **Session Management**: Handles Snowflake connection and user context
- **Permission Engine**: Queries system tables for access information
- **UI Framework**: Responsive card-based layout with search and filtering
- **Data Layer**: Processes and formats application metadata

### Performance
- **Caching**: Uses Streamlit's caching for database connections
- **Efficient Queries**: Optimized SQL to minimize system table scans
- **Lazy Loading**: Only loads data when needed
- **Responsive Design**: Works on desktop and mobile devices

## Security Considerations

- **Principle of Least Privilege**: Only shows apps the user can actually access
- **No Sensitive Data**: Doesn't expose connection strings or credentials
- **Audit Trail**: All access is logged through Snowflake's standard audit mechanisms
- **Role-Based**: Respects Snowflake's role-based access control (RBAC)

## Future Enhancements

Potential improvements for future versions:
- **Usage Analytics**: Track app launch frequency and user preferences
- **Favorites System**: Allow users to bookmark frequently used apps
- **Categories**: Organize apps by business function or team
- **Health Monitoring**: Show app status and performance metrics
- **Integration**: Connect with external app catalogs or documentation systems

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Snowflake's Streamlit documentation
3. Contact your Snowflake administrator for permission issues
4. Submit issues through your organization's support channels

---

**Built with ❤️ using Streamlit and Snowflake**

