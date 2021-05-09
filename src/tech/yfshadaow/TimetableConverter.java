package tech.yfshadaow;

import biweekly.Biweekly;
import biweekly.ICalendar;
import biweekly.component.VEvent;
import biweekly.property.Summary;
import biweekly.util.Duration;
import biweekly.util.Frequency;
import biweekly.util.Recurrence;

import java.io.*;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Scanner;

public class TimetableConverter {
    public static void main(String[] args) {


        ICalendar ical = new ICalendar();


        Scanner scanner = new Scanner(System.in);
        System.out.println("Enter file name:");
        String filePath = scanner.nextLine();
        File file = new File(filePath);
        if (!file.isFile() || !file.exists()) {
            System.out.println("File doesn't exist or is directory!");
            return;
        }

        System.out.println("Enter the date of the first Week A Monday in the form ddmmyyyy:");
        String dateString = scanner.nextLine();

        int recurCount = 0;
        System.out.println("Enter the times of recurrence (one recurrence is one week)");
        recurCount = Integer.valueOf(scanner.nextLine());

        long startMillisLong;

        SimpleDateFormat sdf = new SimpleDateFormat("ddMMyyyy");
        try {
            Date date = sdf.parse(dateString);
            startMillisLong = date.getTime();
        } catch (Exception e) {
            System.out.println("Incorrect date format!");
            return;
        }



        try {
            InputStreamReader isr = new InputStreamReader(new FileInputStream(file));
            BufferedReader reader = new BufferedReader(isr);
            String stringBuffer = "";

            for (int i = 0; i <= 36; i++) {
                //read the first 37 lines
                reader.readLine();
            }


            for (int i = 0; i <=4; i++) {
                stringBuffer = reader.readLine().trim();
                int dateNumber = i;

                Long millisLong = startMillisLong + dateNumber * 86400000 + 27000000 ;
                while (!stringBuffer.startsWith("</tr>")) {
                    stringBuffer = reader.readLine().trim();
                    String string = stringBuffer;
                    if (string.startsWith("<td colspan=\"")) {
                        String[] strings = new String[3];
                        for (int j = 0; j <= 2; j ++) {
                            strings[j] = reader.readLine().trim();
                        }
                        long startTime = millisLong;
                        int durationInt = Integer.valueOf(string.substring(13,14));
                        String summary = strings[0].replace("<p class=\"Large\">","").replace("</p>","");
                        String location = strings[1].replace("<p class=\"Medium\">","").replace("<br></p>","").replace("<br>","/");
                        long endTime = millisLong + durationInt * 1800000;
                        millisLong = endTime;

                        //System.out.println(startTime + " " + endTime + " " + durationInt + " " + summary + " " + location);


                        VEvent event = new VEvent();
                        event.setSummary(summary);
                        if (!location.equals("")) {
                            event.setLocation(location);
                        }
                        event.setDateStart(new Date(startTime));
                        Duration duration = new Duration.Builder().minutes(durationInt * 30).build();
                        event.setDuration(duration);
                        Recurrence recur = new Recurrence.Builder(Frequency.WEEKLY).interval(1).count(recurCount).build();
                        event.setRecurrenceRule(recur);
                        ical.addEvent(event);


                        continue;
                    } else if (string.startsWith("<td bgcolor=\"#DDDDDD\"")) {
                        long startTime = millisLong;
                        long endTime = millisLong + 1800000;
                        millisLong = endTime;
                        continue;
                    } else {
                        continue;
                    }
                }
            }
            String str = Biweekly.write(ical).go();
            PrintWriter out = new PrintWriter("output.ics");
            out.println(str);
            out.close();

        } catch (Exception e) {
            e.printStackTrace();
        }


    }

}
