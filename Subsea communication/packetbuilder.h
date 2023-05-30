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

/* Start PacketIds */
enum PacketIds{
    PING = 1,
    PONG = 2,
    JOYSTICK = 3,

    ACCELEROMETER = 10,
    GYROSCOPE = 11,
    MAGNOMETER = 12,
    BAROMETER = 13,
    TEMPERATURE = 14,
    HUMIDITY = 15,

    THRUST = 20,
    ANGLE = 21,
    TARGET_ANGLE = 22,

    VOLTAGE = 30,
    CURRENT = 31,
    POWER = 32
}

enum PacketSizes{
    PING = 1,
    PONG = 1,
}
/* End PacketIds */

uint8_t* BuildPacket(uint8_t id, uint8_t* data)
{

}

#endif