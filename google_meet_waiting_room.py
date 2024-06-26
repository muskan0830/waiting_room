import streamlit as st
import pandas as pd
import base64

# Load your data
@st.cache_data
def load_data():
    df = pd.read_csv('email_ids.csv', encoding='ISO-8859-1')
    return df

def get_csv_download_link(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="email_ids.csv">Download CSV file</a>'
    return href

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
        st.success("Email id found. Please locate your code in the list and paste it.(الرجاء قم بتنزيل الملف وابحث عن رمز التحقق الخاص بك في القائمه وألصقة في الخانه المخصصه للرمز بالأسفل)")
        st.markdown(get_csv_download_link(df), unsafe_allow_html=True)
        
        code = st.text_input("Enter your verification code:", key="code_input")
        
        if st.button("Join Meeting", key="join_button"):
            if not code:
                st.error("Please enter verification code.")
            elif df.loc[df['email_ids'] == st.session_state.email, 'unique_code'].values[0] != code:
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
