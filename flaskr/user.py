from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flaskr.db import get_db
import os
import pandas as pd
from flaskr.admin import Activate,LSTM
from flaskr.test import ScrapePost
bp = Blueprint('user', __name__,url_prefix='/')

@bp.route('/')
def index():
    return render_template('user/home.html')

@bp.route('/hasil',methods=['GET','POST'])
def hasil():
    if request.method=='POST':
        data = request.form
        text_real = data["kalimat"]
        text=Activate().preprocessing(text_real)
        predict=list(LSTM().predict_comment(text)*100)
        valid=LSTM().cek_validasi(text)
        label = ["Cyberbullying", "Irrelevant", "Netral", "Non Cyberbullying"]
        print(valid)
        high_prob=[]
        high_label=[]
        if(valid=="valid"):
            for x in range(len(predict)):
                if max(predict) == predict[x]:
                    high_prob.append(predict[x])
                    high_label.append(label[x])
                    predict.pop(x)
                    label.pop(x)
                    break
            db=get_db()
            db.execute('INSERT INTO text_analysis (teks,result,real_text) VALUES (?,?,?)', (text, high_label[0],text_real,))
            db.commit()
            result={
                'maximum_prob':high_prob,
                'maximum_label':high_label,
                'prob':predict,
                'label':label
            }
        else:
            label=["Tidak teridentifikasi","Tidak teridentifikasi","Tidak teridentifikasi"]
            high_label=["Tidak teridentifikasi"]
            high_prob=[0]
            predict=[0,0,0]
            db=get_db()
            db.execute('INSERT INTO text_analysis (teks,result,real_text) VALUES (?,?,?)', (text, high_label[0],text_real,))
            db.commit()
            result={
                'maximum_prob':high_prob,
                'maximum_label':high_label,
                'prob':predict,
                'label':label
            }
    else:
        text=None
        result=None
        valid=None
    db=get_db()
    data=db.execute("SELECT real_text,result from text_analysis ORDER BY id DESC LIMIT 10").fetchall()
    return render_template('user/identifikasi_komentar.html', text=text,result=result,data=data,valid=valid)

@bp.route('/instagram',methods=['GET','POST'])
def instagram():
    if request.method=='POST':
        text="aku"
        data = request.form
        url = data["url"]
        name=os.environ.get('USERNAME_INSTAGRAM')
        password=os.environ.get('PASSWORD_INSTAGRAM')
        print(name+","+password)
        tuple=ScrapePost().login_page(url,name,password)
        db=get_db()
        try:
            db.executemany('INSERT INTO history_instagram (url,score,comments,valid,username,image) VALUES (?,?,?,?,?,?)',tuple)
        except:
            db.execute(
                'INSERT INTO history_instagram (url,score,comments,valid,username,image) VALUES (?,?,?,?,?,?)', tuple)
        db.commit()
        result=db.execute("SELECT * from history_instagram WHERE url='{}'".format(url)).fetchall()
    else:
        text = ["aku"]
        db = get_db()
        url = request.args.get('url2', '')
        print(url)
        print("saya")
        result = db.execute("SELECT * from history_instagram WHERE url='{}'".format(url)).fetchall()
    db=get_db()
    data=db.execute("SELECT * from text_analysis ORDER BY id DESC LIMIT 10").fetchall()
    pengujian_terdahulu=db.execute("SELECT COUNT(url) as jumlah,url FROM history_instagram GROUP BY url LIMIT 15").fetchall()
    return render_template('user/identifikasi_instagram.html', text=text,result=result,data=data,data_other=pengujian_terdahulu)
