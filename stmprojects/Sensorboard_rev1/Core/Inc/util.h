/*
 * util.h
 *
 *  Created on: 7 Mar 2023
 *      Author: halva
 */

#ifndef UTIL_H_
#define UTIL_H_

#include <stdio.h>
#include <stdbool.h>

#include "stm32g4xx_hal.h"

void Scan_I2C_Devices(UART_HandleTypeDef* huart, I2C_HandleTypeDef* hi2c);

#endif /* UTIL_H_ */
