import tkinter as tk
from tkinter import messagebox

def create_questions_file():
    try:
        with open("questions.txt", "r") as file:
            pass
    except FileNotFoundError:
        questions_content = """
        Beginner
        Which keyword defines a function in Python?;def
        What is the file extension for Cascading Style Sheets files?;.css
        What is the main function of the print statement?(one word);output
        What keyword is used to exit a function and return a value in most languages?;return
        What is the file extension for Python?;.py

        Intermediate
        What is the output of type([])?;list
        Which data type is used to store true/false values?;boolean
        Which attribute is used to specify the source URL of an image in HTML?;src
        Which CSS property is used to change the text color?;color
        Which method is used to sort a list in place?(answer with proper format);.sort()


        Advanced
        What attribute is used to specify the character encoding for an HTML document?;charset
        Which method is used to add an item to the end of a list?(answer with proper format);.append()
        What is the keyword used to specify a block of code that will run regardless of whether an exception is thrown or not?;finally
        What HTML element is used to define a division or a section?;div
        Which method is used to check if a string ends with a specified suffix in Python?;endswith
        """
        with open("questions.txt", "w") as file:
            file.write(questions_content.strip())

def load_questions():
    questions = {"beginner": [], "intermediate": [], "advanced": []}
    level = None
    try:
        with open("questions.txt", "r") as file:
            for line in file:
                line = line.strip()
                if line.lower() in questions:
                    level = line.lower()
                elif level and line:
                    question, answer = line.split(';')
                    questions[level].append((question, answer))
    except IOError:
        print("An error occurred while reading the questions file.")
    return questions

def start_quiz():
    username = username_entry.get().strip()
    if not username:
        tk.messagebox.showerror("Error", "Please enter a username.")
        return

    level = level_choice.get().lower()
    if level not in ["beginner", "intermediate", "advanced"]:
        tk.messagebox.showerror("Error", "Please select a valid level.")
        return

    questions = level_questions[level]
    num_questions = len(questions)
    score = 0
    current_question = 0

    quiz_window = tk.Toplevel(root)
    quiz_window.title("Quiz")
    quiz_window.geometry("1000x600")

    question_label = tk.Label(quiz_window, text=questions[current_question][0], wraplength=400, font=("Verdana", 20))
    question_label.pack(pady=15)

    answer_entry = tk.Entry(quiz_window, font=("Verdana", 20))
    answer_entry.pack(pady=15)

    def submit_answer():
        nonlocal score
        user_answer = answer_entry.get().strip().lower()
        correct_answer = questions[current_question][1].strip().lower()
    
        if not user_answer:
            status_label.config(text="Please provide an answer.", fg="red")
            return
    
        if user_answer == correct_answer:
            score += 1
            status_label.config(text=f"Correct!\n\nScore: {score}", fg="green")
        else:
            status_label.config(text=f"Wrong. The correct answer is: {correct_answer}", fg="red")
        answer_entry.delete(0, tk.END)
        quiz_window.after(1000, next_question)

    def next_question():
        nonlocal current_question
        current_question += 1
        if current_question < num_questions:
            question_label.config(text=questions[current_question][0])
            status_label.config(text="")
        else:
            finish_quiz()

    def finish_quiz():
        messagebox.showinfo("Quiz Finished", f"Quiz finished! Your score: {score}/{num_questions}")
        quiz_window.destroy()
        write_score_to_file(username, score, num_questions)
        display_high_scores()

    def write_score_to_file(username, score, total_questions):
        try:
            with open("quiz_scores.txt", "a") as file:
                file.write(f"{username},{score},{total_questions}\n")
        except IOError:
            print("An error occurred while writing the score to the file.")

    def quit_quiz():
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            quiz_window.destroy()
        else:
            return

    submit_button = tk.Button(quiz_window, text="Submit", command=submit_answer, font=("Verdana", 15), bg="blue", fg="white")
    submit_button.pack(pady=10)

    quit_button = tk.Button(quiz_window, text="Quit", command=quit_quiz, font=("Verdana", 15), bg="red", fg="white")
    quit_button.pack(pady=10)
    
    status_label = tk.Label(quiz_window, text="", font=("Verdana", 20))
    status_label.pack(pady=15)
    
    high_scores_label = tk.Label(quiz_window, text="High Scores:", font=("Verdana", 20, "bold"))
    high_scores_label.pack(pady=20)
    high_scores_text = tk.Text(quiz_window, height=10, width=50, state=tk.DISABLED, font=("Verdana", 15))
    high_scores_text.pack(pady=15)
    display_high_scores(high_scores_text)

def display_high_scores(text_widget=None):
    try:
        with open("quiz_scores.txt", "r") as file:
            scores = [line.strip().split(',') for line in file]
        scores = [(username, int(score), int(total_questions)) for username, score, total_questions in scores]
        scores.sort(key=lambda x: x[1], reverse=True)

        high_scores = ""
        for score in scores[:10]:
            high_scores += f"Username: {score[0]}, Score: {score[1]}/{score[2]}\n"

        if text_widget:
            text_widget.config(state=tk.NORMAL)
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, high_scores)
            text_widget.config(state=tk.DISABLED)
    except FileNotFoundError:
        with open("quiz_scores.txt", "w") as file:
            pass
    except IOError:
        print("An error occurred while reading the high scores file.")

root = tk.Tk()
root.title("BRAINBUSTERS: Programming Edition")
root.geometry("900x500")

create_questions_file()

welcome_label = tk.Label(root, text="Welcome to BRAINBUSTERS: Programming Edition!", font=("Times", 25, "bold"))
welcome_label.pack(pady=50)

username_label = tk.Label(root, text="Enter your username:", font=("Verdana", 18))
username_label.pack()
username_entry = tk.Entry(root, font=("Verdana", 18))
username_entry.pack(pady=15)

level_choice = tk.StringVar(root)
level_choice.set("Select Difficulty Level")
level_option_menu = tk.OptionMenu(root, level_choice, "Beginner", "Intermediate", "Advanced")
level_option_menu.config(font=("Verdana", 15))
level_option_menu.pack(pady=20)

start_button = tk.Button(root, text="Start Quiz", command=start_quiz, font=("Verdana", 15), bg="green", fg="white")
start_button.pack(pady=10)

quit_button = tk.Button(root, text="Quit", command=root.destroy, font=("Verdana", 15), bg="red", fg="white")
quit_button.pack(pady=15)

level_questions = load_questions()

root.mainloop()
