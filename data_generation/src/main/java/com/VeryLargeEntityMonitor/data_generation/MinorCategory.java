package com.VeryLargeEntityMonitor.data_generation;
import com.google.gson.Gson;
import java.util.Date;

public class MinorCategory{
    public transient static long id_counter = 0;
    MinorType minType;
    MajorType majType;
    int major_area_num, minor_area_num;
    transient float consumption_rate;
    float quantity;
    long unique_id, runtime;
    String item_sensed, subject_measured, sensor_location_name;
    transient boolean is_flowing=false;

    transient float prob_turn_on = 0.05f;
    int ticks_since_turn_on = 0;

    public MinorCategory(MinorType mint, MajorType majt, int major, int minor){
        major_area_num = major;
        minor_area_num = minor;
        minType = mint;
        majType = majt;
        unique_id = id_counter++;
        item_sensed = "toilet";
        subject_measured = "water";
        sensor_location_name = "bathroom";
        consumption_rate = (float)(Math.random() * 10.0f);//TODO: replace magic number
    }
    public String getMajorMinor(){
        return major_area_num+":"+minor_area_num;
    }
    public boolean hasMessage(){
        return true;
    }
    public String getMessage(){
        if(is_flowing){
            if(ticks_since_turn_on++ > 4){
                ticks_since_turn_on = 0;
                is_flowing = false;
            }
            return unique_id+","+item_sensed+","+subject_measured+","+sensor_location_name+","+consumption_rate;
        }else{
            if(Math.random() > prob_turn_on){
                is_flowing = true;
            }
            return unique_id+","+item_sensed+","+subject_measured+","+sensor_location_name+","+0;
        }
    }
    public String getMessageAsJSON(){
        //return "{\"water-sensor\": { \"sensor_id\": "+unique_id+", \"item_sensed\": \""+item_sensed+"\"+}}"
        Gson gson = new Gson();
        this.runtime = new Date().getTime();
        //long unique_id, int major_num, int minor_num,
        // float quantity, String minor_type,
        // String major_type, String item_sensed,
        // String subject_measured, String sensor_location_name
        if(is_flowing){
            quantity = consumption_rate;
            if(ticks_since_turn_on++ > 4){
                ticks_since_turn_on = 0;
                is_flowing = false;
            }
            return gson.toJson(this);
            // return gson.toJson(new WaterSensor(unique_id, major_area_num,
            //                    minor_area_num, consumption_rate, 
            //                    minType.toString(), majType.toString(),
            //                    item_sensed, subject_measured,
            //                    sensor_location_name, runtime));
        }else{
            quantity = 0.0f;
            if(Math.random() > prob_turn_on){
                is_flowing = true;
            }
            // return gson.toJson(new WaterSensor(unique_id, major_area_num,
            //                    minor_area_num, 0.0f, minType.toString(), 
            //                    majType.toString(), item_sensed, 
            //                    subject_measured, sensor_location_name,
            //                    runtime));
            return gson.toJson(this);
        }
    }
}