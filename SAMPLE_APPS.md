# Sample Streamlit Apps

This directory contains 5 simple Streamlit apps designed to showcase the functionality of the Streamlit Landing Page. These apps demonstrate various features and can be deployed together to create a complete multi-app environment.

## 📱 Apps Overview

### 1. 📊 Simple Data Explorer (`simple_data_explorer.py`)
**Purpose:** Demonstrate data filtering and basic analytics

**Features:**
- Generates sample sales data (50 records)
- Filter by Region and Product
- Display filtered data in table format
- Show basic metrics (Total Sales, Quantity, Average Sale)
- Clean, simple interface for data exploration

**Use Case:** Perfect for showcasing data analysis capabilities and basic filtering functionality.

---

### 2. 🧮 Simple Calculator (`simple_calculator.py`)
**Purpose:** Basic mathematical operations with form validation

**Features:**
- Standard operations: +, -, ×, ÷, ^, %
- Input validation (divide by zero protection)
- Quick calculations: Square Root, Square, Absolute Value
- Error handling for invalid operations
- Clean calculator interface

**Use Case:** Demonstrates form inputs, validation, and real-time calculations.

---

### 3. 📈 Simple Chart Maker (`simple_chart_maker.py`)
**Purpose:** Create and display different chart types

**Features:**
- Generate Bar, Line, and Area charts
- Dynamic sample data generation
- Chart customization options
- Data summary statistics
- Interactive "Generate New Data" button

**Use Case:** Shows Streamlit's built-in charting capabilities and dynamic content updates.

---

### 4. 📝 Simple Survey Form (`simple_survey_form.py`)
**Purpose:** Comprehensive form with various input types and validation

**Features:**
- Multiple input types: text, email, selectbox, slider, multiselect, textarea, checkbox
- Form validation with error messages
- Success confirmation with summary display
- Required field validation
- Email format validation

**Use Case:** Perfect example of complex forms, validation, and user interaction patterns.

---

### 5. 📝 Simple Text Analyzer (`simple_text_analyzer.py`)
**Purpose:** Text analysis with statistics and insights

**Features:**
- Character, word, line, paragraph counting
- Word frequency analysis with top 5 words
- Reading time estimates (slow, average, fast readers)
- Text complexity analysis
- Sample text loading option
- Bar chart visualization of word frequency

**Use Case:** Demonstrates text processing, statistical analysis, and chart integration.

## 🚀 Deployment Instructions

### Prerequisites
1. Snowflake account with Streamlit enabled
2. Appropriate privileges (ACCOUNTADMIN or equivalent)
3. Existing warehouse for query execution

### Quick Deployment

1. **Upload Files:**
   ```sql
   -- From SnowSQL or similar tool:
   PUT file:///path/to/simple_data_explorer.py @app_stage overwrite=true;
   PUT file:///path/to/simple_calculator.py @app_stage overwrite=true;
   PUT file:///path/to/simple_chart_maker.py @app_stage overwrite=true;
   PUT file:///path/to/simple_survey_form.py @app_stage overwrite=true;
   PUT file:///path/to/simple_text_analyzer.py @app_stage overwrite=true;
   ```

2. **Run Deployment Script:**
   ```sql
   -- Execute the deploy_sample_apps.sql script
   -- Update warehouse names as needed
   ```

3. **Test Landing Page:**
   - Launch your `streamlit_landing_page` app
   - You should see all 5 sample apps listed
   - Click "Launch" buttons to test each app

### Customization Options

#### Modify App Content
- Edit any `.py` file to customize functionality
- Re-upload to stage and recreate the Streamlit app
- Changes take effect immediately

#### Add Your Own Apps
- Create new `.py` files following the same pattern
- Include Snowflake session initialization
- Add to deployment script
- Grant appropriate permissions

#### Styling and Branding
- Add custom CSS in any app's `st.markdown()` calls
- Modify color schemes, fonts, layout
- Add your organization's branding

## 🎯 Educational Value

These sample apps teach key Streamlit concepts:

1. **Session Management:** All apps properly initialize Snowflake sessions
2. **Form Handling:** Survey form shows comprehensive form patterns
3. **Data Visualization:** Chart maker and text analyzer show chart integration
4. **Input Validation:** Calculator and survey form demonstrate validation patterns
5. **State Management:** Text analyzer and chart maker use session state
6. **Error Handling:** All apps include proper error handling
7. **User Experience:** Clean, intuitive interfaces throughout

## 🔧 Troubleshooting

### Common Issues

1. **"ModuleNotFoundError"**
   - Ensure `requirements.txt` is uploaded to stage
   - Check that all required packages are listed

2. **"Warehouse not found"**
   - Update `COMPUTE_WH` in deployment script to your warehouse name
   - Ensure warehouse exists and is accessible

3. **Apps not appearing in landing page**
   - Check grants: `SHOW GRANTS ON STREAMLIT <app_name>`
   - Verify apps exist: `SHOW STREAMLITS IN SCHEMA`
   - Ensure landing page has proper permissions

4. **Session initialization errors**
   - Verify `READ SESSION` privilege is granted
   - Check `USAGE ON DATABASE SNOWFLAKE` privilege

### Verification Queries

```sql
-- Check all apps are created
SHOW STREAMLITS IN SCHEMA STREAMLIT_APPS.LANDING_PAGE;

-- Get app URLs
SELECT name, url_id FROM SNOWFLAKE.INFORMATION_SCHEMA.STREAMLITS 
WHERE database_name = 'STREAMLIT_APPS';

-- Verify permissions
SELECT * FROM SNOWFLAKE.INFORMATION_SCHEMA.TABLE_PRIVILEGES 
WHERE table_schema = 'LANDING_PAGE';
```

## 🎨 Extending the Apps

### Add New Features
- **Database Integration:** Connect apps to real Snowflake tables
- **User Authentication:** Add role-based access control
- **Advanced Charts:** Use Plotly for more complex visualizations
- **Export Functionality:** Add CSV download options
- **Scheduled Updates:** Implement automatic data refresh

### Create New Apps
Follow this pattern for new apps:

```python
import streamlit as st
from snowflake.snowpark.context import get_active_session

@st.cache_resource
def init_connection():
    return get_active_session()

def main():
    st.title("🎯 Your App Name")
    st.caption("App description")
    
    # Your app logic here
    
if __name__ == "__main__":
    main()
```

## 📊 Performance Notes

- All apps use `@st.cache_resource` for session initialization
- Sample data is generated in-memory (no database queries)
- Apps are optimized for fast loading and responsiveness
- Minimal external dependencies for better reliability

## 🎯 Use Cases

These sample apps are perfect for:

1. **Demos and Presentations:** Show Streamlit capabilities
2. **Training:** Teach Streamlit development patterns
3. **Prototyping:** Base templates for new apps
4. **Testing:** Verify deployment and permission setup
5. **User Onboarding:** Introduce users to your Streamlit environment

---

**Ready to get started?** Run the `deploy_sample_apps.sql` script and launch your landing page to see all these apps in action! 🚀



