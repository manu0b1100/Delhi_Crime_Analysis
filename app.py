import pandas as pd
from flask import render_template
from graphs import Graphs
import json
import os
from flask import Flask, flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'Uploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','csv'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.secret_key = "super secret key"

@app.route("/")
def index():
    return render_template("visulization.html")


@app.route("/analysis")
def analysis():
    g = Graphs()
    return render_template("analysis.html", crimes=['All'] + g.getCrimes())


@app.route("/prediction")
def test():
    g = Graphs()
    return render_template("testgeomap.html", districts=g.getDistricts(), pstations=['Select District'])


@app.route("/calc_func", methods=['POST'])
def calc_func():
    print('func called')
    if request.form['function'] == 'heatmap':
        g = Graphs()
        return g.HeatMap(request.form['sel_val'], request.form['dis_pol'])
    if request.form['function'] == 'linechart':
        g = Graphs()
        return g.LineChart(request.form['time1_val'], request.form['time2_val'])
    if request.form['function'] == 'violinchart':
        g = Graphs()
        return g.ViolinPlot(request.form['time_val'])
    if request.form['function'] == 'scatterchart':
        g = Graphs()
        return g.ScatterPlot(request.form['x_val'], request.form['y_val'])
    if request.form['function'] == 'probachart':
        g = Graphs()
        print(request.form['lat'])
        return g.ProbaPlot(request.form['hour'], request.form['district'], request.form['pstation'],
                           request.form['lat'], request.form['long'])


@app.route("/getpoliceStation", methods=['POST'])
def getPoliceStation():
    g = Graphs()
    pstations = g.getPstations(request.form['district'])
    return json.dumps(pstations)


@app.route("/predictDistrict", methods=['POST'])
def setDistrict():
    g = Graphs()
    return json.dumps(g.getDistrict(float(request.form['lat']), float(request.form['long'])))


@app.route("/predictPstation", methods=['POST'])
def setPstation():
    g = Graphs()
    return json.dumps(g.getPstation(float(request.form['lat']), float(request.form['long']), request.form['district']))



@app.route("/settings", methods=['GET'])
def get_settings():
    df = pd.read_csv("Uploads/user_dataset.csv")
    df_columns=list(df.columns)
    needed_columns=['datefrom', 'district','link', 'pahar', 'pstation','group_charge', 'hour','Lat', 'Long']
    required=['Lat','Long']
    return render_template("settings.html", columns=df_columns, needed_columns=needed_columns, required=required)


@app.route("/settings", methods=['POST'])
def post_settings():

    df = pd.read_csv("Uploads/user_dataset.csv")

    for item,val in request.form.items():
        if val=="":
            if item=="hour":
                df[item]=0
            elif item=="district":
                df[item]="No District"
            elif item=="datefrom":
                df[item]="2017-01-05"
            elif item=="group_charge":
                df[item] ="No Charge"
            elif item=="link":
                df[item] ="#"
            elif item=="pahar":
                df[item]=0

        else:
            df.rename(columns={str(val):str(item)}, inplace=True)
    df.datefrom=pd.to_datetime(df.datefrom, errors='ignore')
    try:
        df.hour=pd.to_datetime(df.hour,errors='ignore').dt.hour
    except:
        pass
    df.to_csv("Uploads/user_dataset.csv", index=False)
    session['user_data']=True

    return redirect(url_for("index"))





@app.route("/data")
def get_data():
    if 'user_data' in session and session['user_data']==True:
        df = pd.read_csv("Uploads/user_dataset.csv")
    else:
        df= pd.read_csv("Dataset/master_lat_long.csv")
    return df.to_json(orient='records')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = "user_dataset.csv"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('get_settings'))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
