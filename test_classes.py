import pytest
from classes import *
from asci_arts import shields_examples as shields

def test_shield_draw():
    s = []
    for i in range(8):
        s.append(Shield(10, 10, i+1))
        
    assert s[2].draw() == shields[3]