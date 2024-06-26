import streamlit as st

def main():
    st.title("Meeting Link")

    meet_link = "https://www.twitch.tv/alhabsilawfirm"  # Replace with actual meeting link
    st.markdown(f"Please [join the meeting here]({meet_link}).")

if __name__ == '__main__':
    main()
