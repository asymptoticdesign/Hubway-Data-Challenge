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
float[][] csv;

//-----------------Setup
void setup(){
  size(500,300,P2D);
  background(0);
  smooth();
  csv = loadData("../output/duration_minutes.csv");
  for (int row = 0; row < csv.length; i++) {
    rect(csv[i] * 8, y, 8, -counts[i] * 10);
  }
}

//-----------------Interactions
void mousePressed() {
}

//-----------------Defined Functions 

float[][] loadData(String filepath) {
  String [] lines = loadStrings("../output/duration_minutes.csv");
  float[][] data = new float[lines.length][3];

  //parse values into 2d array
  for (int i=0; i < lines.length; i++) {
    String [] temp = new String [lines.length];
    temp = split(lines[i], ',');
 
    for (int j=0; j < temp.length; j++){
      data[i][j]=float(temp[j]);
    }
  }

  return data;
}

//-----------------Defined Classes
