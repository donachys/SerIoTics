package com.VeryLargeEntityMonitor.data_generation;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;
import java.io.*;
//import com.google.gson.Gson;
import static java.util.concurrent.TimeUnit.*;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.ScheduledFuture;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;

import java.util.ArrayList;
import java.util.Random;
import java.util.Properties;
import java.util.List;
import java.util.ArrayList;

public class DataGenLogger{
    
    public static void main(String... args){
        int NUM_MAJOR = 1250;
        Random rnd = new Random();
        PrintWriter out=null;
        int seed = 0;
        try {
            out = new PrintWriter(new BufferedWriter(new FileWriter("datagen.txt", true)));
            //create MajorCategories
            List<MajorCategory> major_categories = new ArrayList<MajorCategory>();
            
            for(int i=0; i<NUM_MAJOR; i++){
                major_categories.add(new MajorCategory(seed, MajorType.HUMANITARIAN, i));
            }
            int numMessages = 100000;
            for(int nMsg=0; nMsg < numMessages; nMsg++){
                //iterate through MajorCategories
                for(int i=0; i<major_categories.size(); i++){
                    //iterate through MinorCategories
                    MajorCategory tempMC = major_categories.get(i);
                    for(int j=0; j<tempMC.minors.size(); j++){
                        //poll MinorCategories
                        String key = tempMC.minors.get(j).getMajorMinor();
                        String msg = tempMC.minors.get(j).getMessageAsJSON();
                        //System.out.println("key: " + key + " msg: " + msg);
                        //ProducerRecord<String, String> data = new ProducerRecord<String, String>("my-topic3", key, msg);
                        //producer.send(data);
                        //log
                        out.write(msg+"\n");
                    }
                }
            }
        } catch (IOException e) {
            
        }finally{
            if(out != null){
                out.close();
            }
        }
        
    }
}