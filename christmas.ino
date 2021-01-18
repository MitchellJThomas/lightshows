// NeoPixel Ring simple sketch (c) 2013 Shae Erisson
// Released under the GPLv3 license to match the rest of the
// Adafruit NeoPixel library
// This sketch shows use of the "new" operator with Adafruit_NeoPixel.
// It's helpful if you don't know NeoPixel settings at compile time or
// just want to store this settings in EEPROM or a file on an SD card.

#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
 #include <avr/power.h> // Required for 16 MHz Adafruit Trinket
#endif

// Which pin on the Arduino is connected to the NeoPixels?
int pin         =  6;

// How many NeoPixels are attached to the Arduino?
int numPixels   = 240; 

// NeoPixel color format & data rate. See the strandtest example for
// information on possible values.
int pixelFormat = NEO_GRB + NEO_KHZ800;

// Rather than declaring the whole NeoPixel object here, we just create
// a pointer for one, which we'll then allocate later...
Adafruit_NeoPixel *pixels;

void setup() {
  // Right about here is where we could read 'pin', 'numPixels' and/or
  // 'pixelFormat' from EEPROM or a file on SD or whatever. This is a simple
  // example and doesn't do that -- those variables are just set to fixed
  // values at the top of this code -- but this is where it would happen.

  // Then create a new NeoPixel object dynamically with these values:
  pixels = new Adafruit_NeoPixel(numPixels, pin, pixelFormat);

  // Going forward from here, code works almost identically to any other
  // NeoPixel example, but instead of the dot operator on function calls
  // (e.g. pixels.begin()), we instead use pointer indirection (->) like so:
  pixels->begin(); // INITIALIZE NeoPixel strip object (REQUIRED)
  // You'll see more of this in the loop() function below.
}

void loop() {
  pixels->clear(); // Set all pixel colors to 'off'

  // rainbow(50, *pixels);
  // christmas(50, *pixels);

  // theaterChase(pixels->Color(20,   0,   0), 150, *pixels); // Red, half brightness
  // rainbow2(200, *pixels);
   // red(1000, *pixels);
  // multiColorChase(120, *pixels);
   biden(500, *pixels);
}

uint8_t blues(uint8_t intensity, Adafruit_NeoPixel& strip) {
  return strip.gamma32(strip.Color(0, 0, intensity));
}

uint8_t reds(uint8_t intensity, Adafruit_NeoPixel& strip) {
  return strip.gamma32(strip.Color(intensity, 0, 0));
}

uint8_t whites(uint8_t intensity, Adafruit_NeoPixel& strip) {
  return strip.gamma32(strip.Color(intensity, intensity, intensity));
}

void biden(int wait, Adafruit_NeoPixel& strip) {
  int intensities = 17;
  uint8_t intense[intensities] = {60, 80, 100, 120, 140, 160, 180, 200, 255, 200, 180, 160, 140, 120, 100, 80, 60};
  int color_len = 9;
  int  i = 0;
  uint32_t colors[intensities][color_len] = {{393216, 393216, 393216, 394758, 394758, 394758, 6, 6, 6}, {851968, 851968, 851968, 855309, 855309, 855309, 13, 13, 13}, {1441792, 1441792, 1441792, 1447446, 1447446, 1447446, 22, 22, 22}, {2359296, 2359296, 2359296, 2368548, 2368548, 2368548, 36, 36, 36}, {3538944, 3538944, 3538944, 3552822, 3552822, 3552822, 54, 54, 54}, {4980736, 4980736, 4980736, 5000268, 5000268, 5000268, 76, 76, 76}, {6750208, 6750208, 6750208, 6776679, 6776679, 6776679, 103, 103, 103}, {8912896, 8912896, 8912896, 8947848, 8947848, 8947848, 136, 136, 136}, {16711680, 16711680, 16711680, 16777215, 16777215, 16777215, 255, 255, 255}, {8912896, 8912896, 8912896, 8947848, 8947848, 8947848, 136, 136, 136}, {6750208, 6750208, 6750208, 6776679, 6776679, 6776679, 103, 103, 103}, {4980736, 4980736, 4980736, 5000268, 5000268, 5000268, 76, 76, 76}, {3538944, 3538944, 3538944, 3552822, 3552822, 3552822, 54, 54, 54}, {2359296, 2359296, 2359296, 2368548, 2368548, 2368548, 36, 36, 36}, {1441792, 1441792, 1441792, 1447446, 1447446, 1447446, 22, 22, 22}, {851968, 851968, 851968, 855309, 855309, 855309, 13, 13, 13}, {393216, 393216, 393216, 394758, 394758, 394758, 6, 6, 6}};
  
  int c=0;
  for(int s = 0; s < intensities; s++) {
    strip.clear();
    # No chance, set c=0;
    for(int i=0; i < strip.numPixels(); i++) { 
      strip.setPixelColor(i, colors[s][c++]);
      if (c >= colors_len) c=0;
    }
    strip.show();
    delay(wait);
  }
}
// Theater-marquee-style chasing lights. Pass in a color (32-bit value,
// a la strip.Color(r,g,b) as mentioned above), and a delay time (in ms)
// between frames.
void multiColorChase(int wait, Adafruit_NeoPixel& strip) {

  uint8_t values[] = {40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100, 
                  105, 110, 115, 120, 125, 130, 135, 140, 145, 150, 155, 160, 165, 170, 175, 180, 185, 190, 195, 200,
                  205, 210, 215, 220, 225, 230, 235, 230, 225, 220, 215, 210, 
                  205, 200, 195, 190, 185, 180, 175, 170, 165, 160, 155, 150, 145, 140, 135, 130, 125, 120, 115, 110, 
                  105, 100, 95, 90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35};
  for(int i=0; i<sizeof(values); i++) { 
      uint8_t a = values[i];
      for(int b=0; b<3; b++) { //  'b' counts from 0 to 2...
        strip.clear(); 
        // 'c' counts up from 'b' to end of strip in steps of 3...
        uint16_t color1 = a % 65536;
        uint16_t color2 = ((255 - a) * 64) % 65536;
        for(int c=b; c<strip.numPixels(); c += 3) {
          uint32_t  color = strip.gamma32(strip.ColorHSV(color1));
          strip.setPixelColor(c++, color);
          strip.setPixelColor(c, color);
          c += b;
          color = strip.gamma32(strip.ColorHSV(color2));
          strip.setPixelColor(c++, color);
          strip.setPixelColor(c, color);
        }
        strip.show(); // Update strip with new contents
        delay(wait);  // Pause for a moment
      }
    }
}






// Rainbow cycle along whole strip. Pass delay time (in ms) between frames.
void rainbow(int wait, Adafruit_NeoPixel& strip) {
  // Hue of first pixel runs 5 complete loops through the color wheel.
  // Color wheel has a range of 65536 but it's OK if we roll over, so
  // just count from 0 to 5*65536. Adding 256 to firstPixelHue each time
  // means we'll make 5*65536/256 = 1280 passes through this outer loop:
  for(long firstPixelHue = 0; firstPixelHue < 2*65536; firstPixelHue += 256) {
    for(int i=0; i<strip.numPixels(); i++) { // For each pixel in strip...
      // Offset pixel hue by an amount to make one full revolution of the
      // color wheel (range of 65536) along the length of the strip
      // (strip.numPixels() steps):
      int pixelHue = firstPixelHue + (i * 65536L / strip.numPixels());
      // strip.ColorHSV() can take 1 or 3 arguments: a hue (0 to 65535) or
      // optionally add saturation and value (brightness) (each 0 to 255).
      // Here we're using just the single-argument hue variant. The result
      // is passed through strip.gamma32() to provide 'truer' colors
      // before assigning to each pixel:
      strip.setPixelColor(i, strip.gamma32(strip.ColorHSV(pixelHue)));
    }
    strip.show(); // Update strip with new contents
    delay(wait);  // Pause for a moment
  }
}

void red(int wait, Adafruit_NeoPixel& strip) {
  uint8_t r=128;
  enum incdec {incr, decr} i_d;
  i_d = incr;
  for(int a=0; a<20; a++) {  // Repeat 10 times...
      strip.clear();         //   Set all pixels in RAM to 0 (off)


      for(int c=0; c<strip.numPixels(); c++) {
         uint32_t color = strip.gamma32(strip.Color(r, 0, 0));
         strip.setPixelColor(c, color);

         switch(i_d) {
          case incr:
            r++;
            break;
          case decr:
            r--;
            break;
        }
        if (r >= 255) i_d = decr;
        if (r <= 0) i_d = incr;
        
      }
      strip.show(); // Update strip with new contents
      delay(wait);  // Pause for a moment
  }
}

void rainbow2(int wait, Adafruit_NeoPixel& strip) {
  uint8_t r=0, g=0, b=0;
  enum colors{red, green, blue} which_color; 
  which_color = red;
  for(int a=0; a<100; a++) {  // Repeat 10 times...
      strip.clear();         //   Set all pixels in RAM to 0 (off)
      for(int c=0; c<strip.numPixels(); c++) {
        uint32_t color = 0;
        switch(which_color) {
          case red:
            color = strip.gamma32(strip.Color(r++, b, g));
            if (r >= 255) {
              r = 0;
              which_color = blue;
            }
            break;
          case blue:
            color = strip.gamma32(strip.Color(r, b++, g));
            if (b >= 255) {
              b = 0;
              which_color = green;
            }
            if (r >= 255) {
              r = 0;
            }
            break;
          case green:
            color = strip.gamma32(strip.Color(r, b, g++));
            if (g >= 255) {
              g = 0;
              which_color = red;
            }
            if (b >= 255) {
              b = 0;
            }
            if (r >= 255) {
              r = 0;
            }
            break;
        }
        strip.setPixelColor(c, color);

      }
      strip.show(); // Update strip with new contents
      delay(wait);  // Pause for a moment
  }
}


// Rainbow cycle along whole strip. Pass delay time (in ms) between frames.
void christmas(int wait, Adafruit_NeoPixel& strip) {
  // Hue of first pixel runs 5 complete loops through the color wheel.
  // Color wheel has a range of 65536 but it's OK if we roll over, so
  // just count from 0 to 5*65536. Adding 256 to firstPixelHue each time
  // means we'll make 5*65536/256 = 1280 passes through this outer loop:
  for(long firstPixelHue = 0; firstPixelHue < 2*65536; firstPixelHue += 512) {
    for(int i=0; i<strip.numPixels(); i++) { // For each pixel in strip...
      // Offset pixel hue by an amount to make one full revolution of the
      // color wheel (range of 65536) along the length of the strip
      // (strip.numPixels() steps):
      int pixelHue = firstPixelHue + (i * 65536L / strip.numPixels());
      // strip.ColorHSV() can take 1 or 3 arguments: a hue (0 to 65535) or
      // optionally add saturation and value (brightness) (each 0 to 255).
      // Here we're using just the single-argument hue variant. The result
      // is passed through strip.gamma32() to provide 'truer' colors
      // before assigning to each pixel:
      strip.setPixelColor(i, strip.gamma32(strip.ColorHSV(pixelHue)));
    }
    strip.show(); // Update strip with new contents
    delay(wait);  // Pause for a moment
  }
}
