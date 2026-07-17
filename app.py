import streamlit as st
from openai import OpenAI

# ==========================================
# 1. INITIALIZATION & SETUP
# ==========================================
st.set_page_config(page_title="Copywriting Transformer", page_icon="✍️", layout="wide")
st.title("✍️ Automated Copywriting & Tone Transformer (Local API)")
st.markdown("Running 100% locally and free using Ollama and Llama 3.")

# ==========================================
# 2. FRONTEND: SIDEBAR PARAMETERS
# ==========================================
st.sidebar.header("⚙️ Inference Parameters")
st.sidebar.markdown("Control the generative model's creativity.")

temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=2.0, value=0.7, step=0.1)
top_p = st.sidebar.slider("Top_P", min_value=0.0, max_value=1.0, value=1.0, step=0.1)

# ==========================================
# 3. FRONTEND: USER VARIABLES
# ==========================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("Product Details")
    product_name = st.text_input("Product Name", "SmartBrew Coffee Maker")
    raw_description = st.text_area("Raw Description", "Brews coffee in under 2 minutes. Can be controlled via a smartphone app. Keeps coffee hot for 4 hours. Made of stainless steel.", height=150)

with col2:
    st.subheader("Marketing Strategy")
    platform = st.selectbox("Platform", ["LinkedIn", "Instagram", "Email", "Twitter", "Facebook"])
    tone = st.text_input("Desired Tone", "Professional, innovative, and business-focused")

# ==========================================
# 4. BACKEND: LOCAL GENERATION LOGIC
# ==========================================
if st.button("🚀 Generate Marketing Copy", use_container_width=True):
    
    if not product_name or not raw_description:
        st.warning("Please fill out the product details.")
    else:
        prompt_template = f"""
        You are an expert digital marketing copywriter. 
        
        Product Name: {product_name}
        Raw Description: {raw_description}
        Target Platform: {platform}
        Desired Tone: {tone}
        
        Task: Transform the raw description above into a highly engaging, professional marketing post optimized specifically for {platform}. Ensure the writing strictly follows the desired tone of: {tone}.
        """
        
        # POINTING THE CLIENT TO YOUR LOCAL OLLAMA SERVER
        client = OpenAI(
            base_url='http://localhost:11434/v1',
            api_key='ollama', # API key is required by the library, but Ollama ignores it
        )
        
        with st.spinner(f"Drafting your {platform} copy locally..."):
            try:
                response = client.chat.completions.create(
                    model="llama3", # Matches the model you downloaded in Step 1
                    messages=[
                        {"role": "system", "content": "You are a helpful and creative AI copywriter."},
                        {"role": "user", "content": prompt_template}
                    ],
                    temperature=temperature,
                    top_p=top_p
                )
                
                st.success("Success!")
                st.markdown("### 📝 Generated Copy:")
                st.info(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"An error occurred. Make sure Ollama is running in the background! Error details: {e}")