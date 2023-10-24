import spacy
import random

# !pip install en_core_web_sm
# !python -m spacy download en_core_web_sm
# !pip install en_core_web_sm

nlp_pipeline = spacy.load('en_core_web_sm') #using predefined English language nlp pipeline

def get_mcq(context : str, no_of_questions: int):
    document = nlp_pipeline(context)
    def multi_choice(question,correct_option,other_option,no_of_choice = 4):
        options =  correct_option + other_option
        random.shuffle(options)
        mcq = {
                "question": question,
                "options": options,
                "correct_option": correct_option
            }

        return mcq
    def generate_various_question():
        sentance = random.choice(list(document.sents))
        blank = random.choice([token for token in sentance if not token.is_punct])
        question_text = sentance.text.replace(blank.text,'__________')
        correct_option = [blank.text]
        other_option = [token.text for token in document if token.is_alpha and token.text != correct_option[0]]
        no_other_option = random.randint(1,2)
        correct_option.extend(random.sample(other_option, no_other_option))
        no_other_option = min(4 - no_other_option ,len(other_option))
        other_option = random.sample(other_option,no_other_option)
        mcq = multi_choice(question_text,correct_option,other_option)
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
context = input('Enter paragraph :')
no_of_questions = int(input('Mention number to generate :'))
mcq_questions = get_mcq(context,no_of_questions)
for question in mcq_questions:
    print(question)