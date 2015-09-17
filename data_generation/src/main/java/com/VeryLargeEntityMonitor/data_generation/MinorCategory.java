package com.VeryLargeEntityMonitor.data_generation;

public class MinorCategory{
    public static enum MinorType{ HALLWAY, KITCHEN, BATHROOM, STORAGE, CLASSROOM }
    public static long id_counter = 0;
    MinorType type;
    int major_area_num, minor_area_num;
    float consumption_rate;
    long unique_id;
    String item_sensed, subject_measured, sensor_location_name;
    boolean is_flowing=false;

    float prob_turn_on = 0.05f;
    int ticks_since_turn_on = 0;

    public MinorCategory(MinorType mt, int major, int minor){
        major_area_num = major;
        minor_area_num = minor;
        type = mt;
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
}