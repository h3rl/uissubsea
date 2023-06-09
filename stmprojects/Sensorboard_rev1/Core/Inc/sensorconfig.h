/*
 * sensorconfig.h
 *
 *  Created on: 8 Mar 2023
 *      Author: halva
 */

#ifndef SENSORCONFIG_H_
#define SENSORCONFIG_H_

#include <stdio.h>
#include <stdbool.h>

#include "stm32g4xx_hal.h"
#include "LSM9DS1.h"


#define IMU_INTERVAL 30

// I2C addresses for magnetometer + accelerometer/gyro
#define LSM9DS1_M   0x1E // Would be 0x1C if SDO_M is LOW - magnetometer address
#define LSM9DS1_AG  0x6B // Would be 0x6A if SDO_AG is LOW - accel/gyro address

#endif /* SENSORCONFIG_H_ */
