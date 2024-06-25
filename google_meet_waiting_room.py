import streamlit as st
import pandas as pd

# Load your data
@st.cache_data
def load_data():
    df = pd.read_csv('email_ids.csv', encoding='ISO-8859-1')
    return {row['email_ids']: row['unique_code'] for _, row in df.iterrows()}

codes = load_data()
meet_link = "https://meet.google.com/oaa-cjrv-wrd"

def main():
    st.title("Google Meet Verification")

    translation_text = """يرجى إدخال نفس عنوان البريد الإلكتروني الذي قدمته لمكتب المحامي وإلا لن تتمكن من الدخول."""

    st.text(translation_text)  # Display the translation above the input box

    email = st.text_input(
    "Please enter the same email address given to the Lawyer Office (Otherwise you will not be able to gain the access):")
    code = st.text_input("Enter your verification code:")

    if st.button("Join Meet"):
        if not email or not code:
            st.error("Please enter both Email id and verification code. (يرجى إدخال عنوان البريد الإلكتروني ورمز التحقق.)")
        elif email not in codes:
            st.error("Email id not found. Please check and try again.(لم يتم العثور على عنوان البريد الإلكتروني. يرجى التحقق والمحاولة مرة أخرى.)")
        elif codes[email] != code:
            st.error("Invalid verification code. Please try again.(رمز التحقق غير صالح. يرجى المحاولة مرة أخرى.)")
        else:
            st.success("Verification successful! (تم التحقق بنجاح!)")
            st.markdown(f"[Click here to join the meeting (انقر هنا للانضمام إلى الاجتماع)]({meet_link})")

if __name__ == '__main__':
    main()
