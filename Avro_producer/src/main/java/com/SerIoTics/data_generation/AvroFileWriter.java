package com.SerIoTics.data_generation;
import java.io.File;
import java.io.IOException;


public class AvroFileWriter{
	public static void main(String... args){
		MinorCategory mc = new MinorCategory(MinorType.BATHROOM, MajorType.HUMANITARIAN, 1000000, 10, 200);
		mc.writeToFile();
	}
}