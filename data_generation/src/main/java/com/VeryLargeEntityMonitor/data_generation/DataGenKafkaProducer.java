package com.VeryLargeEntityMonitor.data_generation;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;

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

public class DataGenKafkaProducer{
    public static final int NUM_MAJOR = 100;
    private static final ScheduledExecutorService scheduler = Executors.newScheduledThreadPool(4);

        public static void main(String... args){
            if(args.length != 3){
                System.out.println("args: <seed> <delay> <duration>");
                System.exit(0);
            }
            int seed = Integer.parseInt(args[0]);
            long delay = Long.parseLong(args[1]);
            long duration = Long.parseLong(args[2]);
            System.out.println("delay: " + delay + " duration: " + duration);
            Random rnd = new Random();
            Properties props = new Properties();
            props.put("bootstrap.servers", "ec2-54-219-131-191.us-west-1.compute.amazonaws.com:9092,ec2-54-219-135-236.us-west-1.compute.amazonaws.com:9092,ec2-54-219-166-112.us-west-1.compute.amazonaws.com:9092,ec2-54-219-135-254.us-west-1.compute.amazonaws.com:9092");
            props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
            props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");
            props.put("acks", "1");

            KafkaProducer<String, String> producer = new KafkaProducer<String, String>(props);
            //create MajorCategories
            List<MajorCategory> major_categories = new ArrayList<MajorCategory>();
            
            for(int i=0; i<NUM_MAJOR; i++){
                major_categories.add(new MajorCategory(seed, MajorType.HUMANITARIAN, i));
            }
            final Runnable sendData = new Runnable() {
                public void run() { 
                    //iterate through MajorCategories
                    for(int i=0; i<major_categories.size(); i++){
                        //iterate through MinorCategories
                        MajorCategory tempMC = major_categories.get(i);
                        for(int j=0; j<tempMC.minors.size(); j++){
                            //poll MinorCategories
                            String key = tempMC.minors.get(j).getMajorMinor();
                            String msg = tempMC.minors.get(j).getMessageAsJSON();
                            System.out.println("key: " + key + " msg: " + msg);
                            ProducerRecord<String, String> data = new ProducerRecord<String, String>("my-topic2", key, msg);
                            producer.send(data);
                        }
                    }
                }
            };
            final ScheduledFuture<?> dataGenHandle = scheduler.scheduleAtFixedRate(sendData, delay, delay, SECONDS);
                scheduler.schedule(new Runnable() {
                    public void run() { dataGenHandle.cancel(true); producer.close(); }
                }, duration, SECONDS);
        }
}