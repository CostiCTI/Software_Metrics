from flask import Flask, render_template, flash, request, redirect, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, IntegerField


import pygal

import user_projects as esc

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'secret'


class RForm(Form):
    codelines = IntegerField('Code Lines', validators=[validators.InputRequired()])
    commlines = IntegerField('Comments', validators=[validators.InputRequired()])
    operlines = IntegerField('Operands', validators=[validators.InputRequired()])
    addbut = SubmitField('Add')
    

@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html')


def create_pygraph(title, g1, g2, g3, xlabels, l1, l2, l3):
    graph = pygal.Line(height=450)
    graph.title = title
    graph.x_labels = xlabels
    graph.add(g1,  l1)
    graph.add(g2,  l2)
    graph.add(g3,  l3)
    graph_data = graph.render_data_uri()

    return graph_data


@app.route('/measures', methods=['POST', 'GET', 'PUT', 'DELETE'])
def measures():

    form = RForm()

    if request.method == 'POST':
        '''
        if "addbut" in request.form:
            if True:
                lcode = int(request.form['codelines'])
                lcome = int(request.form['commlines'])
                oper  = int(request.form['operlines'])
                return render_template("measures.html", form=form)
        '''

        if "commbut" in request.form:
            graph_data = create_pygraph('Comments', 'Code Lines', 'Comm Linse', 'Comm Pred',
                                        ['0','1','2','3','4','5'],
                                        [0, 120, 180, 276, 221, 320],
                                        [0, 21, 23, 40, 42, 67],
                                        [0, 50, 70, 94, 83, 130])
            return render_template("measures.html", gdata = graph_data, form=form)
        else:
            graph = pygal.Line()
            graph.fill = True
            graph.title = 'Code metrics'
            graph.x_labels = ['0','1','2','3','4','5']
            graph.add('Lines of code',  [0, 120, 180, 276, 221, 320])
            graph.fill = False
            graph.add('Operands',  [0, 21, 23, 40, 42, 67])
            graph.add('Operands predicted',  [0, 50, 70, 94, 83, 130])
            graph_data = graph.render_data_uri()
            return render_template("measures.html", gdata = graph_data, form=form)
    else:
        graph = pygal.Line()
        graph.fill = True
        graph.title = 'Code metrics'
        graph.x_labels = ['0','1','2','3','4','5']
        graph.add('Lines of code',  [0, 120, 180, 276, 221, 320])
        graph.fill = False
        graph.add('Comments',  [0, 21, 23, 40, 42, 67])
        graph.add('Comments predicted',  [0, 50, 70, 94, 83, 130])
        graph_data = graph.render_data_uri()
        return render_template("measures.html", gdata = graph_data, form=form)


@app.route('/projects', methods=['POST', 'GET', 'PUT', 'DELETE'])
def projects():

    plist = esc.get_projects()
    if request.method == 'POST':
        if "create" in request.form:
            text = request.form['lname']
            ptext = text.lower()
            if ptext in plist or ptext == "" or ptext == " ":
                pass
            else:
                esc.create_new_project(ptext)
                plist = esc.get_projects()
            return render_template('projects.html', projects=plist)
        else:
            for p in plist:
                if p + "del" in request.form:
                    esc.delete_project("measure_" + p)
                    plist = esc.get_projects()
                    return render_template('projects.html', projects=plist)
                elif p in request.form:
                    return redirect(url_for('measures'))

    return render_template('projects.html', projects=plist)


@app.route('/account')
def account():
    return render_template('account.html')


if __name__ == '__main__':
    app.run()