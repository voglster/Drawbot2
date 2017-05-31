//------------------------------------------------------------------------------
// 2 Axis CNC Demo
// dan@marginallycelver.com 2013-08-30
//------------------------------------------------------------------------------
// Copyright at end of file.
// please see http://www.github.com/MarginallyClever/GcodeCNCDemo for more information.

#include <Servo.h>
#include "config.h"

//------------------------------------------------------------------------------
// GLOBALS
//------------------------------------------------------------------------------

char  buffer[MAX_BUF];  // where we store the message until we get a newline
int   sofar;            // how much is in the buffer
				   // speeds
long fr = 0;  // human version
unsigned long step_delay;  // machine version
bool awaiting = false;
unsigned long last_command = 0;

struct COMMAND {
	long lchange;
	long rchange;
	long feedrate;
	int penstate;
	unsigned long wait;
};

COMMAND commands[10];

byte current_index = 0;
byte input_index = 0;

byte nextIndex(byte index) {
	if (index == 9) {
		return 0;
	}
	return index + 1;
}

bool availableCommand() {
	return current_index != input_index;
}


 //------------------------------------------------------------------------------
 // METHODS
 //------------------------------------------------------------------------------


 /**
 * delay for the appropriate number of microseconds
 * @input ms how many milliseconds to wait
 */
void pause(long ms) {
	delay(ms / 1000);
	delayMicroseconds(ms % 1000);  // delayMicroseconds doesn't work for values > ~16k.
}


/**
* Set the feedrate (speed motors will move)
* @input nfr the new speed in steps/second
*/
void feedrate(long nfr) {
	if (fr == nfr) return;  // same as last time?  quit now.

	if (nfr>MAX_FEEDRATE || nfr<MIN_FEEDRATE) {  // don't allow crazy feed rates
		Serial.print(F("New feedrate must be greater than "));
		Serial.print(MIN_FEEDRATE);
		Serial.print(F("steps/s and less than "));
		Serial.print(MAX_FEEDRATE);
		Serial.println(F("steps/s."));
		return;
	}
	step_delay = 1000000.0 / nfr;
	fr = nfr;
	Serial.print(F("feedrate:"));
	Serial.println(nfr);
}


/**
* Uses bresenham's line algorithm to move both motors
* @input newx the destination x position
* @input newy the destination y position
**/
unsigned long last_step;
void line(long dx, long dy) {
	long i;
	long over = 0;
	int dirx = dx>0 ? 1 : 0;
	int diry = dy>0 ? 1 : 0;  // because the motors are mounted in opposite directions
	dx = abs(dx);
	dy = abs(dy);

	if (dx>dy) {
		over = dx / 2;
		for (i = 0; i<dx; ++i) {
			last_step = micros();
			m1step(dirx);
			over += dy;
			if (over >= dx) {
				over -= dx;
				m2step(diry);
			}
			while (micros() - last_step < step_delay) {}
		}
	}
	else {
		over = dy / 2;
		for (i = 0; i<dy; ++i) {
			last_step = micros();
			m2step(diry);
			over += dx;
			if (over >= dy) {
				over -= dy;
				m1step(dirx);
			}
			while (micros() - last_step < step_delay) {}
		}
	}
}

/**
* Look for character /code/ in the buffer and read the float that immediately follows it.
* @return the value found.  If nothing is found, /val/ is returned.
* @input code the character to look for.
* @input val the return value if /code/ is not found.
**/
long parsenumber(char code, long val) {
	char *ptr = buffer;
	while (*ptr && ptr < buffer + sofar) {
		if (*ptr == code) {
			return atol(ptr + 1);
		}
		ptr++;
	}
	return val;
}

/**
* display helpful information
*/
void help() {
	Serial.print(F("JVDrawBot Version "));
	Serial.println(VERSION);
	Serial.println(F("Commands:"));
	Serial.println(F("G00 [L(steps)] [R(steps)] [F(feedrate)]; - line"));
	Serial.println(F("G01 [L(steps)] [R(steps)] [F(feedrate)]; - line"));
	Serial.println(F("G04 P[miliseconds]; - delay"));
	Serial.println(F("G92 [L(steps)] [R(steps)]; - change logical position"));
	Serial.println(F("M1 [A(angle)]; - change pen angle"));
	Serial.println(F("M18; - disable motors"));
	Serial.println(F("M19; - enable motors"));
	Serial.println(F("M100; - this help message"));
	Serial.println(F("All commands must end with a newline."));
}

void runCommand() {
	COMMAND c = commands[current_index];
	if (c.feedrate != 0) {
		feedrate(c.feedrate);
	}
	if (c.penstate != -1) {
		set_servo_angle(c.penstate);
	}
	if (c.wait != 0) {
		pause(c.wait);
	}
	if (c.lchange != 0 || c.rchange != 0) {
		line(c.lchange, c.rchange);
	}
	current_index = nextIndex(current_index);
	if (awaiting) {
		awaiting = false;
		ready();
	}
	last_command = millis();
}

/**
* Read the input buffer and find any recognized commands.  One G or M command per line.
*/
void processCommand() {
	int cmd = parsenumber('G', -1);
	switch (cmd) {
	case  0:
	case  1: { // line
		commands[input_index].feedrate = parsenumber('F', fr);
		commands[input_index].lchange = parsenumber('L',0);
		commands[input_index].rchange = parsenumber('R',0);
		commands[input_index].wait = 0;
		commands[input_index].penstate = -1;
		break;
	}
	case  4: // dwell
		commands[input_index].feedrate = 0;
		commands[input_index].lchange = 0;
		commands[input_index].rchange = 0;
		commands[input_index].wait = parsenumber('P', 0);
		commands[input_index].penstate = -1;
		break;
	default:  break;
	}

	cmd = parsenumber('M', -1);
	switch (cmd) {
	case 1: //set pen angle
		commands[input_index].feedrate = 0;
		commands[input_index].lchange = 0;
		commands[input_index].rchange = 0;
		commands[input_index].wait = 0;
		commands[input_index].penstate = (int)parsenumber('A', 0);
		break;
	case 18:  // disable motors
		disable();
		break;
	case 19:  // disable motors
		enable();
		break;
	case 100:  help();  break;
	default:  break;
	}
	input_index = nextIndex(input_index);
}


/**
* prepares the input buffer to receive a new message and tells the serial connected device it is ready for more.
*/
void ready() {
	sofar = 0;  // clear input buffer
	Serial.println(F(">"));  // signal ready to receive input
}


/**
* First thing this machine does on startup.  Runs only once.
*/
void setup() {
	for (int i = 0; i < 10; i++) {
		commands[i].feedrate = 0;
		commands[i].lchange = 0;
		commands[i].rchange = 0;
		commands[i].wait = 0;
		commands[i].penstate = -1;
	}
	Serial.begin(BAUD);  // open coms

	setup_controller();
	feedrate((MAX_FEEDRATE + MIN_FEEDRATE) / 2);  // set default speed
	help();  // say hello
	ready();
	last_command = millis();
}

/**
* After setup() this machine will repeat loop() forever.
*/
void loop() {
	if (availableCommand())
		runCommand();
	if (millis() - last_command > 10000) {
		disable();
	}
}

void serialEvent() {
	bool err = false;
	while (Serial.available() > 0) {  // if something is available
		char c = Serial.read();  // get it
		if (!awaiting) {
			Serial.print(c);  // repeat it back so I know you got the message
			if (sofar<MAX_BUF - 1) buffer[sofar++] = c;  // store it
			if ((c == '\n') || (c == '\r')) {
				// entire message received
				buffer[sofar] = 0;  // end the buffer so string functions work right
				Serial.print(F("\r\n"));  // echo a return character for humans
				processCommand();  // do something with the command
				last_command = millis();
				if (nextIndex(input_index) != current_index)
					ready();
				else
					awaiting = true;
			}
		}
		else {
			err = true;
		}
	}
	if(err)
		Serial.println("BufferFull please wait");
}
