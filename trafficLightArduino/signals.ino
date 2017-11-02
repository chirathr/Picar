const int r = 9;             //connect red led at pin 9
const int y = 10;           //connect yellow led at pin 10
const int g = 11;           //connect green led at pin 11
const int sec = 1000;       //seconds defined
void setup()
  {
    pinMode(r,OUTPUT);    //setting pin 9 as output mode
    pinMode(y,OUTPUT);    //setting pin 10 as output mode
    pinMode(g,OUTPUT);    //setting pin 11 as output mode
    delay(sec);
  }

void loop()
    {
        digitalWrite(r,HIGH) ;    //turning on pin 9
        delay(sec*5);             //setting light time period as 5*1000 seconds
        digitalWrite(r,LOW) ;     //turning off pin 9
        digitalWrite(y,HIGH) ;    //turning on pin 10
        delay(sec*5);             //setting light time period as 5*1000 seconds
        digitalWrite(y,LOW) ;     //turning off pin 10
        digitalWrite(g,HIGH) ;    //turning on pin 11
        delay(sec*5);             //setting light time period as 5*1000 seconds
        digitalWrite(g,LOW) ;     //turning off pin 11

    }
