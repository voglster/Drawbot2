#pragma once
#ifndef CONFIG_H
#define CONFIG_H

//------------------------------------------------------------------------------
// CONSTANTS
//------------------------------------------------------------------------------

#define VERSION        (1)  // firmware version
#define BAUD           (115200)  // How fast is the Arduino talking?
#define MAX_BUF        (64)  // What is the longest message Arduino can store?
#define STEPS_PER_TURN (6400)  // depends on your stepper motor.  most are 200.
#define MIN_STEP_DELAY (0.1)
#define MAX_FEEDRATE   (10000)
#define MIN_FEEDRATE   (100)

//------------------------------------------------------------------------------
// CONSTANTS
//------------------------------------------------------------------------------
#define ENA  8

#define M1_STEP 2
#define M1_DIR  5

#define M2_STEP 4
#define M2_DIR  7

#define SERVO 11

Servo penServo;

//------------------------------------------------------------------------------
// METHODS
//------------------------------------------------------------------------------

void disable() {
	digitalWrite(ENA, HIGH);
}

void enable() {
	digitalWrite(ENA, LOW);
}

void m1step(int dir) {
	enable();
	digitalWrite(M1_DIR, dir);
	digitalWrite(M1_STEP, HIGH);
	digitalWrite(M1_STEP, LOW);
}

void m2step(int dir) {
	enable();
	digitalWrite(M2_DIR, dir);
	digitalWrite(M2_STEP, HIGH);
	digitalWrite(M2_STEP, LOW);
}


void setup_controller() {
	pinMode(ENA, OUTPUT);
	disable();
	pinMode(M1_STEP, OUTPUT);
	pinMode(M2_STEP, OUTPUT);
	pinMode(M1_DIR, OUTPUT);
	pinMode(M2_DIR, OUTPUT);
	penServo.attach(SERVO);
}

void set_servo_angle(int angle) {
	if (angle > 180) {
		angle = 180;
	}
	if (angle < 0) {
		angle = 0;
	}
	penServo.write(angle);
}


#endif