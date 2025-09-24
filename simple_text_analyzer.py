# Simple Text Analyzer - Streamlit App
# Analyze text with basic statistics and word analysis

import streamlit as st
import re
from collections import Counter

# Snowflake connector
from snowflake.snowpark.context import get_active_session

# Initialize connection
@st.cache_resource
def init_connection():
    return get_active_session()

def analyze_text(text):
    """Analyze text and return various statistics"""
    if not text.strip():
        return None
    
    # Basic stats
    char_count = len(text)
    char_count_no_spaces = len(text.replace(' ', ''))
    word_count = len(text.split())
    line_count = len(text.split('\n'))
    paragraph_count = len([p for p in text.split('\n\n') if p.strip()])
    
    # Word analysis
    words = re.findall(r'\b\w+\b', text.lower())
    unique_words = len(set(words))
    most_common_words = Counter(words).most_common(5)
    
    # Average calculations
    avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
    avg_words_per_line = word_count / line_count if line_count > 0 else 0
    
    return {
        'char_count': char_count,
        'char_count_no_spaces': char_count_no_spaces,
        'word_count': word_count,
        'line_count': line_count,
        'paragraph_count': paragraph_count,
        'unique_words': unique_words,
        'most_common_words': most_common_words,
        'avg_word_length': avg_word_length,
        'avg_words_per_line': avg_words_per_line
    }

def main():
    st.title("📝 Simple Text Analyzer")
    st.caption("Analyze your text with basic statistics and insights")
    
    # Text input
    st.subheader("Enter Your Text")
    
    # Sample text option
    if st.button("Load Sample Text"):
        sample_text = """
        Streamlit is an open-source app framework built specifically for Machine Learning and Data Science projects.
        It allows you to create beautiful web applications in minutes with just Python code.
        
        With Streamlit, you can easily turn data scripts into shareable web apps. It's perfect for creating
        dashboards, generating reports, or building interactive tools for your team.
        
        The framework is designed to be simple and intuitive, so you can focus on your data and algorithms
        rather than worrying about web development details.
        """
        st.session_state.text_input = sample_text.strip()
    
    # Text area for input
    text_to_analyze = st.text_area(
        "Text to analyze:",
        value=st.session_state.get('text_input', ''),
        height=200,
        placeholder="Paste or type your text here..."
    )
    
    # Analysis section
    if text_to_analyze.strip():
        analysis = analyze_text(text_to_analyze)
        
        if analysis:
            st.subheader("Text Analysis Results")
            
            # Basic statistics
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Characters", f"{analysis['char_count']:,}")
                st.metric("Lines", analysis['line_count'])
            
            with col2:
                st.metric("Characters (no spaces)", f"{analysis['char_count_no_spaces']:,}")
                st.metric("Paragraphs", analysis['paragraph_count'])
            
            with col3:
                st.metric("Words", f"{analysis['word_count']:,}")
                st.metric("Unique Words", f"{analysis['unique_words']:,}")
            
            with col4:
                st.metric("Avg Word Length", f"{analysis['avg_word_length']:.1f}")
                st.metric("Avg Words/Line", f"{analysis['avg_words_per_line']:.1f}")
            
            # Word frequency analysis
            if analysis['most_common_words']:
                st.subheader("Most Common Words")
                
                # Create a simple bar chart data
                words, counts = zip(*analysis['most_common_words'])
                word_data = {
                    'Word': words,
                    'Count': counts
                }
                
                # Display as table
                st.table(word_data)
                
                # Display as bar chart
                import pandas as pd
                df = pd.DataFrame(word_data)
                st.bar_chart(df.set_index('Word')['Count'])
            
            # Reading time estimation
            st.subheader("Reading Time Estimate")
            
            # Average reading speed: 200-250 words per minute
            reading_speeds = {
                'Slow (150 wpm)': 150,
                'Average (200 wpm)': 200,
                'Fast (250 wpm)': 250
            }
            
            col1, col2, col3 = st.columns(3)
            
            for i, (speed_name, wpm) in enumerate(reading_speeds.items()):
                reading_time_minutes = analysis['word_count'] / wpm
                
                if reading_time_minutes < 1:
                    time_str = f"{reading_time_minutes * 60:.0f} seconds"
                else:
                    time_str = f"{reading_time_minutes:.1f} minutes"
                
                if i == 0:
                    col1.metric(speed_name, time_str)
                elif i == 1:
                    col2.metric(speed_name, time_str)
                else:
                    col3.metric(speed_name, time_str)
            
            # Text complexity indicators
            st.subheader("Text Complexity")
            
            complexity_score = 0
            complexity_notes = []
            
            # Simple complexity calculations
            if analysis['avg_word_length'] > 6:
                complexity_score += 1
                complexity_notes.append("Long average word length")
            
            if analysis['avg_words_per_line'] > 15:
                complexity_score += 1
                complexity_notes.append("Long sentences")
            
            if analysis['unique_words'] / analysis['word_count'] > 0.8:
                complexity_score += 1
                complexity_notes.append("High vocabulary diversity")
            
            # Display complexity
            if complexity_score == 0:
                st.success("✅ **Simple text** - Easy to read")
            elif complexity_score == 1:
                st.info("📖 **Moderate complexity** - Average reading level")
            else:
                st.warning("🔍 **Complex text** - May require focused reading")
            
            if complexity_notes:
                st.write("**Complexity indicators:**")
                for note in complexity_notes:
                    st.write(f"• {note}")
    
    else:
        st.info("👆 Enter some text above to see the analysis results")

if __name__ == "__main__":
    main()



