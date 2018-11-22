from app import app
from flask import render_template, request, redirect


@app.route('/', methods=['GET','POST'])
def index():
    if request.method=='POST':
        year=request.form['Select']
        if year=='Прогноз':
            year=2018
        return redirect('/'+str(year))
    else:
    	return render_template('index.html')
@app.route('/<selectedyear>/', methods=['GET'])
def years(selectedyear):
    year=int(float(selectedyear))
    if year<2007 or year>2018:
        return render_template('year_nonexistent.html')
    elif year==2018:
        return render_template('prediction.html')
    else:
        yearname = str(year) + "-" + str(year + 1)
        pngname = "attendance_" + yearname + ".png"
        return render_template('year.html', pngname=pngname, yearname=yearname)