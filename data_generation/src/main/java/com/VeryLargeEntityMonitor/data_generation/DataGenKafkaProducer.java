package com.VeryLargeEntityMonitor.data_generation;
// import kafka.javaapi.producer.Producer;
// import kafka.producer.KeyedMessage;
// import kafka.producer.ProducerConfig;
import org.apache.kafka.clients.producer.KafkaProducer;
import org.apache.kafka.clients.producer.ProducerRecord;

import java.util.Random;
import java.util.Properties;
import java.util.Date;

public class DataGenKafkaProducer{

	public static void main(String... args){
		long events = Long.parseLong(args[0]);
        Random rnd = new Random();
 
        Properties props = new Properties();
        //props.put("metadata.broker.list", "ec2-54-153-2-109.us-west-1.compute.amazonaws.com:9092");
        props.put("bootstrap.servers", "ec2-54-153-2-109.us-west-1.compute.amazonaws.com:9092,ec2-54-153-26-178.us-west-1.compute.amazonaws.com:9092,ec2-54-153-48-210.us-west-1.compute.amazonaws.com:9092");
        //props.put("serializer.class", "kafka.serializer.StringEncoder");
        props.put("key.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        props.put("value.serializer", "org.apache.kafka.common.serialization.StringSerializer");
        //props.put("partitioner.class", "example.producer.SimplePartitioner");
        //props.put("serializer.class","kafka.serializer.DefaultEncoder");
        //props.put("producer.type", 1);
        //props.put("request.required.acks", "1");
        props.put("acks", "1");

 
        //ProducerConfig config = new ProducerConfig(props);
 
        KafkaProducer<String, String> producer = new KafkaProducer<String, String>(props);//config
 
        for (long nEvents = 0; nEvents < events; nEvents++) { 
            System.out.println("nEvents: " + nEvents);
               long runtime = new Date().getTime();  
               String ip = "192.168.2." + rnd.nextInt(255); 
               String msg = runtime + ",www.example.com," + ip; 
               ProducerRecord<String, String> data = new ProducerRecord<String, String>("my-topic", ip, msg);
               producer.send(data);
        }
        producer.close();
	}

}