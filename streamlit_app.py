import os

import httpx
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000",
).rstrip("/")


st.set_page_config(
    page_title="Multilingual Property RAG Assistant",
    page_icon="🏠",
    layout="wide",
)

st.title("Multilingual Property RAG Assistant")

st.caption(
    "Stage 1: multilingual semantic retrieval from indexed "
    "UK property-market sources."
)

with st.sidebar:
    top_k = st.slider(
        "Number of source chunks",
        min_value=1,
        max_value=10,
        value=4,
    )

    st.markdown(
        "The LLM answer-generation layer will be added "
        "in the next project stage."
    )

question = st.chat_input(
    "Ask a question about the indexed property sources..."
)

if question:
    with st.chat_message("user"):
        st.write(question)

    try:
        with httpx.Client(timeout=60.0) as client:
            response = client.post(
                f"{API_BASE_URL}/retrieve",
                json={
                    "question": question,
                    "top_k": top_k,
                },
            )
            response.raise_for_status()
            payload = response.json()

        with st.chat_message("assistant"):
            results = payload.get("results", [])

            if not results:
                st.warning(
                    "No indexed source chunks were found. "
                    "Add documents to data/raw and run the ingestion script."
                )
            else:
                st.write("Most relevant source passages:")

                for item in results:
                    with st.expander(
                        f"{item['rank']}. {item['source']} "
                        f"(chunk {item['chunk_index']})"
                    ):
                        st.write(item["text"])

                        if item.get("distance") is not None:
                            st.caption(
                                f"Vector distance: "
                                f"{item['distance']:.4f}"
                            )

    except httpx.HTTPError as exc:
        st.error(
            "Could not reach the FastAPI service. "
            "Start it with `uvicorn app.api:app --reload`."
        )
        st.exception(exc)
