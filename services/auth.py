import streamlit as st


def check_password() -> bool:
    """Simple password gate for personal deployments.

    Reads the expected password from st.secrets["APP_PASSWORD"].
    Returns True once the correct password has been entered; otherwise
    renders a login form and stops the script.
    """
    if st.session_state.get("authenticated"):
        return True

    expected = st.secrets.get("APP_PASSWORD")
    if not expected:
        st.error(
            "APP_PASSWORD is not set in .streamlit/secrets.toml. "
            "Add APP_PASSWORD = \"your-password\" to enable access."
        )
        st.stop()

    st.title("🔒 FinancesV2")
    password = st.text_input("Password", type="password")
    submitted = st.button("Enter")

    if submitted:
        if password == expected:
            st.session_state["authenticated"] = True
            st.rerun()
        else:
            st.error("Incorrect password.")

    st.stop()
