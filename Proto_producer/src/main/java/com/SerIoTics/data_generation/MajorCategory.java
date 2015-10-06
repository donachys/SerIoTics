package com.SerIoTics.data_generation;

import java.util.ArrayList;
import java.util.List;
public class MajorCategory{
    private static final int NUM_MINOR = 1250;//number of minor categories to generate

    private final MajorType type;
    private final int major_area_num;
    public List<MinorCategory> minors = new ArrayList<MinorCategory>();
    public MajorCategory(int seed, MajorType mt, int major_num){
        type = mt;
        major_area_num = major_num;
        for(int i=0; i<NUM_MINOR; i++){
            minors.add(new MinorCategory(MinorType.BATHROOM, type, seed, major_area_num, i));
        }
    }

}

