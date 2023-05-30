/*
 * packets.c
 *
 *  Created on: 7 Mar 2023
 *      Author: halva
 */

#include "util.h"
#include "stm32g4xx_hal.h"

#include <string.h>

void Scan_I2C_Devices(UART_HandleTypeDef* huart, I2C_HandleTypeDef* hi2c)
{
	uint8_t buffer[25] = {0};
	uint8_t msg_start[] = "Starting I2C Scanning: \r\n";
	uint8_t msg_end[] = "Done!\r\n";
	uint8_t msg_summary[] = "Found %";

	uint8_t cnt = 0;
	uint8_t ret;

	HAL_Delay(1000);

	/*-[ I2C Bus Scanning ]-*/
    HAL_UART_Transmit(huart, msg_start, sizeof(msg_start), 10000);
    for(uint8_t i=1; i<128; i++)
    {
        ret = HAL_I2C_IsDeviceReady(hi2c, (uint16_t)(i<<1), 3, 5);
        if(ret == HAL_OK) // ACK Received
		{
			sprintf((char*)buffer, "found 0x%X\r\n", i);
			HAL_UART_Transmit(huart, buffer, sizeof(buffer), 10000);
			cnt++;
		}

    }
	sprintf((char*)buffer, "Done! found %i devices\r\n", cnt);
	HAL_UART_Transmit(huart, buffer, sizeof(buffer), 10000);


    /*--[ Scanning Done ]--*/

    while (1)
    {
    }
}
