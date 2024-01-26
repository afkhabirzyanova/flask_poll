from datetime import datetime

from flask import Flask, redirect, render_template, request
from flask_bootstrap import Bootstrap4
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

import matplotlib.pyplot as plt 
import os 
import numpy as np 
import matplotlib 
matplotlib.use('Agg')
# plt.rcParams["font.family"] = "Helvetica Neue"


app = Flask(__name__, static_url_path='/static')
bootstrap = Bootstrap4(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# правильные ответы
correct_answers = {
   'task_1': 'option3',
   'task_2': 'option2',
   'task_3': 'option4',
   'task_4': 'option3',
   'task_5': 'option1',
   'task_6': 'option4',
   'task_7': 'option2',
   'task_8': 'option4',
   'task_9': 'option3',
   'task_10': 'option1'
   }

# функция для подсчета правильных ответов на каждый вопрос
def count_correct_answers_per_task(task):
      column = getattr(Event, task)
      count_task_values = (
         db.session.query(column, func.count())
         .group_by(column)
         .order_by(column)
         .all()
         )
   
      for value, count in count_task_values:
         if value == correct_answers[task]:
             return count


class Event(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   sex = db.Column(db.String(255), nullable=False)
   age = db.Column(db.Integer, nullable=False)
   education = db.Column(db.String(255), nullable=False)
   region_born = db.Column(db.String(255), nullable=False)
   region_live = db.Column(db.String(255), nullable=False)
   task_1 = db.Column(db.String(255), nullable=False)
   task_2 = db.Column(db.String(255), nullable=False)
   task_3 = db.Column(db.String(255), nullable=False)
   task_4 = db.Column(db.String(255), nullable=False)
   task_5 = db.Column(db.String(255), nullable=False)
   task_6 = db.Column(db.String(255), nullable=False)
   task_7 = db.Column(db.String(255), nullable=False)
   task_8 = db.Column(db.String(255), nullable=False)
   task_9 = db.Column(db.String(255), nullable=False)
   task_10 = db.Column(db.String(255), nullable=False)
   your_option = db.Column(db.String(255), nullable=False)
   num_correct_answers = db.Column(db.Integer, nullable=False)


   def __str__(self):
       return (
           f"Пол: {self.sex}\n"
           f"Возраст: {self.age}\n"
           f"Регион {self.region_live}"
       )


@app.route('/', methods=['POST'])
def add_event():
   sex = request.form['eventSex']
   age = request.form['eventAge']
   education = request.form['eventEducation']
   region_born = request.form['eventRegion_born']
   region_live = request.form['eventRegion_live']
   task_1 = request.form.get('task_1')
   task_2 = request.form.get('task_2')
   task_3 = request.form.get('task_3')
   task_4 = request.form.get('task_4')
   task_5 = request.form.get('task_5')
   task_6 = request.form.get('task_6')
   task_7 = request.form.get('task_7')
   task_8 = request.form.get('task_8')
   task_9 = request.form.get('task_9')
   task_10 = request.form.get('task_10')
   your_option = request.form['eventOption']


   # считаем число правильных ответов у каждого пользователя
   num_correct_answers = 0
   for task in correct_answers:
      submitted_answer = request.form.get(task)
      if submitted_answer == correct_answers[task]:
            num_correct_answers += 1
   


   event = Event(sex=sex, 
                 age=age, 
                 education=education, 
                 region_born=region_born,
                 region_live=region_live,
                 task_1=task_1,
                 task_2=task_2,
                 task_3=task_3,
                 task_4=task_4,
                 task_5=task_5,
                 task_6=task_6,
                 task_7=task_7,
                 task_8=task_8,
                 task_9=task_9,
                 task_10=task_10,
                 your_option=your_option,
                 num_correct_answers= num_correct_answers)
   db.session.add(event)
   db.session.commit()
   return redirect('/result')


@app.route("/")
def get_page_about():
   return render_template("about.html", h1 = "Тестирование на знание диалектизмов")


@app.route("/poll")
def view_poll():
   return render_template("poll.html", h1 = "Анкета")

@app.route("/result")
def view_result():
    latest_poll_result = Event.query.order_by(Event.id.desc()).first().num_correct_answers

    if latest_poll_result:
        return render_template("result.html", h1="Ваш результат", latest_poll_result=latest_poll_result)
    else:
        return render_template("result.html", h1="Ваш результат", latest_poll_result=None)


@app.route("/events")
def view_events():
   events = Event.query.all()
   users_count = db.session.query(func.count(Event.id)).scalar()
   latest_poll_result = Event.query.order_by(Event.id.desc()).first().num_correct_answers
   mean_age = np.round(db.session.query(func.avg(Event.age)).scalar(), 2)
   mean_num_correct_answers = np.round(db.session.query(func.avg(Event.num_correct_answers)).scalar(), 2)
   
   # 
   sex_counts = db.session.query(Event.sex, db.func.count().label('count')).group_by(Event.sex).all()

   labels = [sex_count[0] for sex_count in sex_counts]
   counts = [sex_count[1] for sex_count in sex_counts]


   plt.figure()
   plt.pie(counts, 
           labels=labels,
           autopct='%1.1f%%', 
           startangle=90, 
           colors=['#dc3545', '#007bff', '#6c757d']
         #   explode=[0.01, 0.01, 0.01]
           )
   hole = plt.Circle((0, 0), 0.35, facecolor='white')
   plt.gcf().gca().add_artist(hole)
   plt.axis('equal')
   plt.title('Соотношение полов участников опроса')
   plt.savefig(os.path.join('static','pie_chart.png'), dpi=300)
   

   lnprice = db.session.query(Event.age).all()

   nuw_correct_answers_per_task = {}
   for task in correct_answers:
      if count_correct_answers_per_task(task) != None:
         nuw_correct_answers_per_task[task] = count_correct_answers_per_task(task)
      else:
         nuw_correct_answers_per_task[task] = 0 
          
   

   print(nuw_correct_answers_per_task)

   plt.figure()
   plt.bar([i for i in range(1, 11)], 
           nuw_correct_answers_per_task.values(),
           color='#007bff') 
   plt.xticks([i for i in range(1, 11)], [i for i in range(1, 11)])
   plt.title('Число верных ответов на каждый вопрос из анкеты')
   plt.xlabel('Номер вопроса из анкеты')
   plt.ylabel('Число верных ответов')
   plt.savefig(os.path.join('static', 'plot.png'), dpi=300)
   plt.close()

   # print('figure saved') 

   # lnprice=np.log(db.session.query(Event.age))
   # plt.plot(lnprice)   
   # plt.savefig('/static/new_plot.png')
   # matplotlib.pyplot.plot(lnprice)
   # matplotlib.pyplot.savefig('/static/new_plot.png')


   # task_1 = db.session.query(Event.task_1).all()
   # for i in range(1, 11):
   
           

   return render_template("events.html", 
                          h1 = "Статистика", 
                          events=events,
                          latest_poll_result=latest_poll_result,
                          users_count=users_count, 
                          mean_age=mean_age,
                          mean_num_correct_answers=mean_num_correct_answers,
                          name='pie_chart', url=os.path.join('static', 'pie_chart.png'),
                          name_2='plot', url_2=os.path.join('static', 'plot.png'))



if __name__ == "__main__":
   with app.app_context():
       db.create_all()
   app.run(debug=True)