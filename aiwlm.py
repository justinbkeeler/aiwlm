import streamlit as st
import openai
import textwrap

# Set your OpenAI API key
api_key = st.secrets["OPENAI_API_KEY"]

def buddy_beam_welcome():
    """
    Generates Buddy Beam's welcoming message and sets the tone for confidential and supportive conversation.
    """
    return """
    Hey there! I'm Buddy Beam, your guide through the ups and downs of work life. Feeling stuck, isolated, or just in need of a chat? I'm here to shine a light on your concerns. 
    My mission? To brighten your day with support, advice, and a bit of cheer. So, what's on your mind? Share your story or ask me anything - let's light up your work journey together. 
    And, just for kicks, how about we start with your name and a snapshot of your current work vibes?
    """

def generate_buddy_beam_advice(conversation_history, employee_input):
    """
    Generates responses from Buddy Beam, based on the employee's input, integrating emotional support,
    problem-solving assistance, and resource guidance.
    """
    # Extract user's name from the conversation history if provided
    user_name = "there"
    if st.session_state.dialogue_count == 1:
        # Assuming the user's name or alias might be provided in the first input
        user_name = employee_input.split()[0]  # Simplistic approach to extract a name
    
    name_inquiry_phrases = ["how did you get your name", "why are you called", "what does your name mean"]
    if any(phrase in employee_input.lower() for phrase in name_inquiry_phrases):
        # Return the crafted explanation about Buddy Beam's name directly
        return f"Buddy Beam embodies the concept of a reliable, insightful friend in the digital realm, ready to offer guidance, support, and a listening 'ear' anytime, anywhere. Plus, it's easy to remember and fun to say, {user_name}! What else can I assist you with?"

    try:
        full_conversation = [
            {"role": "system", "content": "Take on a mentor role for the user! Incorporate a rhetorical question in output 2 and 3 to keep a dialogue going. Ask the user's name and refer to their first name in subsquent output. You offer specific and applied emotional support, hope, problem-solving strategies, resource guidance, and learning development for the user when they write about challenges at work. You aim to assist with common workplace issues, offering a personalized experience. This is done with well thought out content that has complete sentences. Your content may not exceed 150 words per response. You need to clearly hint at being transparent and not resorting to knowledge hiding, while not explicity stating this. Also, there needs to be hint of encouragement and uplifting in your responses to build trust and repertorie with you by the user."},
            *conversation_history,
            {"role": "user", "content": employee_input}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=full_conversation,
            temperature=0.75,
            max_tokens=200,
            top_p=.5,
            frequency_penalty=0.5,
            presence_penalty=0.5
        )
        advice = response.choices[0].message['content'].strip()
        # Add a rhetorical question or engaging prompt if it's the second or third interaction
        if st.session_state.dialogue_count in [2, 3]:
            advice += f" Thoughts, {user_name}?"

        return advice
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():

    # Custom CSS to inject for modifying the expander color
    st.markdown("""
    <style>
    /* Targeting all Streamlit expander headers to change their background color */
    .st-ae { 
        background-color: #FFFDE7;
    }
    </style>
    """, unsafe_allow_html=True)

    if 'dialogue_count' not in st.session_state:
        st.session_state.dialogue_count = 0
        st.session_state.conversation_history = []

    st.markdown("""
<div style='text-align: center;'>
    <h2 style='margin-bottom: -10px; line-height: 1.1; color: #1F51FF;'><strong>Meet Buddy Beam: <br>Illuminating Your Workday Path!</strong></h2>
    <h3>🌟Welcome to a Brighter Side of Work🌟</h3>
</div>

""", unsafe_allow_html=True)

    if st.session_state.dialogue_count == 0:
        st.write(buddy_beam_welcome())

    # Instructions text disappears after the user starts typing
    instructions = "If this is your first message, include details about your job role and situation here. This space is also where you converse with the AI Assistant."
    employee_input = st.text_area("What's Dimming Your Shine Today?", value="", placeholder=instructions, key=f"employee_input_{st.session_state.dialogue_count}", on_change=lambda: st.session_state.update(text_area_clicked=True))

    if 'text_area_clicked' not in st.session_state:
        st.session_state.text_area_clicked = False

    if st.button("Seek Advice from Buddy Beam") and employee_input.strip():
        st.session_state.conversation_history.append({"role": "user", "content": employee_input})
        
        advice = generate_buddy_beam_advice(st.session_state.conversation_history, employee_input)
        st.session_state.conversation_history.append({"role": "assistant", "content": advice})

        st.session_state.dialogue_count += 1

        st.experimental_rerun()

    else:
        if st.session_state.dialogue_count >= 5:
            st.markdown("**You've reached the end of this session.** Feel free to start a new one whenever you need. Remember, I'm here to help you navigate your workplace challenges.")

    # Display conversation history
    for message in reversed(st.session_state.conversation_history):
        if message["role"] == "user":
            st.markdown(f"**You:** {textwrap.fill(message['content'], width=80)}")
        else:
            st.markdown(f"**Buddy Beam:** {textwrap.fill(message['content'], width=80)}")

    # Guiding message about using and citing the application, displayed before the "Credits" section
    st.markdown("""
<div style='text-align: center; margin-top: 20px;'>
    <p><strong>For more information on using and citing this web application, see the sections below.</strong></p>
</div>
""", unsafe_allow_html=True)

    with st.expander("Credits"):
        st.markdown("""
        <div style='text-align: center;'>
            <p>Created & Designed by: <strong>Dr. Justin B. Keeler</strong></p>
            <p>Contact Me: <strong>justin@datasciencegym.com</strong></p>
            <p>OpenAI API Model Version: <strong>gpt-4-0613</strong></p>
            <p>Last Updated: <strong>03/14/2024</strong></p>
        </div>
        """, unsafe_allow_html=True)

    with st.expander("Cite This Web Application"):
        st.markdown("""
        - **APA**: Keeler, J.B. (2024). AI Work Life Mentor: Customized Scenario Consultations. GitHub. Retrieved March 14, 2024, from https://github.com/justinbkeeler/aiwlm.git.  
        - **MLA**: Keeler, Justin B. AI Work Life Mentor: Customized Scenario Consultations. 2024, https://github.com/justinbkeeler/aiwlm.git.  
        - **Chicago**: Keeler, Justin B. 2024. AI Work Life Mentor: Customized Scenario Consultations. Accessed March 14, 2024. https://github.com/justinbkeeler/aiwlm.git.
        """)

    with st.expander("Guidelines for Use"):
        st.markdown("""
        - **Attribution**: Please acknowledge Dr. Justin B. Keeler as the original creator and developer of "AI Work Life Mentor: Customized Scenario Consultations." It's important to highlight the foundational support provided by OpenAI's ChatGPT-4 technology that powers this application. Your recognition supports the spirit of innovation and collaboration that brought this tool to life.

        - **Purpose of Use**: I encourage the use of "AI Work Life Mentor" for a broad range of applications, including academic research, educational enhancement, and professional development projects. When you share or present work that benefits from my application, I ask that you briefly describe how it contributed to your objectives. This not only showcases the application's versatility but also inspires potential users by illustrating real-world applications.

        - **Compliance with Terms of Use**: By using "AI Work Life Mentor," you agree to comply with the terms of use and license agreements provided. This includes, but is not limited to, restrictions on commercial exploitation, unauthorized modifications, or redistribution of the application's content or functionality. These guidelines are in place to protect both the users and me, ensuring the application's integrity and availability for all.

        - **Acknowledgment of OpenAI**: Given that the application significantly leverages ChatGPT-4 technology, any use of "AI Work Life Mentor" that results in publications, presentations, or other forms of sharing should include an acknowledgment of OpenAI's role in enabling the application's functionality. Recognizing OpenAI's contribution highlights the collaborative effort behind AI advancements and promotes a culture of gratitude within the tech community. significantly relies on OpenAI's ChatGPT-4, acknowledge OpenAI's contribution, especially if the AI-generated content plays a central role in the project.
        """)

    with st.expander("Additional Notes"):
        st.markdown("""
        - **User Data and Privacy**: I am committed to protecting your privacy and personal information. Any data you provide while using the application is handled with the utmost care, following strict data protection protocols. I do NOT personally log or maintain a record on a server of any in session data you provide. 
                    
        - **Feedback and Continuous Improvement**: Your feedback is invaluable to me. It helps in refining and enhancing the application to better meet your needs. I encourage you to share your experiences, suggestions, and any issues encountered while using the application.
    """)

    with st.expander("Disclaimer"):
        st.markdown("""
    By using "AI Work Life Mentor: Customized Scenario Consultations" (the "Application"), you acknowledge and agree that:

    1. **AI-Generated Content**: The Application generates content based on input from users using technology powered by OpenAI's ChatGPT-4. The content created by the AI model ("AI-Generated Content") is inherently unpredictable and without the express control of Dr. Justin B. Keeler, the Application's developer, or any associated parties.

    2. **No Responsibility**: Dr. Justin B. Keeler, along with any individuals or entities associated with the development, production, distribution, or operation of the Application, shall not be held responsible or liable for any AI-Generated Content or the consequences of using, attempting to use, or relying on such content. This includes, but is not limited to, any direct, indirect, incidental, consequential, or punitive damages arising from your access to or use of the Application.

    3. **No Warranty**: The Application and AI-Generated Content are provided "AS IS" and "AS AVAILABLE," without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, accuracy, or non-infringement.

    4. **User Discretion**: You are solely responsible for your use of the Application and any AI-Generated Content. It is your responsibility to evaluate the accuracy, completeness, or usefulness of any information, opinion, advice, or other content available through the Application.

    5. **Compliance and Conduct**: You agree to use the Application in compliance with all applicable laws, regulations, and codes of conduct. You will not use the Application for any unlawful or prohibited purpose.

    6. **Indemnification**: You agree to indemnify and hold harmless Dr. Justin B. Keeler, and any associated parties, from and against any claims, liabilities, damages, losses, and expenses, including without limitation reasonable attorney fees and costs, arising out of or in any way connected with your access to or use of the Application and AI-Generated Content, your violation of this Disclaimer, or your violation of any rights of another.

    Your use of the Application constitutes your agreement to this Disclaimer. If you do not agree with the terms of this Disclaimer, do not use the Application.

    This Disclaimer may be updated or changed without notice, and it is your responsibility to review it regularly.

    This Disclaimer is governed by Kansas Law. Any disputes arising from or in connection with this Disclaimer shall be subject to the exclusive jurisdiction of the courts of Kansas.

    THIS DISCLAIMER PROVIDES THE SOLE AND EXCLUSIVE REMEDIES AVAILABLE TO YOU IN CONNECTION WITH YOUR USE OF THE APPLICATION AND AI-GENERATED CONTENT. 
        """)
    

if __name__ == "__main__":
    main()