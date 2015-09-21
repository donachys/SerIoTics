package com.VeryLargeEntityMonitor.data_generation;

public class WaterSensor{
    long unique_id, unix_time;
    int major_area_num, minor_area_num;
    float quantity;
    String minor_type_name, major_type_name, item_sensed, subject_measured, sensor_location_name;
    public WaterSensor(long unique_id, int major_num, int minor_num,
                        float quantity, String minor_type,
                        String major_type, String item_sensed,
                        String subject_measured, String sensor_location_name,
                        long runtime){
        this.unique_id = unique_id;
        this.major_area_num = major_num;
        this.minor_area_num = minor_num;
        this.quantity = quantity;
        this.minor_type_name = minor_type;
        this.major_type_name = major_type;
        this.item_sensed = item_sensed;
        this.subject_measured = subject_measured;
        this.sensor_location_name = sensor_location_name;
        this.unix_time = runtime;
    }
}