package com.VeryLargeEntityMonitor.data_generation;

import java.util.ArrayList;
import java.util.List;
public class MajorCategory{
    private static final int NUM_MINOR = 100;
    public static enum MajorType{ INDUSTRY, OUTDOOR, HUMANITARIAN }

    MajorType type;
    int major_area_num;
    public List<MinorCategory> minors = new ArrayList<MinorCategory>();
    public MajorCategory(MajorType mt, int major_num){
        type = mt;
        major_area_num = major_num;
        for(int i=0; i<NUM_MINOR; i++){
            minors.add(new MinorCategory(MinorCategory.MinorType.BATHROOM, major_area_num, i));
        }
    }

}

