from flask import Flask, render_template, flash, request, redirect, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, IntegerField
from operator import itemgetter

import pygal
import time
import datetime
import pprint as pp

from pygal.style import DarkSolarizedStyle
import user_projects as esc

app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'secret'


class RForm(Form):
    codelines = IntegerField('Code Lines', validators=[validators.InputRequired(message="Error")])
    commlines = IntegerField('Comments', validators=[validators.DataRequired()])
    operlines = IntegerField('Operands', validators=[validators.InputRequired()])
    addbut = SubmitField('Add')
    delbutton = SubmitField('Delete last')
    

@app.route('/')
@app.route('/home')
def index():
    return render_template('home.html')

def create_pygraph2(title, g1, g2, xlabels, l1, l2):
    graph = pygal.Line(height=420, legend_at_bottom=True, legend_at_bottom_columns=2)
    graph.title = title
    graph.x_labels = xlabels
    graph.add(g1,  l1)
    graph.add(g2,  l2)
    graph_data = graph.render_data_uri()

    return graph_data


def create_pygraph(title, g1, g2, g3, xlabels, l1, l2, l3):
    graph = pygal.Line(height=420, legend_at_bottom=True, legend_at_bottom_columns=3)
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

    project_name = request.args.get('proname')
    ddlist = esc.get_project_data(project_name)
    dlist = sorted(ddlist, key=itemgetter('insert_date'))

    linecode  = []
    linecomm  = []
    linecommp = []
    operands  = []
    operandsp = []
    dates  = []    
    zeros = []
    last_input = dlist[len(dlist) - 1]['insert_date']

    for d in dlist:
        linecode.append(d['lcode'])
        linecomm.append(d['lcom'])
        linecommp.append(d['lcom_pred'])
        operands.append(d['operands'])
        operandsp.append(d['operands_pred'])
        #dates.append(d['insert_date'])
        zeros.append(0)
        dates.append(time.strftime("%a %d %b %Y %H:%M:%S GMT", time.gmtime(d['insert_date'] / 1000.0)))

    scorecomm = []
    sc = esc.get_score(linecode[len(linecode)-1], linecomm[len(linecomm)-1], operands[len(operands)-1], "comments")
    for i in range(sc):
        scorecomm.append('*')

    pscorecomm = []
    if len(linecode) >= 2:
        sc = esc.get_score(linecode[len(linecode)-2], linecomm[len(linecomm)-2], operands[len(operands)-2], "comments")
    for i in range(sc):
        pscorecomm.append('*')

    scoreopnd = []
    sc = esc.get_score(linecode[len(linecode)-1], linecomm[len(linecomm)-1], operands[len(operands)-1], "operands")
    for i in range(sc):
        scoreopnd.append('*')

    pscoreopnd = []
    if len(linecode) >= 2:
        sc = esc.get_score(linecode[len(linecode)-2], linecomm[len(linecomm)-2], operands[len(operands)-2], "operands")
    for i in range(sc):
        pscoreopnd.append('*')

    if request.method == 'POST':
        if "delbutton" in request.form:
            p = request.args.get('proname')
            if len(dlist) > 1:
                esc.delete_last_phase(p, last_input)
            print ('* * * * * * * * * DEL * * * * * * * * *')
            return redirect(url_for('measures', proname=p))

        elif "addbut" in request.form:
            lcode = int(request.form['codelines'])
            lcome = int(request.form['commlines'])
            oper  = int(request.form['operlines'])

            esc.add_phase(project_name, lcode, lcome, oper)

            '''
            score = []
            sc = esc.get_score(lcode, lcome, oper)
            for i in range(sc):
                score.append('*')
            '''

            graph_data = create_pygraph('Comments', 'Code Lines', 'Comm Lines', 'Comm Pred',
                                        dates,
                                        linecode,
                                        linecomm,
                                        linecommp)
            p = request.args.get('proname')
            return redirect(url_for('measures', proname=p))
            #return render_template("measures.html", stars=score, pstars=pscore, gdata=graph_data, form=form, pname=request.args.get('proname'))
        

        if "commbut" in request.form:
            graph_data = create_pygraph('Comments', 'Code Lines', 'Comments', 'Comments Predicted',
                                        dates,
                                        linecode,
                                        linecomm,
                                        linecommp)
            p = request.args.get('proname')
            return render_template("measures.html", stars=scorecomm, pstars=pscorecomm,
                                gdata=graph_data, form=form, pname=request.args.get('proname'))
  
        elif "opbut" in request.form:
            graph_data = create_pygraph('Operators', 'Code Lines', 'Operators', 'Oprs Pred',
                                        dates,
                                        linecode,
                                        linecomm,
                                        linecommp)
            p = request.args.get('proname')
            return render_template("measures.html", stars=scoreopnd, pstars=pscoreopnd,
                                gdata=graph_data, form=form, pname=request.args.get('proname'))

        elif "opndbut" in request.form:
            graph_data = create_pygraph('Operands', 'Code Lines', 'Operands', 'Operands Predicted',
                                        dates,
                                        linecode,
                                        operands,
                                        operandsp)
            p = request.args.get('proname')
            return render_template("measures.html", stars=scoreopnd, pstars=pscoreopnd,
                                gdata=graph_data, form=form, pname=request.args.get('proname'))

        elif "ccbut" in request.form:
            graph_data = create_pygraph('Complexity', 'Code Lines', 'Cyclomatic C', 'CC Pred',
                                        dates,
                                        linecode,
                                        linecomm,
                                        linecommp)
            return render_template("measures.html", stars=scorecomm, pstars=pscorecomm,
                                gdata=graph_data, form=form, pname=request.args.get('proname'))

        if "commbut2" in request.form:
            graph_data = create_pygraph2('Comments Difference', 'Comments Predicted', 'Difference',
                                        dates,
                                        zeros,
                                        [a - b for a, b in zip(linecomm, linecommp)])
            p = request.args.get('proname')
            return render_template("measures.html", stars=scorecomm, pstars=pscorecomm,
                                gdata=graph_data, form=form, pname=request.args.get('proname'))
  
        elif "opbut2" in request.form:
            graph_data = create_pygraph2('Comments Difference', 'Predicted', 'Difference',
                                        dates,
                                        zeros,
                                        [a - b for a, b in zip(operands, operandsp)])
            p = request.args.get('proname')
            return render_template("measures.html", stars=scoreopnd, pstars=pscoreopnd,
                                gdata=graph_data, form=form, pname=request.args.get('proname'))

        elif "opndbut2" in request.form:
            graph_data = create_pygraph2('Operands Difference', 'Predicted', 'Difference',
                                        dates,
                                        zeros,
                                        [a - b for a, b in zip(operands, operandsp)])
            p = request.args.get('proname')
            return render_template("measures.html", stars=scoreopnd, pstars=pscoreopnd,
                                gdata=graph_data, form=form, pname=request.args.get('proname'))

        else:
            graph_data = create_pygraph2('Comments Difference', 'Predicted', 'Difference',
                                        dates,
                                        zeros,
                                        [a - b for a, b in zip(linecomm, linecommp)])
            return render_template("measures.html", stars=scorecomm, pstars=pscorecomm,
                                gdata=graph_data, form=form, pname=request.args.get('proname'))

    else:
        graph_data = create_pygraph('Comments', 'Code Lines', 'Operands', 'Oper Pred',
                                        dates,
                                        linecode,
                                        linecomm,
                                        linecommp)
        return render_template("measures.html", stars=scorecomm, pstars=pscorecomm,
                            gdata=graph_data, form=form, pname=request.args.get('proname'))


@app.route('/projects', methods=['POST', 'GET', 'PUT', 'DELETE'])
def projects():

    plist = esc.get_projects()
    plist = sorted(plist)
    if request.method == 'POST':
        if "create" in request.form:
            text = request.form['lname']
            ptext = text.lower()
            if ptext in plist or ptext == "" or ptext == " ":
                pass
            else:
                esc.create_new_project(ptext)
                plist = esc.get_projects()
                plist = sorted(plist)
            return redirect(url_for('projects', projects=plist))
            #return render_template('projects.html', projects=plist)
        else:
            for p in plist:
                if p + "del" in request.form:
                    esc.delete_project("measure_" + p)
                    plist = esc.get_projects()
                    plist = sorted(plist)
                    return redirect(url_for('projects', projects=plist))
                elif p in request.form:
                    return redirect(url_for('measures', proname=p))

    return render_template('projects.html', projects=plist)


@app.route('/account')
def account():
    return render_template('account.html')


if __name__ == '__main__':
    app.run()