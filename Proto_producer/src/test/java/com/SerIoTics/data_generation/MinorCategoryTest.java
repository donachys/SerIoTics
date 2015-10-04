package com.SerIoTics.data_generation;

import junit.framework.Test;
import junit.framework.TestCase;
import junit.framework.TestSuite;

/**
 * Unit test for MinorCategory.
 */
public class MinorCategoryTest extends TestCase{

    /**
    *
    * @param testName test case name
    **/
    public MinorCategoryTest( String testName ){
      super( testName );
    }
    /**
    * @return the suite of tests being tested
    **/
    public static Test suite(){
      return new TestSuite( MinorCategoryTest.class );
    }
    private float getQuantityAsFloat(String msg){
      int comma_count = 0;
      int quantity_index = 0;
      for(int i=0; i < msg.length() && comma_count < 4; i++){
        quantity_index = i+1;
        if(msg.charAt(i) == ','){
          comma_count++;
        }
      }
      return Float.parseFloat( msg.substring(quantity_index) );
    }

    public void testQuantityIsZeroAfterFiveMessages(){
      MinorCategory mc = new MinorCategory(MinorType.BATHROOM,
                                           MajorType.HUMANITARIAN,
                                           45, 35, 10);
      String message = "";
      mc.is_flowing = true;
      for(int i=0; i < 6; i++){
        message=mc.getMessage();
      }
      float quant = getQuantityAsFloat(message);
      assertEquals( 0.0f, quant );
    }


} 

