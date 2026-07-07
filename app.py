# NLTK resources download karne ka updated function
@st.cache_resource
def download_nltk_resources():
    nltk.download('punkt')
    nltk.download('punkt_tab')  # Yeh missing line add karein
    nltk.download('stopwords')
    nltk.download('wordnet')

download_nltk_resources()
