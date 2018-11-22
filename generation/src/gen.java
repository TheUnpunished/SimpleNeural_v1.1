/*import java.io.FileWriter;
import java.io.IOException;

public class gen {

    public static void main(String[] args) {

        //счетчик дней
        int weekend=1;

        try(FileWriter writer = new FileWriter("db.csv", false))
        {
            //для чтения csv
            writer.write("date,attendance,firstfood,secondfood,salads,drinks,desserts\n");

            //инициализация цикла по годам
            for (int year=2017; year<=2018; year++) {

                //2017 учебный год начинается с 9 месяца и заканчивается 12
                int monthstart = 9;
                int monthfinish = 12;

                //2018 учебный год начинается с 1 месяца и заканчивается 5
                if (year == 2018) {
                    monthstart = 1;
                    monthfinish = 5;
                }

                //инициализация цикла по месяцам
                for (int month = monthstart; month <= monthfinish; month++) {

                    //в остальных месяцах 31 день (не учитывая лето)
                    int countday = 31;

                    //переменная для создания реализма данных
                    int reducecount = 0;

                    //в 4, 9 и 11 месяце 30 дней
                    if (month ==  4| month ==9 | month == 11) {
                        countday = 30;
                    }

                    //в 2 месяце 28 дней
                    if (month == 2){
                        countday = 28;
                    }

                    //в 1 месяце уменьшение количества студентов на 200
                    if (month == 1){
                        reducecount = 200;
                    }

                    //в 9 месяце увеличение количества студентов на 150
                    int addcount=0;
                    if (month == 9){
                        addcount= 150;
                    }

                    //в 5 месяце уменьшение количества студентов на 100
                    if (month == 5){
                        reducecount = 100;
                    }

                    //в 12 месяце уменьшение количества студентов на 70
                    if (month == 12){
                        reducecount = 70;
                    }
                    //инициализация цикла по дням
                    for (int day = 1; day <= countday; day++) {

                        //генерация столбцов посещения и продаж
                        int atn = 900 + (int) (Math.random() * 200);
                        int drinks = 250 + (int) (Math.random() * 80);
                        int second = 180 + (int) (Math.random() * 80);
                        int first = 150 + (int) (Math.random() * 80);
                        int salads = 130 + (int) (Math.random() * 80);
                        int desserts = 120 + (int) (Math.random() * 80);

                        //первого сентября все пришли
                        if (year == 2017 & month == 9 & day == 1) {
                            atn = 1101;
                        }

                        //исключение выходных дней (воскресений)
                        boolean on = true;
                        if ((weekend == 3) | (weekend > 7 & (((weekend - 3) % 7) == 0))) {
                            on = false;
                        }

                        //вывод данных в csv

                        if (on) {
                            writer.write(day + "." + month + "." + year + "," +
                            Math.round(atn - weekend - reducecount*2.5) + "," +
                            Math.round(first + weekend / 2 - reducecount + addcount) + ","+
                            Math.round(second + weekend / 2 - reducecount + addcount) + ","+
                            Math.round(salads + weekend / 2 - reducecount/2 + addcount) + ","+
                            Math.round(drinks + weekend/1.5 - reducecount + addcount) + ","+
                            Math.round(desserts + weekend / 2 - reducecount/2 + addcount) + "\n"
                            );
                            writer.flush();
                            weekend++;
                        }
                        else{
                            weekend++;
                            continue;
                        }
                    }
                }
            }
        }
        catch(IOException ex){
            System.out.println(ex.getMessage());
        }
    }
}
*/



import java.io.FileWriter;
import java.io.IOException;

public class gen {

    public static void main(String[] args) {

        //счетчик дней
        int weekend=1;

        try(FileWriter writer = new FileWriter("attendance_2016-2017.csv", false))
        {
            //для чтения csv
            writer.write("date,attendance\n");

            //инициализация цикла по годам
            for (int year=2016; year<=2017; year++) {

                //2017 учебный год начинается с 9 месяца и заканчивается 12
                int monthstart = 9;
                int monthfinish = 12;

                //2018 учебный год начинается с 1 месяца и заканчивается 5
                if (year == 2017) {
                    monthstart = 1;
                    monthfinish = 5;
                }

                //инициализация цикла по месяцам
                for (int month = monthstart; month <= monthfinish; month++) {

                    //в остальных месяцах 31 день (не учитывая лето)
                    int countday = 31;

                    //переменная для создания реализма данных
                    int reducecount = 0;

                    //в 4, 9 и 11 месяце 30 дней
                    if (month ==  4| month ==9 | month == 11) {
                        countday = 30;
                    }

                    //в 2 месяце 28 дней
                    if (month == 2){
                        countday = 28;
                    }

                    //в 1 месяце уменьшение количества студентов на 200
                    if (month == 1){
                        reducecount = 200;
                    }

                    //в 9 месяце увеличение количества студентов на 150
                    int addcount=0;
                    if (month == 9){
                        addcount= 150;
                    }

                    //в 5 месяце уменьшение количества студентов на 100
                    if (month == 5){
                        reducecount = 100;
                    }

                    //в 12 месяце уменьшение количества студентов на 70
                    if (month == 12){
                        reducecount = 70;
                    }
                    //инициализация цикла по дням
                    for (int day = 1; day <= countday; day++) {

                        //генерация столбцов посещения и продаж
                        int atn = 900 + (int) (Math.random() * 200);
                        int drinks = 250 + (int) (Math.random() * 80);
                        int second = 180 + (int) (Math.random() * 80);
                        int first = 150 + (int) (Math.random() * 80);
                        int salads = 130 + (int) (Math.random() * 80);
                        int desserts = 120 + (int) (Math.random() * 80);


                        //исключение выходных дней (воскресений)
                        boolean on = true;
                        if ((weekend == 3) | (weekend > 7 & (((weekend - 3) % 7) == 0))) {
                            on = false;
                        }

                        //вывод данных в csv

                        if (on) {
                            writer.write(day + "." + month + "." + year + "," +
                                    Math.round(atn - weekend - reducecount*2.5-40) + "\n"
                            );
                            writer.flush();
                            weekend++;
                        }
                        else{
                            weekend++;
                            continue;
                        }
                    }
                }
            }
        }
        catch(IOException ex){
            System.out.println(ex.getMessage());
        }
    }
}
