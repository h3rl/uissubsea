/*
 * packetbuilder.h
 * 
 * Contains functions for building packets
 */

#ifndef PACKET_BUILDER_H
#define PACKET_BUILDER_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Start PacketInfo */
enum PacketIds {
    PING = 1,
    PONG = 2,
    JOYSTICK = 3,
    ACCELEROMETER = 10,
    GYRO = 11,
    MAGNOMETER = 12,
    BAROMETER = 13,
    TEMPERATURE = 14,
    HUMIDITY = 15,
    THRUST = 20,
    ANGLE = 21,
    TARGETANGLE = 22,
    VOLTAGE = 30,
    CURRENT = 31,
    POWER = 32,
};

enum PacketSize {
    PING = 1,
    PONG = 1,
    JOYSTICK = 24,
    ACCELEROMETER = 6,
    GYRO = 6,
    MAGNOMETER = 4,
    BAROMETER = 2,
    TEMPERATURE = 2,
    HUMIDITY = 2,
    THRUST = 12,
    ANGLE = 16,
    TARGETANGLE = 16,
    VOLTAGE = 4,
    CURRENT = 4,
    POWER = 4,
};
/* End PacketInfo */

uint8_t* BuildPacket(uint8_t id, uint8_t* data)
{

}

#endif