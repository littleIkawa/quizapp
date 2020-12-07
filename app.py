from flask import Flask, render_template, request
from utils import load_data, create_queue, flagstring_to_bool

app = Flask(__name__)

class Quiz:
    question_num = 0
    view_mode = False
    random_mode = True

    def __init__(self):
        self.count = 0

    def set_params(self, question_num=0, view_mode=False, random_mode=True):
        self.count = 0
        self.correct_num = 0
        self.question_num = question_num
        self.view_mode = view_mode
        self.random_mode = random_mode

    def set_question_data(self, dataframe):
        self.data = create_queue(dataframe, num=self.question_num, randomize=self.random_mode)

    def pop_question(self):
        return self.data.popleft()

    def question_empty(self):
        return len(self.data) == 0

    def get_question_num(self):
        return self.question_num

    def display_next_question(self):
        data = self.pop_question()
        self.count += 1
        group, question_type, question_text, ans1, ans2, ans3, op1, op2, op3, op4, op5 = list(data)
        ans_set = [ans1, ans2, ans3]
        op_set = [op1, op2, op3, op4, op5]
        #question_type: 0=一問一答, 1=
        if question_type == 0:
            correct_answers = [ans1]
        elif question_type == 1:
            op1 = int(op1)
            correct_answers = []
            if op1 < 4:
                for i in range(op1):
                    correct_answers.append(ans_set[i])
            else:
                correct_answers.extend(ans_set)
                for i in range(op1-3):
                    correct_answers.append(op_set[i+1])
        else:
            correct_answers = [ans1]

        return render_template('quiz.html', question_text=question_text, question_type=question_type, correct_answers=correct_answers, question_num=self.count, viewmode=self.view_mode, num_of_answer=len(correct_answers))

    def add_correct_num(self, request=None):
        if self.view_mode:
            return
        else:
            correctness = request.form['correctness']
            if correctness == "正解":
                self.correct_num += 1

    def get_results(self):
        results = []
        results.append(f"正解数：{quizapp.correct_num}")
        return results


quizapp = Quiz()
data_df = load_data("data/data.csv")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/restart', methods=['POST'])
def restart():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    if request.method == 'POST':
        q_num = int(request.form['question_num'])
        view_mode = flagstring_to_bool(request.form['viewflag'])
        random_mode = flagstring_to_bool(request.form['randomflag'])
        quizapp.set_params(question_num=q_num, view_mode=view_mode, random_mode=random_mode)
        quizapp.set_question_data(data_df)

    return quizapp.display_next_question()


@app.route('/quiz', methods=['POST'])
def quiz():
    if request.method == 'POST':
        quizapp.add_correct_num(request=request)
        if quizapp.question_empty():
            results = quizapp.get_results()
            return render_template('result.html', results=results)
        else:
            return quizapp.display_next_question()

if __name__ == "__main__":
    app.run(debug=True)
