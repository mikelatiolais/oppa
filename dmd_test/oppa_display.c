#include "oppa_display.h"
#include <stdio.h>

UINT8 oppadmd[OPPA_NUM_DMD_FRAMES][4096];

/* Set up initial DMD pin configuration */
void oppaInitDMD() {
  wiringPiSetup();
  pinMode(pinDisplayEnable, OUTPUT);
  pinMode(pinRowData, OUTPUT);
  pinMode(pinRowClock, OUTPUT);
  pinMode(pinColLatch, OUTPUT);
  pinMode(pinDotClock, OUTPUT);
  pinMode(pinDotData, OUTPUT);
}

/* Take in array and update the DMD directly */
void oppaUpdateDMD(UINT8 *dotData) {
  printf("Print update DMD\n");
  for(int i = 0; i < OPPA_NUM_OF_BYTES; i++) {
    printf("%d\n",dotData[i]);
    shiftOut(pinDotData,pinDotClock,MSBFIRST,dotData[i]);
  }

  /* Latch the row of data */
  digitalWrite(pinColLatch, HIGH);
  digitalWrite(pinColLatch, LOW);

  digitalWrite(pinDisplayEnable, LOW);  // Turn off the display while we latch in the this row.
  if(row == 0) { // For some reason 
    digitalWrite(pinRowData, HIGH); // row data high on row 0
  } else {
    digitalWrite(pinRowData, LOW);
  }
  digitalWrite(pinRowClock, LOW);   // Advance the row pointer.
  delayMicroseconds(1);             // Minimum 1us dip
  digitalWrite(pinRowClock, HIGH);
  digitalWrite(pinDisplayEnable, HIGH); 
}
