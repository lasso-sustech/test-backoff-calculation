#!/usr/bin/env python3
import numpy as np
from sympy import *
from scipy.sparse import bsr_matrix

AC0_PARAM = { 'aifsn':2, 'cw':(2,3) }
AC1_PARAM = { 'aifsn':2, 'cw':(3,4) }
AC2_PARAM = { 'aifsn':3, 'cw':(4,10) }
AC3_PARAM = { 'aifsn':7, 'cw':(4,10) }

AC2_CW = lambda x: { 'aifsn':3, 'cw':(x,10) }
AC3_CW = lambda x: { 'aifsn':7, 'cw':(x,10) }

IDX2CW = lambda idx: 2**idx - 1
_P = lambda x: max(x, 0)

class User:
    __counter = 0
    __slots__ = ('name', 'arrival', 'mcs', 'aifsn', 'cw_idx', 'cw_max')

    def __init__(self, param, name=''):
        self.name = name
        if not name:
            self.name = 'x_{}'.format(User.__counter)
            User.__counter += 1

        self.arrival = float( param['arrival'] )
        self.mcs = float( param['mcs'] )

        self.aifsn  = int( param['aifsn'] )
        self.cw_idx = int( param['cw'][0] )
        self.cw_max = int( param['cw'][1] )
        pass

    @property
    def real_cw(self):
        return ( self.aifsn, self.aifsn+IDX2CW(self.cw_idx) )

    @property
    def cw_size(self):
        return IDX2CW(self.cw_idx) + 1

    def next_cw(self):
        self.cw_idx = min(self.cw_idx+1, self.cw_max)
        return self.cw_idx
    pass

def collide(users:list, selection:list, prob_limit=1E-5):
    ##FIXME: calculate the collision probability and the counter side.
    collide_users = [x for (i,x) in enumerate(users) if selection[i]=='1' ]
    

    real_min, real_max = zip(*[x.real_cw for x in collide_users])
    for collide_cw in range( max(real_min), min(real_max)+1 ):
        pass

    num_collide = min(real_max) - max(real_min) + 1
    prob_collide = [ num_collide/x.cw_size for x in users ] 

    ##
    prob_result = 1.0

    for i,x in enumerate(users):
        if selection[i]=='1':
            _prob_busy = x.demand
            _prob_collide = num_collide / x.cw_size
            prob_result *= _prob_busy * _prob_collide
    ##
    print(selection, prob_result)
    if prob_result > prob_limit:
        users = [x.copy() for x in users]
        for i,x in enumerate(users):
            if selection[i]=='1':
                x.next_cw()
        return (prob_result, users)
    else:
        return (0.0, None)
    pass

def guess(users: list):

    def guess_ab(demand_a, demand_b, user_a:User, user_b:User): #FIXME: use uniform guess is not acceptable
        pa, cwa_len, cwa_s, cwa_t = demand_a, user_a.cw_size, *user_a.real_cw
        pb, cwb_len, cwb_s, cwb_t = demand_b, user_b.cw_size, *user_b.real_cw
        ##
        prob_a = (1-pb)*pa # A always wins
        for i in range(cwa_s,cwa_t+1):
            prob_a += (pa*pb) / (cwa_len*cwb_len) * _P(cwb_t - i)
            pass
        ##
        prob_b = (1-pa)*pb # B always wins
        for i in range(cwb_s, cwb_t+1):
            prob_b += (pa*pb) / (cwa_len*cwb_len) * _P(cwa_t - i)
            pass
        ##
        return (prob_a, prob_b)
    
    num_users = len(users)
    demands = [ symbols(u.name) if u.arrival else 1 for u in users ]

    prob_ratio = [1] * num_users
    for i in range(num_users-1):
        _prob_a, _prob_b = guess_ab(demands[0], demands[i+1], users[0], users[i+1])
        prob_ratio[i+1] = _prob_b / _prob_a
    ##
    _sum_ratio = sum(prob_ratio)
    prob_ratio = [x/_sum_ratio for x in prob_ratio]

    poly_eqs = list()
    for i,u in enumerate(users):
        if u.arrival:
            poly_eqs.append( u.arrival/(u.mcs*prob_ratio[i]) - demands[i] )

    _variables =  [ x for x in demands if x!=1 ]
    solutions = nonlinsolve(poly_eqs, _variables)
    print(solutions)

    return guess_ab(1, 1, users[0], users[1])

def go_through(users, run_event, depth=0):
    num_users = len(users)
    result = run_event(users)
    print(depth)

    for i in range(1,num_users):
        selection = ( '{:0%db}'%(num_users) ).format(i)
        _prob, _users = collide(users, selection)
        if _prob:
            result += _prob * go_through(_users, run_event, depth+1)
    ##
    return result

def run_event(users) -> float:
    return 0.0

if __name__=='__main__':
    users = [
        User({ **AC2_PARAM, 'arrival':0, 'mcs':54 }),
        User({ **AC2_CW(8), 'arrival':0, 'mcs':54 }),
    ]
    # prob = go_through(users, run_event)
    prob = guess(users)
    print(prob)