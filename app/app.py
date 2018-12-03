from flask import Flask
from config import Configuration
from posts.about import posts
import pandas as pd
import numpy as np
import sqlalchemy as db
import matplotlib.pyplot as plt

engine = db.create_engine('postgresql+psycopg2://postgres:root@localhost:5432/simple_neural')
connection = engine.connect()

app = Flask(__name__)
app.config.from_object(Configuration)

app.register_blueprint(posts, url_prefix='/blog')

# Датасеты и полученнные из них серии посещаемости с 2007 по 2018 год, построение графиков посещаемости
atns = []
for year in range(2007, 2018):
    dataset_tmp = pd.read_sql(sql='select * from data_' + str(year) + '_' + str(year + 1), con=connection,
                              index_col=['date'], parse_dates=['date'], coerce_float=True)
    atn = dataset_tmp.attendance
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(atn, label=r"attendance")
    ax.set_xlabel(r'$Date$', fontsize=18)
    ax.set_ylabel(r'$Attendance$', fontsize=18)
    ax.set_title('Attendance ' + str(year) + ' - ' + str(year + 1))
    ax.legend(loc=2)
    fig.savefig('static/attendance_' + str(year) + '-' + str(year + 1) + '.png')
    atns.append(np.array(dataset_tmp.attendance))

# Серии столбцов
# В последнем датасете хранятся также данные о продажах
atn = dataset_tmp.attendance
dri = dataset_tmp.drinks
des = dataset_tmp.desserts
firs = dataset_tmp.firstfood
sec = dataset_tmp.secondfood
sal = dataset_tmp.salads

# график продаж по категориям 2017-2018 год
fig, ax = plt.subplots(figsize=(15, 5))
ax.plot(firs, label=r"firstfood")
ax.plot(sec, label=r"secondfood")
ax.plot(sal, label=r"salads")
ax.plot(dri, label=r"drinks")
ax.plot(des, label=r"desserts")
ax.set_xlabel(r'$Date$', fontsize=18)
ax.set_ylabel(r'$Sales$', fontsize=18)
ax.set_title('Statistics 2017 - 2018')
ax.legend(loc=2);
fig.savefig('static/sales_2017-2018.png')

# коэффициенты продаж по категориям
k_dri = (dri) / atn
k_des = (des) / atn
k_firs = (firs) / atn
k_sec = (sec) / atn
k_sal = (sal) / atn

# график коэффициентов
fig, ax = plt.subplots(figsize=(15, 5))
ax.plot(k_firs, label=r"firstfood")
ax.plot(k_sec, label=r"secondfood")
ax.plot(k_sal, label=r"salads")
ax.plot(k_dri, label=r"drinks")
ax.plot(k_des, label=r"desserts")
ax.set_xlabel(r'$Date$', fontsize=18)
ax.set_ylabel(r'$Ratio$', fontsize=18)
ax.set_title('Ratio of sales 2017 -2018')
ax.legend(loc=2);
fig.savefig('static/ratio.png')

# Датасет, из которого выводим столбец с датами для конкатинирования
dataset_2007_2008 = pd.read_sql(sql='select * from data_2007_2008', con=connection, coerce_float=True)
date = dataset_2007_2008.date

# прогнозирование посещаемости в 2018-2019 году
pred_temp = 0
for x in range(0, 10):
    pred_temp += atns[x]
    pred_temp -= atns[0]
prediction_2018_2019 = np.ceil((pred_temp - atns[0]) / 11 + atns[10]).astype(np.int64)
atn = pd.DataFrame(prediction_2018_2019)

# Конкатенирование
Frame = [date, atn]
prediction1 = pd.concat(Frame, axis=1)
prediction1.columns = ['date', 'prediction_attendance']
prediction1.to_sql(name='prediction_attendance', con=connection, if_exists='replace', index=False)

# Чтение csv файла с прогнозом посещаемости
prediction_new = pd.read_sql(sql='select * from prediction_attendance', con=connection,
                             index_col=['date'], parse_dates=['date'], coerce_float=True)
atn2 = prediction_new.prediction_attendance

# Построение графика прогноза посещаемости
fig, ax = plt.subplots(figsize=(15, 5))
ax.plot(atn2, label=r"attendance")
ax.set_xlabel(r'$Date$', fontsize=18)
ax.set_ylabel(r'$Prediction Attendance$', fontsize=18)
ax.set_title('Prediction Attendance')
ax.legend(loc=2);
fig.savefig('static/prediction_attendance.png')

# Создание отдельного датасета для записи в стобец индекос (здесь - дата), нужно для конкатенирования
dataset_help = pd.read_sql(sql='select * from prediction_attendance', con=connection, coerce_float=True)
date = dataset_help.date

# Умножение коэффициентов продаж на прогноз посещаемости для каждого дня учебного года
# Запись в DataFrame прогноза покупок 2018-2019 года, округление (np.ceil) и перевод в целые чила (astype(np.int64))
p_dri = pd.DataFrame(np.ceil(k_dri.values * atn2.values).astype(np.int64))
p_des = pd.DataFrame(np.ceil(k_des.values * atn2.values).astype(np.int64))
p_firs = pd.DataFrame(np.ceil(k_firs.values * atn2.values).astype(np.int64))
p_sec = pd.DataFrame(np.ceil(k_sec.values * atn2.values).astype(np.int64))
p_sal = pd.DataFrame(np.ceil(k_sal.values * atn2.values).astype(np.int64))

# Запись в фрейм и конкатенирование, запись во временную csv
Frame = [date, p_dri, p_des, p_firs, p_sec, p_sal]
prediction = pd.concat(Frame, axis=1)
prediction.columns = ['date', 'drinks', 'desserts', 'first_food', 'second_food', 'salads']
prediction.to_sql(name='prediction_temp', con=connection, index=False, if_exists='replace')

# Ставим в качестве индекс-столбца дату и перезаписываем
dataset_2018_2019 = pd.read_sql(sql='select * from prediction_temp',
                                con=connection, index_col=['date'], parse_dates=['date'], coerce_float=True)
dataset_2018_2019.to_sql(name='prediction_sales', con=connection, if_exists='replace', index=False)

# Чтение стобцов из таблицы с прогнозом
p_dri = dataset_2018_2019.drinks
p_des = dataset_2018_2019.desserts
p_firs = dataset_2018_2019.first_food
p_sec = dataset_2018_2019.second_food
p_sal = dataset_2018_2019.salads

# Построение графика прогнозируемых продаж на 2018-2019 год
fig, ax = plt.subplots(figsize=(15, 5))
ax.plot(p_firs, label=r"firstfood")
ax.plot(p_sec, label=r"secondfood")
ax.plot(p_sal, label=r"salads")
ax.plot(p_dri, label=r"drinks")
ax.plot(p_des, label=r"desserts")
ax.set_xlabel(r'$Date$', fontsize=18)
ax.set_ylabel(r'$Sales$', fontsize=18)
ax.set_title('Prediction Statistics 2018-2019')
ax.legend(loc=2);
fig.savefig('static/prediction_sales.png')


# p - prediction (Прогноз)
# r - revenue (Выручка)
# c - cost (Цена)
# prices = pd.read_csv('input/prices.csv',',')
prices = pd.read_sql('select * from prices', con=connection, coerce_float=True)
c_dri = prices.drinks
c_des = prices.desserts
c_firs = prices.firstfood
c_sec = prices.secondfood
c_sal = prices.salads

# Подсчет предполагаемой выручки
r_dri = pd.DataFrame(np.ceil(c_dri.values * p_dri.values).astype(np.int64))
r_des = pd.DataFrame(np.ceil(c_des.values * p_des.values).astype(np.int64))
r_firs = pd.DataFrame(np.ceil(c_firs.values * p_firs.values).astype(np.int64))
r_sec = pd.DataFrame(np.ceil(c_sec.values * p_sec.values).astype(np.int64))
r_sal = pd.DataFrame(np.ceil(c_sal.values * p_sal.values).astype(np.int64))
r_all = pd.DataFrame(r_dri + r_des + r_firs + r_sec + r_sal)

# Подсчет выручки за 2017-2018 год
r_dri_old = pd.DataFrame(np.ceil(c_dri.values * dri.values).astype(np.int64))
r_des_old = pd.DataFrame(np.ceil(c_des.values * des.values).astype(np.int64))
r_firs_old = pd.DataFrame(np.ceil(c_firs.values * firs.values).astype(np.int64))
r_sec_old = pd.DataFrame(np.ceil(c_sec.values * sec.values).astype(np.int64))
r_sal_old = pd.DataFrame(np.ceil(c_sal.values * sal.values).astype(np.int64))
r_all_old = pd.DataFrame(r_dri_old + r_des_old + r_firs_old + r_sec_old + r_sal_old)

# Запись в фрейм и конкатенирование, запись во временную csv
Frame = [date, r_dri, r_des, r_firs, r_sec, r_sal, r_all]
prediction = pd.concat(Frame, axis=1)
prediction.columns = ['date', 'drinks', 'desserts', 'first_food', 'second_food', 'salads', 'all']
prediction.to_sql(name='prediction_temp', con=connection, index=False, if_exists='replace')

# Ставим в качестве индекс-столбца дату и перезаписываем
prediction_revenue = pd.read_sql(sql='select * from prediction_temp', con=connection,
                                 index_col=['date'], parse_dates=['date'], coerce_float=True)
prediction_revenue.to_sql(name='prediction_revenue', con=connection, if_exists='replace', index=False)

# Строим график предполагаемой выручки
fig, ax = plt.subplots(figsize=(15, 5))
ax.plot(r_all, label=r"revenue")
ax.set_xlabel(r'$Date$', fontsize=18)
ax.set_ylabel(r'$Revenue$', fontsize=18)
ax.set_title('Prediction Revenue')
ax.legend(loc=2);
fig.savefig('static/prediction_revenue.png')

# Строим график сравнения выручек за 2017-2018 и 2018-2019 год
fig, ax = plt.subplots(figsize=(15, 5))
ax.plot(r_all, label=r"2018-2019")
ax.plot(r_all_old, label=r"2017-2018")
ax.set_ylabel(r'$Revenue$', fontsize=18)
ax.set_title('Compare Revenue')
ax.legend(loc=2);
fig.savefig('static/compare_revenue.png')

# Удаление ненужных таблиц
metadata = db.MetaData()
prediction = db.Table('prediction_temp', metadata, autoload=True, autoload_with=engine)
prediction.drop(engine)
prediction = db.Table('prediction_attendance', metadata, autoload=True, autoload_with=engine)
prediction.drop(engine)
prediction = db.Table('prediction_revenue', metadata, autoload=True, autoload_with=engine)
prediction.drop(engine)
prediction = db.Table('prediction_sales', metadata, autoload=True, autoload_with=engine)
prediction.drop(engine)