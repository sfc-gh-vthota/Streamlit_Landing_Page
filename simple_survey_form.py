# Simple Survey Form - Streamlit App
# Basic form with various input types and validation

import streamlit as st
from datetime import datetime

# Snowflake connector
from snowflake.snowpark.context import get_active_session

# Initialize connection
@st.cache_resource
def init_connection():
    return get_active_session()

def main():
    st.title("📝 Simple Survey Form")
    st.caption("Fill out this sample survey form")
    
    # Survey form
    st.subheader("Customer Feedback Survey")
    
    with st.form("survey_form"):
        # Basic information
        st.write("**Basic Information**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name*", placeholder="Enter your full name")
            
        with col2:
            email = st.text_input("Email*", placeholder="your.email@company.com")
        
        department = st.selectbox(
            "Department*",
            options=["", "Sales", "Marketing", "Engineering", "HR", "Finance", "Operations", "Other"]
        )
        
        # Experience section
        st.write("**Experience Rating**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            satisfaction = st.slider(
                "Overall Satisfaction (1-10)",
                min_value=1, max_value=10, value=5
            )
            
        with col2:
            recommendation = st.slider(
                "Likelihood to Recommend (1-10)",
                min_value=1, max_value=10, value=5
            )
        
        # Multiple choice
        services_used = st.multiselect(
            "Which services have you used?",
            options=["Web Application", "Mobile App", "API", "Customer Support", "Training", "Documentation"]
        )
        
        # Feedback
        st.write("**Feedback**")
        
        what_works = st.text_area(
            "What works well?",
            placeholder="Tell us what you like...",
            height=100
        )
        
        improvements = st.text_area(
            "What could be improved?",
            placeholder="Tell us what could be better...",
            height=100
        )
        
        # Additional options
        newsletter = st.checkbox("Subscribe to our newsletter")
        follow_up = st.checkbox("I'm open to follow-up questions")
        
        # Submit button
        submitted = st.form_submit_button("Submit Survey", type="primary")
        
        if submitted:
            # Basic validation
            errors = []
            
            if not name.strip():
                errors.append("Full Name is required")
            
            if not email.strip():
                errors.append("Email is required")
            elif "@" not in email:
                errors.append("Please enter a valid email address")
            
            if not department:
                errors.append("Department is required")
            
            if errors:
                st.error("Please fix the following errors:")
                for error in errors:
                    st.write(f"• {error}")
            else:
                # Success message
                st.success("🎉 Survey submitted successfully!")
                
                # Display summary
                st.subheader("Survey Summary")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Name:** {name}")
                    st.write(f"**Email:** {email}")
                    st.write(f"**Department:** {department}")
                    st.write(f"**Satisfaction:** {satisfaction}/10")
                    st.write(f"**Recommendation:** {recommendation}/10")
                
                with col2:
                    st.write(f"**Services Used:** {', '.join(services_used) if services_used else 'None selected'}")
                    st.write(f"**Newsletter:** {'Yes' if newsletter else 'No'}")
                    st.write(f"**Follow-up OK:** {'Yes' if follow_up else 'No'}")
                    st.write(f"**Submitted:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
                
                if what_works:
                    st.write(f"**What Works:** {what_works}")
                
                if improvements:
                    st.write(f"**Improvements:** {improvements}")
                
                # Thank you message
                st.info("Thank you for your feedback! Your responses help us improve our services.")

if __name__ == "__main__":
    main()



