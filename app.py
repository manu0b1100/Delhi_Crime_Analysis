import pandas as pd
from flask import Flask
from flask import render_template, request, jsonify
from graphs import Graphs
import json

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


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


@app.route("/data")
def get_data():
    df = pd.read_csv("Dataset/master_lat_long.csv")
    return df.to_json(orient='records')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
