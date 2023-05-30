/*
 * packets.c
 *
 *  Created on: 7 Mar 2023
 *      Author: halva
 */

#include "packets.h"
#include "stm32g4xx_hal.h"

#include <string.h>

extern UART_HandleTypeDef huart2;

PacketHandler::PacketHandler()
{

}

PacketHandler::~PacketHandler()
{

}

void PacketHandler::setEcho(bool echo)
{
	this->echo = echo;
}

void PacketHandler::processData(uint8_t* data, size_t size)
{
	if(this->echo)
	{
	    HAL_UART_Transmit(&huart2, data, size, 100);// send each byte we recieve back (echo)
	}

	//if(this->size >= packet_size)
	if(memcmp(data,"\r",1)==0)
	{
		// is eof
		//Packet packet = createPacketFromBuffer();

		this->appendBuffer((uint8_t*)"\r\n",2);
		HAL_UART_Transmit(&huart2, this->buffer, this->size, 100);// send what we got

	    // reset ptr to start of buffer
	    this->clearBuffer();
	}
	else
	{
		// add data to end of packetbuffer
		this->appendBuffer(data, size);
	}

	// if echo enabled transmit recieved data;
}

void PacketHandler::clearBuffer(void)
{
	this->ptr = this->buffer;
	this->size = 0;
}

void PacketHandler::appendBuffer(uint8_t* data, size_t size)
{
	memcpy(this->ptr,data,size);
	this->ptr += size;
	this->size += size;
}
