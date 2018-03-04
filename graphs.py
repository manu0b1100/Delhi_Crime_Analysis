import plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
import pandas as pd
from sklearn.externals import joblib
import math


class Graphs:
    def __init__(self):
        # self.df = pd.read_csv("/home/manobhav/Downloads/train.csv")
        self.ddf = pd.read_csv("Dataset/master_lat_long.csv")
        self.ddf = self.ddf[self.ddf.Long >= 0]
        self.ddf.datefrom = pd.to_datetime(self.ddf.datefrom)
        self.ddf['year'] = self.ddf.datefrom.dt.year
        self.ddf['month'] = self.ddf.datefrom.dt.month
        self.mergedf = pd.read_csv("Dataset/merged_abstract_data.csv")

    def getCrimes(self):
        return self.mergedf.columns[10:].tolist()

    def getDistricts(self):
        return self.ddf.district.unique().tolist()

    def getPstations(self, district):
        return self.ddf[self.ddf.district == district].pstation.unique().tolist()

    def getDistrict(self, lat, long):
        lat = (lat - math.floor(lat)) * 10000000
        long = (long - math.floor(long)) * 10000000
        district_predictor = joblib.load('Pickle/district_predictor.pkl')
        return {"district": district_predictor.predict([[lat, long]])[0]}

    def getPstation(self, lat, long, district):
        lat = (lat - math.floor(lat)) * 10000000
        long = (long - math.floor(long)) * 10000000
        db = joblib.load('Pickle//districtb.pkl')
        a = [lat, long]
        a.extend(db.transform([district])[0])
        pstation_predictor = joblib.load('Pickle/pstation_predictor.pkl')
        return {"pstation": pstation_predictor.predict([a])[0]}

    def HeatMap(self, selval, dis_pol):

        if selval == 'Column':
            data = pd.crosstab(self.ddf.district, self.ddf.group_charge).apply(lambda c: (c / c.sum()) * 100,
                                                                               axis=0).apply(lambda c: c.round(2),
                                                                                             axis=0)
        else:
            data = pd.crosstab(self.ddf.district, self.ddf.group_charge).apply(lambda r: (r / r.sum()) * 100,
                                                                               axis=1).apply(lambda r: r.round(2),
                                                                                             axis=1)

        # trace = go.Heatmap(z=data.values.tolist(),
        #                    x=data.columns.tolist(),
        #                    y=data.index.tolist())
        # data = [trace]
        data = ff.create_annotated_heatmap(z=data.values.tolist(),
                                           x=data.columns.tolist(),
                                           y=data.index.tolist())
        return py.offline.plot(data, include_plotlyjs=False, output_type='div')

    def LineChart(self, time1, time2):
        data = []
        val = self.ddf.groupby([time1, time2])['group_charge'].count().tolist()
        c = 0
        print(self.ddf[time2].min(), self.ddf[time2].max())

        min = 0
        max = len(self.ddf[time2].unique())

        for i in self.ddf[time1].sort_values().unique():
            data.append(go.Scatter(
                x=list(range(min, max)),
                y=val[c * max:(c + 1) * max],
                name=i

            ))
            c += 1

        return py.offline.plot(data, include_plotlyjs=False, output_type='div')

    def ViolinPlot(self, time):
        data=[]

        for charge in self.ddf.group_charge.unique().tolist():
            trace=go.Box(y=self.ddf[self.ddf.group_charge==charge].hour,name=charge)
            data.append(trace)

        return py.offline.plot(data,include_plotlyjs=False, output_type='div')

    def ScatterPlot(self, x_val, y_val):

        if y_val == 'All':
            crime = 'Total Cognizable IPC crimes'
        else:
            crime = y_val

        trace = go.Scatter(
            x=self.mergedf[x_val],
            y=self.mergedf[crime],
            mode='markers',
            text=self.mergedf['District'],
            marker=dict(
                size=20,
                color=list(range(120, 120 + len(self.mergedf['District']) * 5, 5)),
                colorscale='Viridis'
            )
        )

        data = [trace]
        return py.offline.plot(data, include_plotlyjs=False, output_type='div')

    def ProbaPlot(self, hour, district, pstation, lat, long):

        logreg = joblib.load('Pickle/logreg.pkl')
        db = joblib.load('Pickle/districtb.pkl')
        pb = joblib.load('Pickle/policeb.pkl')

        a = [float(lat), float(long), int(hour)]
        a.extend(db.transform([district])[0])
        a.extend(pb.transform([pstation])[0])

        proba = logreg.predict_proba([a])
        trace = go.Pie(labels=logreg.classes_, values=proba[0])

        return py.offline.plot([trace], include_plotlyjs=False, output_type='div')
