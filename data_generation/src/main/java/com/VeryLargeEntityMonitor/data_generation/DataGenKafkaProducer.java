package com.VeryLargeEntityMonitor.data_generation;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;

import java.util.ArrayList;
import java.util.Random;
import java.util.Properties;
import java.util.Date;
import java.util.List;
import java.util.ArrayList;

public class DataGenKafkaProducer{
    public static final int NUM_MAJOR = 10;
    public static void main(String... args){
        long events = Long.parseLong(args[0]);
        Random rnd = new Random();
        
        Properties props = new Properties();
        props.put("bootstrap.servers", "ec2-54-153-2-109.us-west-1.compute.amazonaws.com:9092,ec2-54-153-26-178.us-west-1.compute.amazonaws.com:9092,ec2-54-153-48-210.us-west-1.compute.amazonaws.com:9092");
        props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        props.put("acks", "1");

        KafkaProducer<String, String> producer = new KafkaProducer<String, String>(props);
        //create MajorCategories
        List<MajorCategory> major_categories = new ArrayList<MajorCategory>();
        
        for(int i=0; i<NUM_MAJOR; i++){
            major_categories.add(new MajorCategory(MajorCategory.MajorType.HUMANITARIAN, i));
        }
        for (long nEvents = 0; nEvents < events; nEvents++) {
            System.out.println("nEvents: " + nEvents);
            long runtime = new Date().getTime();
            //iterate through MajorCategories
            for(int i=0; i<major_categories.size(); i++){
                //iterate through MinorCategories
                MajorCategory tempMC = major_categories.get(i);
                for(int j=0; j<tempMC.minors.size(); j++){
                    //poll MinorCategories
                    String key = tempMC.minors.get(j).getMajorMinor();
                    String msg = tempMC.minors.get(j).getMessage() +","+ runtime;
                    long msg_num = (nEvents*events*major_categories.size()*tempMC.minors.size())+(i*tempMC.minors.size())+j;
                    ProducerRecord<String, String> data = new ProducerRecord<String, String>("my-topic2", key, msg_num+","+msg);
                    producer.send(data);
                }
            }
        }
        producer.close();
    }
}