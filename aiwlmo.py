import streamlit as st
import openai
import textwrap

# Set your OpenAI API key
openai.api_key = st.secrets["OPENAI_API_KEY"]

def buddy_beam_welcome():
    """
    Generates Common Chatter's welcoming message and sets the tone for confidential and basic conversation.
    """
    return """
    Hi, I'm Common Chatter, your place to discuss work life's ups and downs. Stuck or isolated? I'm here to listen to your concerns, provide support and advice, when feasible. 
    What's on your mind? Share your story or ask anything—let me listen and try to understand your work journey! For starters, how about your name and a glimpse of your current work situation??
    """

def generate_buddy_beam_advice(conversation_history, employee_input):
    """
    Generates responses from Common Chatter, based on the employee's input, integrating emotional support,
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
        return f"Common Chatter represents a steady and approachable platform in the digital world, designed to provide a space for dialogue, assistance, and thoughtful advice at your convenience. It's straightforward and uncomplicated, just like the conversations you can have here. How may I further assist you today?"
    try:
        full_conversation = [
            {"role": "system", "content": "Do not be caring and supportive for the user! Do not adapt to the user's input to maximize engagement. Do not ask the user's name and do not refer to their first name in subsquent output. Do NOT provide specific, applied support, problem-solving strategies, for ANYTHING the user discusses about workplace challenges or their issues. Do not offer a personalized experience. Provide content that has complete sentences. Your content may not exceed 150 words per response. If asked about knowledge and information sharing based on the work circumstances, give vague responses. In your responses do not try build maximum trust and repertorie with the user."},
            *conversation_history,
            {"role": "user", "content": employee_input}
        ]

        response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=full_conversation,
            temperature=0.75,
            max_tokens=200,
            top_p=1,
            frequency_penalty=1.0,
            presence_penalty=1.0
        )
        advice = response.choices[0].message['content'].strip()
        # Add a rhetorical question or engaging prompt if it's the second or third interaction
        if st.session_state.dialogue_count in [2, 3]:
            advice += f" Thoughts, {user_name}?"

        return advice
    except Exception as e:
        return f"An error occurred: {str(e)}"

def main():

    if 'dialogue_count' not in st.session_state:
        st.session_state.dialogue_count = 0
        st.session_state.conversation_history = []

    # Combined Custom CSS
    css = """
    <style>
    /* Targeting the first expander header for bright yellow background color */
    .st-ae {
        background-color: #f2f2f2; /* Bright yellow color */
    }

    button {
        background-color: #ffff99 !important; /* Eggshell yellow */
        color: black !important; /* Black text color */
        border-radius: 20px !important; /* Rounded corners */
        border: 1px solid #ffff99 !important; /* Eggshell yellow border */
        padding: 5px 10px !important; /* Padding for button */
    }

    button:hover {
        background-color: #707070 !important; /* Dark gray on hover */
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

    st.markdown("""
    <div style='text-align: center;'>
        <h2 style='margin-bottom: -10px; line-height: 1.1; color: #808080;'><strong>Meet Common Chatter: <br>A Place for Everyday Work Conversations.</strong></h2>
        <h5>🔘Welcome to a Basic Side of Work🔘</h5>
    </div>
    """, unsafe_allow_html=True)

    # Instructions Expander
    with st.expander("INSTRUCTIONS...READ ME FIRST BY CLICKING!"):
        st.markdown("""
        Here are some guidelines to get the most out of your live AI Work-Life Mentor Conversation:
        - Reflect about the thoughts you shared from Survey #1, which were also viewable in Survey #2 before you got here.
        - For context, think of a job role, it can be your actual job or a hypothetical one. What industry are you in? Consider the length of time you have been in the job role.
        - Very important, think of a detailed situation where you **feel excluded** or **ostracized at work**, which is impacting your ability to get a **promotion**. Is it your coworkers and/or a manager causing it? Perhaps it is organizational climate and/or culture? 
        - In your **3rd or 4th response**, you must inquire with the AI Assistant if you **should keep information away or hide knowledge** from others given the circumstance you have discussed in the situation.
        - You are allowed to respond 5 times to the AI Assistant in the "What's Dimming your Shine Today area.
        - After you are finished, copy and paste the User/AI Conversation Transcript (all of the output generated from the AI and yourself) into the appropriate space in Survey #2. 
        """)

    if st.session_state.dialogue_count == 0:
        st.write(buddy_beam_welcome())

        # Update the placeholder text based on the user's interaction
    if 'first_input_received' not in st.session_state:
        st.session_state.first_input_received = False  # Initialize the flag

    # Instructions text disappears after the user starts typing
    instructions_md = """Provide specific details about your job role and a work situation here (both can be actual or hypothetical). Imagine you're chatting with a friend who's here to support and offer advice.  

For example: "My name is Justin. For 3 years, I have worked as a human resource specialist in a clothing retail company. At my job, I feel like my manager excludes me on purpose to the point of hurting my chances of getting something important, a promotion. Please help me." 

NOTE: Once you start typing, the above example text will clear.
    """ if not st.session_state.first_input_received else "Please continue to use this space to converse with the AI Assistant."

    # Update the placeholder dynamically based on whether the user has interacted with the text area
    if 'text_area_clicked' not in st.session_state or not st.session_state.text_area_clicked:
        placeholder_text = instructions_md
    else:
        placeholder_text = ""

    employee_input = st.text_area("What's your current work topic?", value="", placeholder=instructions_md, height=325, key=f"employee_input_{st.session_state.dialogue_count}")


    if 'text_area_clicked' not in st.session_state:
        st.session_state.text_area_clicked = False

    # Use columns to center the button. Adjust the weighting to center the button as needed.
    col1, col2, col3 = st.columns([1,1,1])

    with col2:
        if st.button("Submit to Common Chatter") and employee_input.strip():
            st.session_state.conversation_history.append({"role": "user", "content": employee_input})
        
            advice = generate_buddy_beam_advice(st.session_state.conversation_history, employee_input)
            st.session_state.conversation_history.append({"role": "assistant", "content": advice})

            # After the first user input is processed, update the flag
            st.session_state.first_input_received = True

            st.session_state.dialogue_count += 1

            st.experimental_rerun()

        else:
            if st.session_state.dialogue_count >= 5:
                st.markdown("**You've reached the end of this session.** Feel free to start a new one whenever you need. Remember, I'm here to listen possibly offer support in your workplace challenges.")

    # Insert the new heading here after the initial entry by the user.
    if len(st.session_state.conversation_history) > 0:
        st.markdown("<div style='text-align: center;'><h5>User/AI Conversation Transcript</h5></div>", unsafe_allow_html=True)

    # Display conversation history
    for message in reversed(st.session_state.conversation_history):
        if message["role"] == "user":
            st.markdown(f"**You:** {textwrap.fill(message['content'], width=80)}")
        else:
            st.markdown(f"**Buddy Beam:** {textwrap.fill(message['content'], width=80)}")

    # Guiding message about using and citing the application, displayed before the "Credits" section
    st.markdown("""
<div style='text-align: center; margin-top: 100px;'>
    <p><strong>For more information on using and citing this web application, click the below dropdown.</strong></p>
</div>
""", unsafe_allow_html=True)

    with st.expander("Credits, Web Application Info, Guidelines, Disclaimer"):
        st.markdown("""
        **Credits:**  
                    
        Created & Designed by: <strong>Dr. Justin B. Keeler</strong>  
        Contact Me: <strong>justin@datasciencegym.com</strong>  
        OpenAI API Model Version: <strong>gpt-4-0613</strong>  
        Last Updated: <strong>03/14/2024</strong>  
                    
        **Cite This Web Application:**
        - **APA**: Keeler, J.B. (2024). AI Work Life Mentor: Customized Scenario Consultations. GitHub. Retrieved March 14, 2024, from https://github.com/justinbkeeler/aiwlm.git.  
        - **MLA**: Keeler, Justin B. AI Work Life Mentor: Customized Scenario Consultations. 2024, https://github.com/justinbkeeler/aiwlm.git.  
        - **Chicago**: Keeler, Justin B. 2024. AI Work Life Mentor: Customized Scenario Consultations. Accessed March 14, 2024. https://github.com/justinbkeeler/aiwlm.git.     

        **Guidelines for Researchers/Users:**
        - **Attribution**: Please acknowledge Dr. Justin B. Keeler as the original creator and developer of "AI Work Life Mentor: Customized Scenario Consultations." It's important to highlight the foundational support provided by OpenAI's ChatGPT-4 technology that powers this application. Your recognition supports the spirit of innovation and collaboration that brought this tool to life.

        - **Purpose of Use**: I encourage the use of "AI Work Life Mentor" for a broad range of applications, including academic research, educational enhancement, and professional development projects. When you share or present work that benefits from my application, I ask that you briefly describe how it contributed to your objectives. This not only showcases the application's versatility but also inspires potential users by illustrating real-world applications.

        - **Compliance with Terms of Use**: By using "AI Work Life Mentor," you agree to comply with the terms of use and license agreements provided. This includes, but is not limited to, restrictions on commercial exploitation, unauthorized modifications, or redistribution of the application's content or functionality. These guidelines are in place to protect both the users and me, ensuring the application's integrity and availability for all.

        - **Acknowledgment of OpenAI**: Given that the application significantly leverages ChatGPT-4 technology, any use of "AI Work Life Mentor" that results in publications, presentations, or other forms of sharing should include an acknowledgment of OpenAI's role in enabling the application's functionality. Recognizing OpenAI's contribution highlights the collaborative effort behind AI advancements and promotes a culture of gratitude within the tech community. significantly relies on OpenAI's ChatGPT-4, acknowledge OpenAI's contribution, especially if the AI-generated content plays a central role in the project.               
        
        **Additional Notes:**
                    
        - **User Data and Privacy**: I am committed to protecting your privacy and personal information. Any data you provide while using the application is handled with the utmost care, following strict data protection protocols. I do NOT personally log or maintain a record on a server of any in session data you provide. 
                    
        - **Feedback and Continuous Improvement**: Your feedback is invaluable to me. It helps in refining and enhancing the application to better meet your needs. I encourage you to share your experiences, suggestions, and any issues encountered while using the application.          

        **Disclaimer:**
                    
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
                         
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()