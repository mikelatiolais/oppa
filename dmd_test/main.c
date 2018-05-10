#include <stdio.h>
#include "oppa_display.h"

/*
 * 128 x 32 LEDs = 4096
 * 4096 / 8 (number of bits in a byte) = 512
 */

void main() {
  UINT8 dmddata[OPPA_NUM_OF_BYTES]; 

  for (int i = 0; i < OPPA_NUM_OF_BYTES; ++i){
    dmddata[i] = i;
  }
  
  oppaUpdateDMD(dmddata);
}
