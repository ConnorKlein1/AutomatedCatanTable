from catan_objects.BoardComponents import *
from catan_objects.CatanBoard import CatanBoard
import math

"""
Defines the standard setup of a catan game, useful for tests and the final product.    
"""

def Setup(A_pos):
    # The size of each resource hex and number tile
    long_hex_Radius = 45.5 # mm
    short_hex_radius = long_hex_Radius / 2 * math.sqrt(3) * 1.01 # mm

    # The neighbors of each empty hex
    A_neighbors = ['0', 'B', 'E','C', '0', '0']
    B_neighbors = ['0', 'D', 'G','E', 'A', '0']
    C_neighbors = ['A', 'E', 'H','F', '0', '0']
    D_neighbors = ['0', '0', 'I','G', 'B', '0']
    E_neighbors = ['B', 'G', 'J','H', 'C', 'A']
    F_neighbors = ['C', 'H', 'K','0', '0', '0']
    G_neighbors = ['D', 'I', 'L','J', 'E', 'B']
    H_neighbors = ['E', 'J', 'M','K', 'F', 'C']
    I_neighbors = ['0', '0', 'N','L', 'G', 'D']
    J_neighbors = ['G', 'L', 'O','M', 'H', 'E']
    K_neighbors = ['H', 'M', 'P','0', '0', '0']
    L_neighbors = ['I', 'N', 'Q','O', 'J', 'G']
    M_neighbors = ['J', 'O', 'R','P', 'K', 'H']
    N_neighbors = ['0', '0', '0','Q', 'L', 'I']
    O_neighbors = ['L', 'Q', 'S','R', 'M', 'J']
    P_neighbors = ['M', 'R', '0','0', '0', 'K']
    Q_neighbors = ['N', '0', '0','S', 'O', 'L']
    R_neighbors = ['O', 'S', '0','0', 'P', 'M']
    S_neighbors = ['Q', '0', '0','0', 'R', 'O']

    # The position of each possible catan board, determined by the hexes radius
    # The position of each possible catan board, determined by the hexes radius
    B_pos = (A_pos[0] + 1.5 * long_hex_Radius, A_pos[1] + short_hex_radius)
    C_pos = (A_pos[0] - (1.5 * long_hex_Radius), A_pos[1] + short_hex_radius)
    D_pos = (B_pos[0] + 1.5 * long_hex_Radius, B_pos[1] + short_hex_radius)
    E_pos = (A_pos[0], 2 * short_hex_radius + A_pos[1])
    F_pos = (C_pos[0] - (1.5 * long_hex_Radius), C_pos[1] + short_hex_radius)
    G_pos = (B_pos[0], 2 * short_hex_radius + B_pos[1])
    H_pos = (C_pos[0], 2 * short_hex_radius + C_pos[1])
    I_pos = (D_pos[0], 2 * short_hex_radius + D_pos[1])
    J_pos = (E_pos[0], 2 * short_hex_radius + E_pos[1])
    K_pos = (F_pos[0], 2 * short_hex_radius + F_pos[1])
    L_pos = (G_pos[0], 2 * short_hex_radius + G_pos[1])
    M_pos = (H_pos[0], 2 * short_hex_radius + H_pos[1])
    N_pos = (I_pos[0], 2 * short_hex_radius + I_pos[1])
    O_pos = (J_pos[0], 2 * short_hex_radius + J_pos[1])
    P_pos = (K_pos[0], 2 * short_hex_radius + K_pos[1])
    Q_pos = (L_pos[0], 2 * short_hex_radius + L_pos[1])
    R_pos = (M_pos[0], 2 * short_hex_radius + M_pos[1])
    S_pos = (O_pos[0], 2 * short_hex_radius + O_pos[1])
    
    configuration = [
        [['A', A_pos, A_neighbors, long_hex_Radius], Hex('A', long_hex_Radius)]
        ]
    
    return CatanBoard(configuration)

if __name__ == '__main__':
    Setup()