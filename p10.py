#!/usr/bin/env python
# coding:utf-8
#
# p10.py
#
# Author:   Hiromasa Ihara (miettal)
# URL:      http://miettal.com
# License:  MIT License
# Created:  2014-10-26
#

import serial

s = serial.Serial(port='/dev/ttyUSB0', baudrate=2400)
def byte2num(b) :
  tbl = {
    0:0b01111101,
    1:0b00000101,
    2:0b01011011,
    3:0b00011111,
    4:0b00100111,
    5:0b00111110,
    6:0b01111110,
    7:0b00010101,
    8:0b01111111,
    9:0b00111111,
    10:0b00000000,
    11:0b01101000,
  }

  for (index, value) in tbl.items() :
    if b == value :
      if index == 10 : return 0
      if index == 11 : return float("+inf")
      return index

def readseg(ser) :
  data = ord(ser.read())
  bin_str = "{:8b}".format(data)
  n = int(bin_str[0:4], 2)
  d = int(bin_str[4:8], 2)

  return (n, d)

while True :
  try :
    (n, seg1) = readseg(s)
    if n != 1 : continue
    (_, seg2) = readseg(s)
    (_, seg3) = readseg(s)
    (_, seg4) = readseg(s)
    (_, seg5) = readseg(s)
    (_, seg6) = readseg(s)
    (_, seg7) = readseg(s)
    (_, seg8) = readseg(s)
    (_, seg9) = readseg(s)
    (_, seg10) = readseg(s)
    (_, seg11) = readseg(s)
    (_, seg12) = readseg(s)
    (_, seg13) = readseg(s)
    (_, seg14) = readseg(s)
  except ValueError :
    print "Error!"
    continue

  d0 = byte2num(((seg2<<4)+seg3)&0b01111111)
  d1 = byte2num(((seg4<<4)+seg5)&0b01111111)
  d2 = byte2num(((seg6<<4)+seg7)&0b01111111)
  d3 = byte2num(((seg8<<4)+seg9)&0b01111111)
  value = d0*1000 + d1*100 + d2*10 + d3

  if seg2&0b1000 :
    sign = -1
  else :
    sign = 1

  if seg4&0b1000 :
    scale = 0.001
  elif seg6&0b1000 :
    scale = 0.01
  elif seg8&0b1000:
    scale = 0.1
  else :
    scale = 1.0

  if seg10&0b0010 :
    subunit = "K"
  elif seg10&0b0100 :
    subunit = "n"
  elif seg10&0b1000 :
    subunit = "u"
  elif seg11&0b0010 :
    subunit = "M"
  elif seg11&0b1000 :
    subunit = "m"
  else :
    subunit = ""

  if seg12&0b0100 :
    unit = "ohm"
  elif seg12&0b1000 :
    unit = "F"
  elif seg13&0b0010 :
    unit = "Hz"
  elif seg13&0b0100 :
    unit = "V"
  elif seg13&0b1000 :
    unit = "A"

  print str(sign * value * scale) + " " + subunit + unit
