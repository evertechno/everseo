import streamlit as st
import google.generativeai as genai
import re
from collections import Counter
import textstat  # New import for readability scoring
from nltk.corpus import stopwords

# Configure the API key securely from Streamlit's secrets
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# Download NLTK stopwords (only need to do once)
import nltk
nltk.download('stopwords')

# Function to clean and analyze the content for SEO keywords and readability
def analyze_content(content, target_keyword):
    # Clean the content (remove non-alphanumeric characters and make lowercase)
    content_clean = re.sub(r'\W+', ' ', content.lower())
    
    # Count word occurrences
    word_count = Counter(content_clean.split())
    
    # Get the frequency of the target keyword
    keyword_frequency = word_count.get(target_keyword.lower(), 0)
    
    # Calculate readability score using textstat (Flesch Reading Ease)
    readability_score = textstat.flesch_reading_ease(content)
    
    # Calculate keyword density (percentage of target keyword in content)
    total_words = sum(word_count.values())
    keyword_density = (keyword_frequency / total_words) * 100 if total_words > 0 else 0
    
    # Provide suggestions for improvements
    suggestions = []
    if keyword_density < 2:
        suggestions.append(f"Increase the usage of the target keyword '{target_keyword}' to improve keyword density.")
    if readability_score < 60:
        suggestions.append("The content may be hard to read. Consider simplifying the language.")
    
    return keyword_frequency, keyword_density, readability_score, suggestions

# Streamlit App UI
st.title("Ever AI - Content Optimization Tool")
st.write("Optimize your content using AI and SEO analysis.")

# Input for the target keyword and content
target_keyword = st.text_input("Enter your target keyword:", "AI content optimization")
content_input = st.text_area("Enter your content here:")

# Button to generate response
if st.button("Generate and Optimize"):
    try:
        # Generate content using the generative AI model from Google
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"Write an SEO-friendly article about {target_keyword}. Make sure to include the keyword naturally throughout the content."
        response = model.generate_content(prompt)
        
        generated_content = response.text
        
        # Display the generated content
        st.write("Generated Content:")
        st.write(generated_content)
        
        # Analyze the generated content for SEO
        keyword_frequency, keyword_density, readability_score, suggestions = analyze_content(generated_content, target_keyword)
        
        # Display SEO analysis
        st.write("SEO Analysis:")
        st.write(f"Keyword Frequency for '{target_keyword}': {keyword_frequency}")
        st.write(f"Keyword Density: {keyword_density:.2f}%")
        st.write(f"Readability Score (Flesch Reading Ease): {readability_score:.2f}")
        
        # Provide optimization suggestions
        if suggestions:
            st.write("Suggestions to Improve SEO and Readability:")
            for suggestion in suggestions:
                st.write(f"- {suggestion}")
        else:
            st.write("Your content looks great! No further optimizations needed.")
    
    except Exception as e:
        st.error(f"Error: {e}")
