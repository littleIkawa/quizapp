function check_answer() {
  const question_type = parseInt(document.getElementById('type_of_question').innerHTML);
  const num_of_answers = parseInt(document.getElementById('num_of_answer').innerHTML);
  const element_answers = Array.from(document.getElementsByClassName('answertext'));

  const element_correctanswer_box = document.getElementById('output_text');
  const element_correctness_text = document.getElementById('correctness');
  const element_submit_correctness = document.getElementById('submit_correctness');
  const element_correct_answers = Array.from(document.getElementsByClassName('answer'));

  let correctness_text = '不正解';
  if (question_type === 0) {
    if (element_answers[0].value === element_correct_answers[0].innerHTML) {
      correctness_text = '正解';
    }
  } else if (question_type == 1) {
    let exist_inccorect = false;
    for(let i=0;i<num_of_answers;i++) {
      if (element_answers[i].value !== element_correct_answers[i].innerHTML) {
        exist_inccorect = true;
      }
    }
    if (!exist_inccorect) {
      correctness_text = '正解'
    }
  }
  element_correctness_text.innerHTML = correctness_text;
  element_submit_correctness.value = correctness_text;

  element_correctanswer_box.style.display = 'block';

}

function display_answer() {
  const element_correctanswer_box = document.getElementById('output_text');
  element_correctanswer_box.style.display = 'block';

}
