import streamlit as st
import requests
import json
from datetime import datetime


st.set_page_config(
    page_title="Law Study Buddy",
    page_icon="⚖️",
    layout="wide"
)


st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E86AB;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sidebar .sidebar-content {
        background-color: #f0f2f6;
    }
    .response-box {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2E86AB;
        margin: 10px 0;
    }
    .source-item {
        background-color: #e9ecef;
        padding: 10px;
        margin: 5px 0;
        border-radius: 5px;
        font-size: 0.9em;
    }
</style>
""", unsafe_allow_html=True)


st.markdown('<h1 class="main-header">⚖️ Law Study Buddy</h1>', unsafe_allow_html=True)
st.markdown("### AI-Powered Legal Research Assistant")


with st.sidebar:
    st.header("⚙️ Settings")

    api_url = st.text_input(
        "API URL",
        value="http://localhost:8000",
        help="URL where your FastAPI is running"
    )

    top_k = st.slider(
        "Number of sources",
        min_value=1,
        max_value=10,
        value=5,
        help="How many legal documents to retrieve"
    )

    min_score = st.slider(
        "Minimum confidence",
        min_value=0.0,
        max_value=1.0,
        value=0.2,
        step=0.1,
        help="Minimum similarity score for sources"
    )

    return_context = st.checkbox(
        "Show full context",
        value=False,
        help="Display the full text of retrieved documents"
    )


    if st.button("🔄 Check System Status"):
        try:
            response = requests.get(f"{api_url}/health")
            if response.status_code == 200:
                health_data = response.json()
                st.success(f"✅ System Status: {health_data['status']}")
                st.info(f"📊 Documents in database: {health_data.get('vector_store_count', 0)}")
            else:
                st.error("❌ Cannot connect to API")
        except Exception as e:
            st.error(f"❌ Connection error: {e}")


col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🔍 Ask a Legal Question")


    query = st.text_area(
        "Enter your legal question:",
        placeholder="E.g., What are the elements required to prove negligence in tort law?",
        height=100
    )


    with st.expander("Advanced Options"):
        custom_prompt = st.text_area(
            "Custom instructions (optional):",
            placeholder="E.g., Focus on Nigerian case law and provide practical examples...",
            height=80
        )


    if st.button("🚀 Get Legal Answer", type="primary", use_container_width=True):
        if not query.strip():
            st.error("Please enter a legal question")
        else:
            try:
                with st.spinner("🔍 Researching legal sources..."):

                    request_data = {
                        "query": query,
                        "top_k": top_k,
                        "min_score": min_score,
                        "return_context": return_context
                    }


                    if custom_prompt:
                        request_data["query"] = f"{query}\n\nAdditional instructions: {custom_prompt}"


                    response = requests.post(
                        f"{api_url}/ask",
                        json=request_data,
                        timeout=60
                    )

                    if response.status_code == 200:
                        result = response.json()


                        st.markdown("### 📝 Legal Analysis")
                        st.markdown('<div class="response-box">', unsafe_allow_html=True)
                        st.write(result["answer"])
                        st.markdown('</div>', unsafe_allow_html=True)


                        confidence = result.get("confidence", 0)
                        st.metric("Confidence Score", f"{confidence:.2%}")


                        st.subheader("📚 Legal Sources")
                        sources = result.get("sources", [])

                        if sources:
                            for i, source in enumerate(sources, 1):
                                with st.expander(f"Source {i}: {source['source']} (Score: {source['score']:.2f})"):
                                    st.write(f"**Preview:** {source['preview']}")
                                    st.write(f"**Page:** {source.get('page', 'N/A')}")
                                    st.write(f"**Relevance Score:** {source['score']:.3f}")
                        else:
                            st.info("No specific sources retrieved for this query")


                        if return_context and result.get("context"):
                            st.subheader("📖 Full Context")
                            st.text_area("Retrieved Context", result["context"], height=200)

                    else:
                        st.error(f"API Error: {response.status_code} - {response.text}")

            except requests.exceptions.RequestException as e:
                st.error(f"Network error: {e}")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

with col2:
    st.subheader("💡 Example Questions")

    examples = [
        "What constitutes murder under Nigerian criminal law?",
        "Explain the requirements for a valid contract",
        "What are the defenses to defamation?",
        "How does the statute of limitations work in tort cases?",
        "What is the difference between theft and robbery?",
        "Explain the concept of mens rea in criminal law"
    ]

    for example in examples:
        if st.button(example, key=example, use_container_width=True):
            st.session_state.last_query = example
            st.rerun()

    st.markdown("---")
    st.subheader("⚡ Quick Actions")

    if st.button("📊 Initialize Documents", use_container_width=True):
        try:
            with st.spinner("Initializing document database..."):
                response = requests.post(f"{api_url}/documents/initialize")
                if response.status_code == 200:
                    st.success("Documents initialized successfully!")
                else:
                    st.error("Failed to initialize documents")
        except Exception as e:
            st.error(f"Error: {e}")

    if st.button("📈 System Info", use_container_width=True):
        try:
            response = requests.get(f"{api_url}/system/info")
            if response.status_code == 200:
                info = response.json()
                st.json(info)
        except Exception as e:
            st.error(f"Error: {e}")


st.markdown("---")
st.markdown(
    "⚠️ **Disclaimer:** This AI assistant provides legal information for educational purposes only. "
    "It does not constitute legal advice. Always consult a qualified attorney for legal matters."
)