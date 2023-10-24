import streamlit as st
from streamlit_option_menu import option_menu
import random
import spacy

with st.sidebar:
    selected = option_menu("NLP Assignment", ["Home", 'Generate MCQ'], 
        icons=['house', 'gear'])

if selected == "Home":
    st.markdown("In natural language processing. You will be tasked with developing a solution that can automatically generate objective questions with multiple correct answers based on a given chapter from a subject.The generated questions should test the reader's understanding of the chapter and have more than one possible correct answer to increase the complexity and challenge of the questions.The generated questions should not only test the reader's comprehension of the chapter but also encourage them to think beyond the surface level and explore different perspectives and possibilities. Ultimately, the objective of this project is to develop a robust and accurate solution that can aid educators in creating engaging and challenging assessments for their students.")
if selected == "Generate MCQ":
    st.markdown("MCQ")
    nlp_pipeline = spacy.load("en_core_web_sm")

    def get_mcq(context: str, no_of_questions: int):
        document = nlp_pipeline(context)

        def multi_choice(question, correct_option, other_option, no_of_choice=4):
            options = correct_option + other_option
            random.shuffle(options)
            mcq = {
                "question": question,
                "options": options,
                "correct_option": correct_option
            }
            return mcq

        def generate_various_question():
            sentence = random.choice(list(document.sents))
            blank = random.choice([token for token in sentence if not token.is_punct])
            question_text = sentence.text.replace(blank.text, "__________")
            correct_option = [blank.text]
            other_option = [token.text for token in document if token.is_alpha and token.text != correct_option[0]]
            no_other_option = random.randint(1, 2)
            correct_option.extend(random.sample(other_option, no_other_option))
            no_other_option = min(4 - no_other_option, len(other_option))
            other_option = random.sample(other_option, no_other_option)
            mcq = multi_choice(question_text, correct_option, other_option)
            return mcq

        questions = [generate_various_question() for _ in range(no_of_questions)]
        mca_questions = []
        for i, question in enumerate(questions, start=1):
            question_str = f"Q{i}: {question['question']}\n"
            options_str = ""
            for j, option in enumerate(question['options']):
                options_str += f"{j+1}. {option}\n"

            correct_options_formatted = " & ".join([f"({chr(97+question['options'].index(ans))})" for ans in question['correct_option']])
            correct_options_str = f"Correct Options: {correct_options_formatted}"

            mca_question = f"{question_str}{options_str}{correct_options_str}\n"
            mca_questions.append(mca_question)

        return mca_questions

    context = st.text_input("Enter paragraph:")
    no_of_questions = st.number_input("Insert a number", value=0)
    if st.button("Submit"):
        mcq_questions = get_mcq(context, no_of_questions)
        for question in mcq_questions:
            st.markdown(question)
