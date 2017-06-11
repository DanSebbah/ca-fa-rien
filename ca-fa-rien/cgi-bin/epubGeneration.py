#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import cgitb
# enable debugging
cgitb.enable()

import writeBook;

print("Content-Type: text/html;charset=utf-8\n\n")

retValue = writeBook.generate()
print(retValue)

def main():
    print("ho ho ho !")
    return retValue

