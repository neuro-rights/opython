import OpenHoldem

import math
import argparse
import os
import sys
import time
import random

import numpy as np

# from board_classifier import classify_board

print(sys.version)

from pathlib import Path

# Ensure project root is in path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PokerAxiom.src.strategy.game_state import GameState, Street
from PokerAxiom.src.strategy.positions import Position
from PokerAxiom.src.strategy.strategy_engine import StrategyEngine

class Main:
    """
    """

    # double symbols #
    oh_double = { 
        'prwin': 0.0,
        'prtie': 0.0,
        'prlos': 0.0,
        'call': 0.0,
        'currentbet': 0.0,
        'balance': 0.0,
        'pot': 0.0,
        'sblind': 0.0,
        'bblind': 0.0,
        'balance0': 0.0,
        'balance1': 0.0,
        'balance2': 0.0,
        'balance3': 0.0,
        'balance4': 0.0,
        'balance5': 0.0,
        'balance6': 0.0,
        'balance7': 0.0,
        'balance8': 0.0,
        'balance9': 0.0,
        'currentbet0': 0.0,
        'currentbet1': 0.0,
        'currentbet2': 0.0,
        'currentbet3': 0.0,
        'currentbet4': 0.0,
        'currentbet5': 0.0,
        'currentbet6': 0.0,
        'currentbet7': 0.0,
        'currentbet8': 0.0,
        'currentbet9': 0.0
    }
    
    # int symbols #
    oh_int = {
        'betround': 0,
        'handrank169': 0,
        'nplayersplaying': 0,
        'nplayersdealt': 0,
        'didfold': 0,
        'didchec': 0,
        'didcall': 0,
        'didrais': 0,
        'didbetsize': 0,
        'didalli': 0,
        'dealerchair': 0,
        'userchair': 0,
        'dealposition': 0,
        'playersplayingbits': 0
    }
    
    # player cards
    oh_player_card_ranks = {
        '$$pr0': -1,
        '$$pr1': -1
    }
    
    # player suits
    oh_player_card_suits = {
        '$$ps0': -1,
        '$$ps1': -1
    }
    
    # board cards
    oh_common_card_ranks = {
        '$$cr0': -1,
        '$$cr1': -1,
        '$$cr2': -1,
        '$$cr3': -1,
        '$$cr4': -1
    }
    
    # board_suits
    oh_common_card_suits = {
        '$$cs0': -1,
        '$$cs1': -1,
        '$$cs2': -1,
        '$$cs3': -1,
        '$$cs4': -1
    }
    
    cc1 = ''
    cc2 = ''
    cc3 = ''
    cc4 = ''
    cc5 = ''
    
    pc1 = ''
    pc2 = ''
    
    player_cards = []
    common_cards = []
    
    
    def __init__(self):
        """
        """   
        # common cards
        for k, v in self.oh_common_card_ranks.items():
            self.oh_common_card_ranks[k] = -1
        for k, v in self.oh_common_card_suits.items():
            self.oh_common_card_suits[k] = -1
            
        # player cards
        for k, v in self.oh_player_card_ranks.items():
            self.oh_player_card_ranks[k] = -1
        for k, v in self.oh_player_card_suits.items():
            self.oh_player_card_suits[k] = -1
        
        # int values
        for k, v in self.oh_int.items():
            self.oh_int[k] = 0
            
        # double values
        for k, v in self.oh_double.items():
            self.oh_double[k] = 0.0


    def _rank_str_card(self, card_rank):
        """
            Convert card rank to string value (2=2, ..., T=10, J=11, Q=12, K=13, A=14)
        """
        rank_map = {2: '2', 
                    3: '3', 
                    4: '4', 
                    5: '5', 
                    6: '6', 
                    7: '7', 
                    8: '8', 
                    9: '9', 
                    10: 'T', 
                    11: 'J', 
                    12: 'Q', 
                    13: 'K',
                    14: 'A'}
        return rank_map.get(card_rank, 'X')
    
    
    def _suit_str_card(self, card_suit):
        """
            Convert card rank to string value (2=2, ..., T=10, J=11, Q=12, K=13, A=14)
        """
        suit_map = {0: 'h', 
                    1: 'd', 
                    2: 'c', 
                    3: 's'}
        return suit_map.get(card_suit, 'x')
        
            
    def updateVars(self):
        
        # common card ranks
        for k, v in self.oh_common_card_ranks.items():
            self.oh_common_card_ranks[k] = int(OpenHoldem.getSymbol(k))
            
        # common card suits
        for k, v in self.oh_common_card_suits.items():
            self.oh_common_card_suits[k] = int(OpenHoldem.getSymbol(k))

        # player card ranks
        for k, v in self.oh_player_card_ranks.items():
            self.oh_player_card_ranks[k] = int(OpenHoldem.getSymbol(k))
    
        # player card suits
        for k, v in self.oh_player_card_suits.items():
            self.oh_player_card_suits[k] = int(OpenHoldem.getSymbol(k))

        # int values #
        for k, v in self.oh_int.items():
            self.oh_int[k] = int(OpenHoldem.getSymbol(k))
            
        # double values
        for k, v in self.oh_double.items():
            self.oh_double[k] = OpenHoldem.getSymbol(k)
            #print(f'{k}: {self.oh_double[k]}\n')        
        

    def timesActed(self):
        return int(self.oh["didfold"] + self.oh["didchec"] + self.oh["didcall"] + self.oh["didrais"] + self.oh["didbetsize"])
        

    def getDecision(self):
        """
        """
        decision = 0.0
        self.updateVars()
            
        # common cards strings
        self.cc1 = self._rank_str_card(self.oh_common_card_ranks["$$cr0"]) + self._suit_str_card(self.oh_common_card_suits["$$cs0"])
        self.cc2 = self._rank_str_card(self.oh_common_card_ranks["$$cr1"]) + self._suit_str_card(self.oh_common_card_suits["$$cs1"])
        self.cc3 = self._rank_str_card(self.oh_common_card_ranks["$$cr2"]) + self._suit_str_card(self.oh_common_card_suits["$$cs2"])
        self.cc4 = self._rank_str_card(self.oh_common_card_ranks["$$cr3"]) + self._suit_str_card(self.oh_common_card_suits["$$cs3"])
        self.cc5 = self._rank_str_card(self.oh_common_card_ranks["$$cr4"]) + self._suit_str_card(self.oh_common_card_suits["$$cs4"])
        
        self.common_cards = []
        if self.oh_int["betround"] > 1:
            self.common_cards.append(self.cc1)
            self.common_cards.append(self.cc2)
            self.common_cards.append(self.cc3)
        if self.oh_int["betround"] > 2:
            self.common_cards.append(self.cc4)
        if self.oh_int["betround"] > 3:
            self.common_cards.append(self.cc5)
         
        # player cards strings
        self.pc1 = self._rank_str_card(self.oh_player_card_ranks["$$pr0"]) + self._suit_str_card(self.oh_player_card_suits["$$ps0"])
        self.pc2 = self._rank_str_card(self.oh_player_card_ranks["$$pr1"]) + self._suit_str_card(self.oh_player_card_suits["$$ps1"])
        
        self.player_cards = []
        self.player_cards.append(self.pc1)
        self.player_cards.append(self.pc2)
        
        players_stacks = {}
        players_bets = {}
        players_active_bits = {}
        for i in range(10):
            p_bet = self.oh_double["currentbet" + str(i)]
            players_bets.update({i: p_bet})
            p_stack = self.oh_double["balance" + str(i)]
            players_stacks.update({i: p_stack})
            players_active_bits.update({i: bool(int(self.oh_int["playersplayingbits"]) & (1 << i))})
            
        print("Players Stacks\n")
        print(players_stacks)
        print("Plzyers Bets\n")
        print(players_bets)
        print("Players Active\n")
        print(players_active_bits)
        print("\n")
            
        # Scenario: Hero has flush draw
        state = GameState(
            hero_cards=self.player_cards,
            board_cards=self.common_cards,  # Flush draw
            pot=self.oh_double["pot"],
            stacks=players_stacks,
            bets=players_bets,
            street=int(self.oh_int["betround"]) - 1,
            sb=self.oh_double["sblind"],
            bb=self.oh_double["bblind"],
            position=(0 if self.oh_int["dealposition"] == self.oh_int["nplayersdealt"] else self.oh_int["dealposition"]),
            dealer_seat=int(self.oh_int["dealerchair"]),
            hero_seat=int(self.oh_int["userchair"]),
            active_seats=players_active_bits
        )
        
        engine = StrategyEngine()
        action = engine.recommend(state)
        print(action.action_type.name + "\n")
        
        if action.action_type.name == "CALL":
            decision = 0.001
        elif action.action_type.name == "BET":
            decision = action.amount
        elif action.action_type.name == "RAISE":
            decision = action.amount + state.to_call()
        elif action.action_type.name == "ALLIN":
            decision = action.amount
            
        print(f"Hero cards: {state.hero_cards}" + "\n")
        print(f"Board: {state.board_cards}" + "\n")
        print(f"Pot: ${state.pot}, To call: ${state.to_call()}" + "\n")
        print("\n")
        print(f"Recommended action: {action.action_type.name}" + "\n")
        if action.reasoning:
            print(f"Reasoning: {action.reasoning}" + "\n")
        print("Decision\n")
    
        print(f"Decision: ${decision:.3f}\n")
        
        return decision