#!/usr/bin/env python3
import numpy as np
from scipy.sparse import bsr_matrix

AC0_PARAM = { 'aifsn':2, 'cw':(2,3) }
AC1_PARAM = { 'aifsn':2, 'cw':(3,4) }
AC2_PARAM = { 'aifsn':3, 'cw':(4,10) }
AC3_PARAM = { 'aifsn':7, 'cw':(4,10) }

AC2_CW = lambda x: { 'aifsn':3, 'cw':(x,10) }
AC3_CW = lambda x: { 'aifsn':7, 'cw':(x,10) }

IDX2CW = lambda idx: 2**idx - 1

class User:
    __slots__ = ('demand', 'aifsn', 'cw_idx', 'cw_max')

    def __init__(self, param):
        self.demand = float( param['demand'] )
        self.aifsn  = int( param['aifsn'] )
        self.cw_idx = int( param['cw'][0] )
        self.cw_max = int( param['cw'][1] )
        # self.cw_cur = -1
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
        User({ **AC2_PARAM, 'demand':1.0 }),
        User({ **AC2_PARAM, 'demand':1.0 }),
    ]
    prob = go_through(users, run_event)
    print(prob)