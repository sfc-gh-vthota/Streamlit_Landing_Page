# Simple Calculator - Streamlit App
# Basic calculator with standard operations

import streamlit as st

# Snowflake connector
from snowflake.snowpark.context import get_active_session

# Initialize connection
@st.cache_resource
def init_connection():
    return get_active_session()

def main():
    st.title("🧮 Simple Calculator")
    st.caption("Basic calculator with standard operations")
    
    # Calculator input section
    st.subheader("Calculator")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        num1 = st.number_input("First Number", value=0.0, format="%.2f")
    
    with col2:
        operation = st.selectbox(
            "Operation",
            options=["+", "-", "×", "÷", "^", "%"]
        )
    
    with col3:
        num2 = st.number_input("Second Number", value=0.0, format="%.2f")
    
    # Calculate button
    if st.button("Calculate", type="primary"):
        try:
            if operation == "+":
                result = num1 + num2
                st.success(f"{num1} + {num2} = **{result}**")
                
            elif operation == "-":
                result = num1 - num2
                st.success(f"{num1} - {num2} = **{result}**")
                
            elif operation == "×":
                result = num1 * num2
                st.success(f"{num1} × {num2} = **{result}**")
                
            elif operation == "÷":
                if num2 != 0:
                    result = num1 / num2
                    st.success(f"{num1} ÷ {num2} = **{result:.4f}**")
                else:
                    st.error("Cannot divide by zero!")
                    
            elif operation == "^":
                result = num1 ** num2
                st.success(f"{num1} ^ {num2} = **{result}**")
                
            elif operation == "%":
                if num2 != 0:
                    result = num1 % num2
                    st.success(f"{num1} % {num2} = **{result}**")
                else:
                    st.error("Cannot calculate modulo with zero!")
                    
        except Exception as e:
            st.error(f"Calculation error: {str(e)}")
    
    # Quick calculations section
    st.subheader("Quick Calculations")
    
    if st.button("Square Root of First Number"):
        if num1 >= 0:
            result = num1 ** 0.5
            st.info(f"√{num1} = **{result:.4f}**")
        else:
            st.error("Cannot calculate square root of negative number!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Square First Number"):
            result = num1 ** 2
            st.info(f"{num1}² = **{result}**")
    
    with col2:
        if st.button("Absolute Value"):
            result = abs(num1)
            st.info(f"|{num1}| = **{result}**")

if __name__ == "__main__":
    main()



