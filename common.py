#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 1/15/18 5:30 PM
# @Author  : xiaowa

import random
import json

def random_choice(prop_list):
    total_prop = sum(prop_list)
    prop_list = [e / total_prop for e in prop_list]
    target = random.random()
    acc = 0
    for idx, prop in enumerate(prop_list):
        acc += prop
        if acc >= target:
            return idx

def random_move(action_list):
    action = random.choice(action_list)
    return action

def get_status_key(status):
    key = json.dumps(status)
    return key




