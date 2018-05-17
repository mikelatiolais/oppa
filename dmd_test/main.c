#include <stdio.h>
#include "oppa_display.h"

/*
 * 128 x 32 LEDs = 4096
 * 4096 / 8 (number of bits in a byte) = 512
 */

void main() {
  UINT8 dmddata[OPPA_NUM_OF_BYTES]; 

  /* Keep looping */
  while(1) {
    /* Cycle through values of byte */
    for(int val = 0; val < 9; val++) {
      /* Fill the array with the same value */
      for (int i = 0; i < OPPA_NUM_OF_BYTES; ++i){
        dmddata[i] = val;
      }
      /* Update the DMD */
      oppaUpdateDMD(dmddata);
    }
  }
}
