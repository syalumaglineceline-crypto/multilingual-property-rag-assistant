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
    "Ask questions about indexed UK property-market sources. "
    "Answers are generated from retrieved source passages."
)


with st.sidebar:
    st.header("Settings")

    top_k = st.slider(
        "Number of source chunks",
        min_value=1,
        max_value=10,
        value=4,
    )

    st.markdown(
        """
        **How it works**

        1. Your question is embedded.
        2. Relevant source passages are retrieved.
        3. The LLM generates an answer using those passages.
        4. Supporting sources are shown below the answer.
        """
    )

    st.warning(
        "This project is for information retrieval and demonstration only. "
        "It does not provide mortgage, legal, financial, investment, "
        "or property-valuation advice."
    )


if "messages" not in st.session_state:
    st.session_state.messages = []


def show_sources(sources):
    if not sources:
        return

    st.markdown("**Sources**")

    for source in sources:
        label = (
            f"[{source['rank']}] {source['source']} "
            f"— chunk {source['chunk_index']}"
        )

        with st.expander(label):
            st.write(source["text"])

            if source.get("distance") is not None:
                st.caption(
                    f"Vector distance: {source['distance']:.4f}"
                )


for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

        if message["role"] == "assistant":
            show_sources(message.get("sources", []))


question = st.chat_input(
    "Ask a question about the indexed property sources..."
)


if question:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.write(question)

    try:
        with st.spinner("Searching sources and generating answer..."):
            with httpx.Client(timeout=90.0) as client:
                response = client.post(
                    f"{API_BASE_URL}/ask",
                    json={
                        "question": question,
                        "top_k": top_k,
                    },
                )

                response.raise_for_status()
                payload = response.json()

        answer = payload.get(
            "answer",
            "No answer was generated.",
        )

        sources = payload.get(
            "sources",
            [],
        )

        with st.chat_message("assistant"):
            st.write(answer)
            show_sources(sources)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "sources": sources,
            }
        )

    except httpx.HTTPStatusError as exc:
        try:
            detail = exc.response.json().get(
                "detail",
                "The API returned an error.",
            )
        except ValueError:
            detail = "The API returned an error."

        st.error(detail)

    except httpx.RequestError:
        st.error(
            "Could not reach the FastAPI service. "
            "Start it with `uvicorn app.api:app --reload`."
        )
