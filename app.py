from flask import Flask, render_template, request,redirect,flash,session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import s_survey 

app = Flask(__name__)
app.config["SECRET_KEY"] = "fishpaste453"

debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

RESPONSES = "responses"

@app.route('/')
def survey_home():
   """Select survey"""
   return render_template("survey_start.html", survey=s_survey)

@app.route('/start')
def survey_start():
   """Begin survey"""

   session["RESPONSES"] = []
   return redirect("/questions/0")

@app.route('/questions/<int:qid>')
def show_question(qid):
   """Display questions"""
   responses = session.get(RESPONSES)
   
   if responses is None:
      return redirect ("/")
   
   if (len(responses) == len(s_survey.questions)):
      return redirect("/completed")
   
   if (len(responses)) != qid:
      flash(f"Invalid question id: {qid}")
      return redirect(f"/questions/{len(responses)}")
   
   question = s_survey.questions[qid]
  
   return render_template("questions.html", question_num=qid, question=question)
   
   

@app.route('/answer', methods=["POST"])
def question_response():
   """Get answers and continue survey"""
   choice = request.form["answer"]
   responses = session["RESPONSES"]
   RESPONSES.append(choice)
   session["RESPONSES"] = responses

   if (len(responses) == len(s_survey.questions)):
      return redirect("/complete")
   
   else:
     return redirect(f"/questions/{len(responses)}")
   

@app.route("/completed")
def finish_survey():
   """Show Thank you page for completing survey"""
   return render_template("completed.html")
   
   
   


   

