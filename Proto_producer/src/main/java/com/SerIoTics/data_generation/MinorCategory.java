package com.SerIoTics.data_generation;

import com.google.gson.Gson;
import java.util.Date;
import com.SerIoTics.data_generation.SensorProtos.WaterSensor;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.nio.file.Paths;
import java.nio.file.Files;
import java.io.IOException;

import com.google.protobuf.*;

public class MinorCategory{
    
    MinorType minType;
    MajorType majType;
    int major_area_num, minor_area_num;
    float quantity;
    long unique_id, runtime;
    String item_sensed, subject_measured, sensor_location_name;
    int ticks_since_turn_on = 0;
    
    transient static long id_counter = 0;
    transient float consumption_rate;
    transient boolean is_flowing=false;
    transient float prob_turn_on = 0.05f;
    transient float max_consumption_rate = 10.0f;
    

    public MinorCategory(MinorType mint, MajorType majt, int seed, int major, int minor){
        major_area_num = major;
        minor_area_num = minor;
        minType = mint;
        majType = majt;
        unique_id = seed+id_counter++;
        item_sensed = "toilet";
        subject_measured = "water";
        sensor_location_name = "bathroom";
        consumption_rate = (float)(Math.random() * max_consumption_rate);
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

    public byte[] getMessageAsBytes() throws IOException{
        this.runtime = new Date().getTime();
        if(is_flowing){
            quantity = consumption_rate;
            if(ticks_since_turn_on++ > 4){
                ticks_since_turn_on = 0;
                is_flowing = false;
            }
        }else{
            quantity = 0.0f;
            if(Math.random() > prob_turn_on){
                is_flowing = true;
            }
        }
        WaterSensor ws = WaterSensor.newBuilder()
            .setQuantity(quantity)
            .setMajorAreaNum(major_area_num)
            .setMinorAreaNum(minor_area_num)
            .setMinType(minType.toString())
            .setMajType(majType.toString())
            .setItemSensed(item_sensed)
            .setSubjectMeasured(subject_measured)
            .setSensorLocationName(sensor_location_name)
            .setUniqueId(unique_id)
            .setRuntime(runtime)
            .setTimeSinceTurnOn(ticks_since_turn_on)
            .build();
        return ws.toByteArray();
    }
    public void writeToFile(){
        try{
            Files.write(Paths.get("avromessage.txt"), getMessageAsBytes());
        }catch(IOException e){
            e.printStackTrace();
        }
    }
    public String getMessageAsJSON(){
        Gson gson = new Gson();
        this.runtime = new Date().getTime();
        if(is_flowing){
            quantity = consumption_rate;
            if(ticks_since_turn_on++ > 4){
                ticks_since_turn_on = 0;
                is_flowing = false;
            }
            return gson.toJson(this);
        }else{
            quantity = 0.0f;
            if(Math.random() > prob_turn_on){
                is_flowing = true;
            }
            return gson.toJson(this);
        }
    }
}