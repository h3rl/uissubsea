/*
 * imu_config.h
 *
 *  Created on: 7 Mar 2023
 *      Author: halva
 */

#ifndef IMU_CONFIG_H_
#define IMU_CONFIG_H_

#include <stdio.h>
#include <stdbool.h>

#include "LSM9DS1.h"

// SDO_XM and SDO_G are both pulled high, so our addresses are:
#define LSM9DS1_M	0x1E // Would be 0x1C if SDO_M is LOW
#define LSM9DS1_AG	0x6B // Would be 0x6A if SDO_AG is LOW
#define LSM9DS1_M	0x1C // Would be 0x1C if SDO_M is LOW
#define LSM9DS1_AG	0x6A // Would be 0x6A if SDO_AG is LOW


#endif /* IMU_CONFIG_H_ */
