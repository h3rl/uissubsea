/*
 * packets.h
 *
 *  Created on: 7 Mar 2023
 *      Author: halva
 */

#ifndef PACKETS_H_
#define PACKETS_H_

#include <stdio.h>
#include <stdbool.h>

/*
 * Packet structure
 * uint8_t id;
 * buffer
 */

class Packet{

};

class PacketHandler {
public:
	PacketHandler();
	virtual ~PacketHandler();

private:
	uint8_t buffer[128];
	uint8_t* ptr = nullptr;
	size_t size = 0;

	bool echo = false;
public:
	void processData(uint8_t* data, size_t size);
	void setEcho(bool echo);
	//void processPacket();
private:
	Packet createPacketFromBuffer(void);
	void clearBuffer(void);
	void appendBuffer(uint8_t* data, size_t size);
};

#endif /* PACKETS_H_ */
