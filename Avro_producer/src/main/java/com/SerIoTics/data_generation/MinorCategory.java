package com.SerIoTics.data_generation;
import com.google.gson.Gson;
import java.util.Date;

import org.apache.avro.Schema;
import org.apache.avro.generic.GenericData;
import org.apache.avro.generic.GenericRecord;
import org.apache.avro.io.*;
import org.apache.avro.specific.SpecificDatumReader;
import org.apache.avro.specific.SpecificDatumWriter;
import org.apache.avro.file.DataFileWriter;

import java.io.ByteArrayOutputStream;
import java.io.File;
import java.nio.file.Paths;
import java.nio.file.Files;
import java.io.IOException;


public class MinorCategory{
    
    MinorType minType;
    MajorType majType;
    int major_area_num, minor_area_num;
    float quantity;//sensor measurement value
    long unique_id, runtime;//device_id, unix_time of message
    String item_sensed, subject_measured, sensor_location_name;
    int ticks_since_turn_on = 0;
    
    /*non serialized variables*/
    transient static long id_counter = 0;
    transient float consumption_rate;
    transient boolean is_flowing=false;
    transient float prob_turn_on = 0.05f;
    transient float max_consumption_rate = 10.0f;
    

    public MinorCategory(MinorType mint, MajorType majt, 
                            int seed, int major, int minor){
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
    /* basic information String */
    public String getMessage(){
        if(is_flowing){
            ticks_since_turn_on++;
            if(ticks_since_turn_on > 4){
                ticks_since_turn_on = 0;
                is_flowing = false;
            }
            return unique_id+","+item_sensed+","+subject_measured+","+
                    sensor_location_name+","+consumption_rate;
        }else{
            if(Math.random() > prob_turn_on){
                is_flowing = true;
            }
            return unique_id+","+item_sensed+","+subject_measured+","+
                    sensor_location_name+","+0;
        }
    }
    /* Avro byte array */
    public byte[] getMessageAsBytes() throws IOException{

        WaterSensor ws = toWaterSensor();
        DatumWriter<WaterSensor> wsDatumWriter = 
                    new SpecificDatumWriter<WaterSensor>(WaterSensor.class);
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        BinaryEncoder encoder = EncoderFactory.get().binaryEncoder(out, null);
        wsDatumWriter.write(ws, encoder);
        encoder.flush();
        out.close();
        return out.toByteArray();
    }
    public void writeToFile(){
        try{
            Files.write(Paths.get("avromessage.txt"), getMessageAsBytes());
        }catch(IOException e){
            e.printStackTrace();
        }
    }
    /* convert this to a WaterSensor */
    private WaterSensor toWaterSensor(){
        /*
        all-args constructor
        public WaterSensor(java.lang.Float quantity, 
                           java.lang.Integer major_area_num, 
                           java.lang.Integer minor_area_num, 
                           java.lang.Integer time_since_turn_on, 
                           java.lang.Long unique_id, 
                           java.lang.Long runtime, 
                           java.lang.CharSequence minType, 
                           java.lang.CharSequence majType, 
                           java.lang.CharSequence item_sensed, 
                           java.lang.CharSequence subject_measured, 
                           java.lang.CharSequence sensor_location_name) {
            */
        this.runtime = new Date().getTime();
        if(is_flowing){
            quantity = consumption_rate;
            ticks_since_turn_on++;
            if(ticks_since_turn_on > 4){
                ticks_since_turn_on = 0;
                is_flowing = false;
            }
            return new WaterSensor(
                                 consumption_rate,
                                 major_area_num,
                                 minor_area_num,
                                 ticks_since_turn_on,
                                 unique_id,
                                 runtime,
                                 minType.toString(),
                                 majType.toString(),
                                 item_sensed,
                                 subject_measured,
                                 sensor_location_name
                                 );
            }else{
                quantity = 0.0f;
                if(Math.random() > prob_turn_on){
                    is_flowing = true;
                }
                return new WaterSensor(
                                 consumption_rate,
                                 major_area_num,
                                 minor_area_num,
                                 ticks_since_turn_on,
                                 unique_id,
                                 runtime,
                                 minType.toString(),
                                 majType.toString(),
                                 item_sensed,
                                 subject_measured,
                                 sensor_location_name
                                 );
            }
    }
    /* JSON format String */
    public String getMessageAsJSON(){
        Gson gson = new Gson();
        this.runtime = new Date().getTime();
        if(is_flowing){
            quantity = consumption_rate;
            ticks_since_turn_on++;
            if(ticks_since_turn_on > 4){
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