from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import os
from werkzeug.exceptions import abort
from flaskr.auth import login_required
from flaskr.db import get_db
from . import Prepocessing_sentence

def Activate():
    db = get_db()
    typo = pd.read_sql_query("SELECT * from typo",db)
    return Prepocessing_sentence.Preprocessing(typo)

def LSTM():
    db = get_db()
    dataframe=pd.read_sql_query("SELECT * from datasetprogram", db)
    from . import lstm_model
    return lstm_model.LstmModel(dataframe)

bp = Blueprint('admin', __name__,url_prefix='/admin')

# @bp.route('/perbarui_model')
def perbarui_model():
    data=LSTM()
    Activate()
    data.build_model()
    return None

@bp.route('/')
@login_required
def index():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    path = 'flaskr'
    basepath = os.path.join(path,"data","fold","kfold.csv")
    data = pd.read_csv(basepath)
    counter = []
    for x in range(0,4):
        kelas=db.execute("SELECT COUNT(score) from datasetprogram WHERE score={}".format(x)).fetchone()
        counter.append(kelas[0])
    print(counter)
    sum_training=db.execute("SELECT COUNT(score) from datasetprogram").fetchone()
    sum_typo= db.execute("SELECT COUNT(false) from typo_2").fetchone()
    sum_emoji = db.execute("SELECT COUNT(false) from emoji_2").fetchone()
    sum_emoticon = db.execute("SELECT COUNT(false) from emoticon_2").fetchone()
    statistik={
        'n_training':sum_training[0],
        'n_emoji': sum_emoji[0],
        'n_emoticon': sum_emoticon[0],
        'n_typo': sum_typo[0],
    }
    values={
        'accuracy': data['Accuracy'],
        'f1': data['F1-Score'],
        'presisi': data['Presisi'],
        'recall': data['Recall']
    }
    return render_template('admin/home.html', posts=posts,counter=counter,values=values,statistik=statistik)


@bp.route('/data_training',methods=['POST','GET'])
@login_required
def data_training():
    db = get_db()
    # x=perbarui_model()
    # print(x)
    if request.form.get('update') is not None:
        message = None
        data_update = db.execute("SELECT * from datasetprogram WHERE id=?", (request.form.get('update'),)).fetchone()
    elif request.form.get('delete') is not None:
        message = "Data Sucessfull Deleted"
        data_update = None
        db.execute("DELETE FROM datasetprogram WHERE id=?", (request.form.get('delete'),))
        db.commit()
    elif request.method == 'POST':
        data = request.form
        text1 = data["message"]
        normal = Activate()
        text2=normal.preprocessing(text1)
        score=data["score"]
        try:
            id = data["id"]
            db.execute('UPDATE dataset_baru SET real_comment=?,after_prepro=?,score=? WHERE id=?', (text1, text2,score, id,))
            message = "Successfull Update Data"
        except:
            db.execute('INSERT INTO dataset_baru (real_comment,after_prepro,score) VALUES (?,?,?)', (text1, text2,score))
            message = "Successfull Adding Data"
        finally:
            data_update = None
            db.commit()
            perbarui_model()
    else:
        message = None
        data_update = None
    data = db.execute("SELECT * from datasetprogram").fetchall()
    return render_template('admin/data_training.html',data_update=data_update,message=message,data=data)


@bp.route('/history_instagram',methods=['POST','GET'])
@login_required
def history_instagram():
    db=get_db()
    if request.method=='POST':
        if request.form.get('show') is not None:
            url=request.form.get('show')
            print(url)
            data = db.execute("SELECT * FROM history_instagram WHERE url='{}'".format(url)).fetchall()
            result=True
        else:
            result=None
            url = request.form.get('delete')
            print(url)
            db.execute("DELETE FROM history_instagram WHERE url='{}'".format(url))
            db.commit()
            data = db.execute("SELECT COUNT(url) as jumlah,url FROM history_instagram GROUP BY url").fetchall()
    else:
        db = get_db()
        data = db.execute("SELECT COUNT(url) as jumlah,url FROM history_instagram GROUP BY url").fetchall()
        result=None
    return render_template('admin/history_instagram.html',data=data,result=result)


@bp.route('/history_analysis',methods=['POST','GET'])
@login_required
def history_analysis():
    db=get_db()
    if request.method=='POST':
        url = request.form.get('delete')
        print(url)
        db.execute("DELETE FROM text_analysis WHERE id='{}'".format(url))
        db.commit()
    db = get_db()
    data = db.execute("SELECT * from text_analysis").fetchall()
    return render_template('admin/history_analisis.html',data=data)


@bp.route('/new_model',methods=['POST','GET'])
@login_required
def new_model():
    LSTM().new_model()
    return "BErhasil"


@bp.route('/barchart')
@login_required
def barchart():
    path = 'flaskr'
    basepath = os.path.join(path, "data", "fold","kfold.csv")
    data = pd.read_csv(basepath)
    values = {
        'type': "bar",
        'accuracy': data['Accuracy'],
        'f1': data['F1-Score'],
        'presisi': data['Presisi'],
        'recall': data['Recall']
    }
    return render_template('admin/chart.html', values=values)


@bp.route('/linechart')
@login_required
def linechart():
    path = 'flaskr'
    basepath = os.path.join(path, "data","fold", "kfold.csv")
    data = pd.read_csv(basepath)
    values = {
        'type':"line",
        'accuracy': data['Accuracy'],
        'f1': data['F1-Score'],
        'presisi': data['Presisi'],
        'recall': data['Recall']
    }
    return render_template('admin/chart.html',values=values)


@bp.route('/perbaikan_kata',methods=['POST','GET'])
@login_required
def perbaikan_kata():
    db = get_db()
    if request.form.get('update') is not None:
        message=None
        data_update=db.execute("SELECT * from typo_2 WHERE id=?",(request.form.get('update'),)).fetchone()
    elif request.form.get('delete') is not None:
        message = "Data Sucessfull Deleted"
        data_update=None
        db.execute("DELETE FROM typo_2 WHERE id=?", (request.form.get('delete'),))
        db.commit()
    elif request.method=='POST':
        data=request.form
        typo = data["typo"]
        correct = data["correct"]
        try:
            id = data["id"]
            db.execute('UPDATE typo_2 SET false=?,true=? WHERE id=?', (typo, correct, id,))
            message = "Successfull Update Data"
        except:
            db.execute('INSERT INTO typo_2 (false,true) VALUES (?,?)',(typo,correct,))
            message="Successfull Adding Data"
        finally:
            data_update=None
            db.commit()
    else:
        message = None
        data_update=None
    data = db.execute("SELECT * from typo_2").fetchall()
    return render_template('admin/kamus.html',data=data,message=message,data_update=data_update)


@bp.route('/emoji',methods=['POST','GET'])
@login_required
def emoji():
    db = get_db()
    if request.form.get('update') is not None:
        message=None
        data_update=db.execute("SELECT * from emoji WHERE id=?",(request.form.get('update'),)).fetchone()
    elif request.form.get('delete') is not None:
        message = "Data Sucessfull Deleted"
        data_update=None
        db.execute("DELETE FROM emoji WHERE id=?", (request.form.get('delete'),))
        db.commit()
    elif request.method=='POST':
        data=request.form
        typo = data["typo"]
        correct = data["correct"]
        try:
            id = data["id"]
            db.execute('UPDATE emoji SET false=?,true=? WHERE id=?', (typo, correct, id,))
            message = "Successfull Update Data"
        except:
            db.execute('INSERT INTO emoji (false,true) VALUES (?,?)',(typo,correct,))
            message="Successfull Adding Data"
        finally:
            data_update=None
            db.commit()
    else:
        message = None
        data_update=None
    data = db.execute("SELECT * from emoji").fetchall()
    return render_template('admin/emoji.html',data=data,message=message,data_update=data_update)


@bp.route('/emoticon',methods=['POST','GET'])
@login_required
def emoticon():
    db = get_db()
    if request.form.get('update') is not None:
        message=None
        data_update=db.execute("SELECT * from emoticon WHERE id=?",(request.form.get('update'),)).fetchone()
    elif request.form.get('delete') is not None:
        message = "Data Sucessfull Deleted"
        data_update=None
        db.execute("DELETE FROM emoticon WHERE id=?", (request.form.get('delete'),))
        db.commit()
    elif request.method=='POST':
        data=request.form
        typo = data["typo"]
        correct = data["correct"]
        try:
            id = data["id"]
            db.execute('UPDATE emoticon SET false=?,true=? WHERE id=?', (typo, correct, id,))
            message = "Successfull Update Data"
        except:
            db.execute('INSERT INTO emoticon (false,true) VALUES (?,?)',(typo,correct,))
            message="Successfull Adding Data"
        finally:
            data_update=None
            db.commit()
    else:
        message = None
        data_update=None
    data = db.execute("SELECT * from emoticon").fetchall()
    return render_template('admin/emoticon.html',data=data,message=message,data_update=data_update)


@bp.route('/statistic_model')
@login_required
def statistic_model():
    path='flaskr'
    basepath=os.path.join(path,"data","model","logger.csv")
    file=pd.read_csv(basepath)
    data={
        'accuracy':file['accuracy'],
        'loss':file['loss'],
        'epoch':file['epoch'],
        'val_accuracy':file['val_accuracy'],
        'val_loss':file['val_loss'],
    }
    report_csv = pd.read_csv(os.path.join('flaskr', "data", "confusion", "report.csv"))
    conf_mat = pd.read_csv(os.path.join('flaskr', "data", "confusion", "cf.csv"))
    classification = pd.read_csv(os.path.join('flaskr', "data", "confusion", "confusion_matrix.csv"))
    print(report_csv.iloc[:, 0])
    print(conf_mat.iloc[:, 0])
    data_y = {
        'row': classification.iloc[:, 0],
        'true': classification['true'],
        'pred': classification['pred']
    }
    report = {
        'row': report_csv.iloc[:, 0],
        'precision': report_csv['precision'],
        'recall': report_csv['recall'],
        'f1': report_csv['f1-score'],
        'support': report_csv['support'],
    }
    cf = {
        'row': conf_mat.iloc[:, 0],
        'Cyberbullying': conf_mat.iloc[:, 1],
        'Irrelevant': conf_mat.iloc[:, 2],
        'Netral': conf_mat.iloc[:, 3],
        'NonCyberbullying': conf_mat.iloc[:, 4],
    }
    return render_template('admin/model.html',data=data,report=report,cf=cf,data_y=data_y)