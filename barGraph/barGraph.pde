/*
Title:
Description:
Date Started:
Last Modified:
http://asymptoticdesign.wordpress.com/
This work is licensed under a Creative Commons 3.0 License.
(Attribution - NonCommerical - ShareAlike)
http://creativecommons.org/licenses/by-nc-sa/3.0/

In summary, you are free to copy, distribute, edit, and remix the work.
Under the conditions that you attribute the work to me, it is for
noncommercial purposes, and if you build upon this work or otherwise alter
it, you may only distribute the resulting work under this license.

Of course, the conditions may be waived with permission from the author.
*/

//-----------------Globals
FloatTable data;
int rowCount;
float[] abscissa;
float[] counts;
float minX, maxX;
float minY, maxY;
float plotMinX,plotMaxX;
float plotMinY,plotMaxY;

//-----------------Setup
void setup(){
  size(800,600,P2D);
  background(0);
  strokeWeight(2);
  noFill();
  smooth();
  
  //setup data structure for csv file
  data = new FloatTable("../output/start_hour.csv");
  rowCount = data.getRowCount();
  println("Row Count " + rowCount);
  
  //setup x-axis with min and max
  abscissa = float(data.getRowNames());
  minX = abscissa[0];
  maxX = abscissa[abscissa.length - 1];
  
  //setup y-axis with min and max
  counts = new float[rowCount];
  for(int i = 0; i < abscissa.length; i++) {
    counts[i] = data.getFloat(i,0);
  }
  
  minY = min(counts);
  maxY = max(counts);

  //drawBarGraph(abscissa,counts,24);
  //daytime
  stroke(255,255,0);
  drawClock(3*width/4,height/2,abscissa,counts,12,23);
  //nighttime
  stroke(0,255,255);
  drawClock(width/4,height/2,abscissa,counts,0,11);
  
}

//-----------------Interactions
void mousePressed() {
}

//-----------------Defined Functions 
void drawBarGraph(float[] ex, float[] why, float maxValue) {
  for(int row = 0; row < rowCount; row++) {
    if(ex[row] < maxValue) {
      float x = map(ex[row],minX,maxValue,50,width-50);
      float y = map(why[row],minY,maxY,height-50,50);
      line(x,y,x,height-50);
    }
  }
}

void drawClock(float centX, float centY, float[] ex, float[] why, float minValue, float maxValue) {
  //add numbers to clock!1

  //find where the cutoff for maxValue is
  int lowIndex = int(maxX);
  int highIndex = 0;
  float arrayMax = 0;

  println(ex);
  for(int row = 0; row < rowCount; row++) {
    
    if(ex[row] <= maxValue && ex[row] >= minValue) {
      lowIndex = min(lowIndex,row);
      highIndex = max(highIndex,row);
      arrayMax = max(arrayMax,why[row]);
    }

    else {
      continue;
    }
  }
  
  //setup drawing
  pushMatrix();  
  translate(centX, centY);

  //draw each bar
  for(int row = lowIndex; row < highIndex; row++) {
    float y = map(why[row],minY,arrayMax,0,height/4-50);
    line(0,0,0,-y);
    println("Hour: " + row + "\t Counts: " + why[row]);
    rotate(TWO_PI/float(highIndex - lowIndex + 1));
  }
  
  ellipse(0,0,height/2 - 50,height/2 - 50);
  
  popMatrix();
  
}
  

//-----------------Defined Classes
