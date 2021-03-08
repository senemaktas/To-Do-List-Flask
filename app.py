from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app= Flask(__name__)
# herşey test.db'de depolanacak.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app) # database'i başlatmak için.

# db iceriginin nasil olacagini tanimladik.
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # id degeri verildi.
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow) # zamani alir.

    def __repr__(self):
        return '<Task %r>' % self.id  # task ve idsini dondurur

@app.route('/', methods=['POST', 'GET']) # db ye veri göndermek için post-get
def index():
    # taski alip dbye yazar.
    if request.method == 'POST':  
        # forma input idsi olan content gecildi,index.html deki input text idsi
        task_content = request.form['content']
        #yeni nesne (task) icin model cagrildi, content databasedeki content sutunudur.
        new_task = Todo(content=task_content)

        # yeni task db ye eklenir,commit edilir ve anasayda kalinir
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')  # task eklenir ve anasayfada kalinir.
        except:
            return 'There was an issue adding your task' # eklenemez ise mesaji yazar.

    else:
        # taskleri date 2 gore siraliyor
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

# silme islemi id degerine gore yapiliyor, indexte tanimlandi
@app.route('/delete/<int:id>')
def delete(id):
    # task id sini alir varsa ya da 404 doner
    task_to_delete = Todo.query.get_or_404(id)

    # id sini aldigi task in db den silinmesinin saglar
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/') # home page de kalir
    except:
        return 'There was a problem deleting that task'

# guncelleme islemi id ye gore yapiliyor yine, update.html acildi
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    # task id sini alir varsa ya da 404 doner
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']
        
        # sadece commit ederiz, ekleme degil guncelleme yapiyoruz
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
