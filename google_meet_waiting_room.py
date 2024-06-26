import streamlit as st
import pandas as pd

# Load your data
@st.cache_data
def load_data():
    df = pd.read_csv('email_ids.csv', encoding='ISO-8859-1')
    return df

def main():
    st.title("Meeting Verification")
    df = load_data()

    # Initialize session state
    if 'email_verified' not in st.session_state:
        st.session_state.email_verified = False
    if 'verification_successful' not in st.session_state:
        st.session_state.verification_successful = False

    if not st.session_state.email_verified:
        email = st.text_input(
            "Please enter the same email address given to the Lawyer Office(يرجى إدخال نفس عنوان البريد الإلكتروني الذي قدمته لمكتب المحامي.):",
            key="email_input"
        )
        if st.button("Submit", key="submit_button"):
            if email in df['email_ids'].values:
                st.session_state.email_verified = True
                st.session_state.email = email
                st.experimental_rerun()
            else:
                st.error("Email id not found. Please check and try again.(لم يتم العثور على عنوان البريد الإلكتروني. يرجى التحقق والمحاولة مرة أخرى.)")

    elif not st.session_state.verification_successful:
        st.success("Email id found. Please check your verification code below.(تم العثور على عنوان البريد الإلكتروني. يرجى التحقق من رمز التحقق الخاص بك أدناه.)")
        
        # Display only the user's email and unique code
        user_data = df[df['email_ids'] == st.session_state.email]
        st.table(user_data[['email_ids', 'unique_code']])
        
        code = st.text_input("Enter your verification code:(أدخل رمز التحقق الخاص بك:)", key="code_input")
        
        if st.button("Join Meeting", key="join_button"):
            if not code:
                st.error("Please enter verification code.(يرجى إدخال رمز التحقق.)")
            elif user_data['unique_code'].values[0] != code:
                st.error("Invalid verification code. Please try again.(رمز التحقق غير صالح. يرجى المحاولة مرة أخرى.)")
            else:
                st.session_state.verification_successful = True
                st.experimental_rerun()
    else:
        st.success("Verification successful! (تم التحقق بنجاح!)")
        meet_link = "https://www.twitch.tv/alhabsilawfirm"  # Replace with actual meeting link
        st.markdown(f"[Click here to join the meeting (انقر هنا للانضمام إلى الاجتماع)]({meet_link})")

if __name__ == '__main__':
    main()
