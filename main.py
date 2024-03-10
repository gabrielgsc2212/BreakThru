import tkinter as tk
from tkinter import messagebox
import math
import random

class Game:
    def __init__(self):
        self.Player_dourada = False
        self.linhas = 7
        self.colunas = 7
        self.tabuleiro = []        
        self.selected_letter = None
        self.last_clicked_button = None
        self.switch = 1
        self.posicoes_douradas = []
        self.posicoes_pratas = []
        self.ia = IA_functions(self)
        
# ================== CONTROLE DO TABULEIRO ==================       
    def criar_tabuleiro(self, root):
        for linha in range(self.linhas):
                linha_tabuleiro = []
                for coluna in range(self.colunas):
                    botao = tk.Button(root, text="", width=6, height=3, bg="black", command=lambda row=linha, col=coluna: self.on_button_click(row, col))
                    botao.grid(row=linha, column=coluna, padx=1, pady=1)
                    linha_tabuleiro.append(botao)
                self.tabuleiro.append(linha_tabuleiro)
        return self.tabuleiro

    def desativar_tabuleiro(self):
        for linha in self.tabuleiro:
                for botao in linha:
                    botao.config(state="disabled")
    
    def on_button_click(self, row, col):
        if self.Player_dourada:
                if self.switch == 1:
                    self.selected_letter, self.last_clicked_button = self.golden_user(row, col)
                else:
                    self.ia.turno_IA(-math.inf, math.inf, 4)
        else:
                if self.switch == 1:
                    self.ia.turno_IA(-math.inf, math.inf, 4)
                else:
                    self.selected_letter, self.last_clicked_button = self.silver_user(row, col)
                
# ========================== MOVIMENTOS DAS PEÇAS ===========================     
    #Função de validação de movimento
    def is_valid_move(self, last_row, last_col, row, col):             
                if (abs(last_row - row) == 1 and last_col == col) or (abs(last_col - col) == 1 and last_row == row):
                    if self.switch == 2:
                            if self.tabuleiro[row][col]['text'] in ["X", "@"]:
                                return False
                            if last_row == row or last_col == col:
                                step_row = 1 if row > last_row else -1
                                step_col = 1 if col > last_col else -1
                                if last_row == row:
                                        for col in range(last_col + step_col, col, step_col):
                                            if self.tabuleiro[last_row][col]['text'] != "":
                                                    return False
                                            else:
                                                    for row in range(last_row + step_row, row, step_row):
                                                        if self.tabuleiro[row][last_col]['text'] != "":
                                                                return False
                                return True
                    else:
                            if self.tabuleiro[row][col]['text'] == "O":
                                return False
                            if last_row == row or last_col == col:
                                step_row = 1 if row > last_row else -1
                                step_col = 1 if col > last_col else -1
                                if last_row == row:
                                        for col in range(last_col + step_col, col, step_col):
                                            if self.tabuleiro[last_row][col]['text'] != "":
                                                    return False
                                else:
                                        for row in range(last_row + step_row, row, step_row):
                                            if self.tabuleiro[row][last_col]['text'] != "":
                                                    return False
                            return True
                elif abs(row - last_row) == abs(col - last_col) and abs(row - last_row) == 1:
                    return False
                else:
                    print("Movimento fora do alcance")
                    return False
        
    #Função de captura das peças    
    def check_captura(self, row, col,  last_row, last_col):
        if abs(row - last_row) == abs(col - last_col) and abs(row - last_row) == 1:
                    # Movimento das douradas
                    if self.switch == 1:
                            # Impede o flagship de realizar capturas
                            if self.selected_letter == "@":
                                print("O @ não pode capturar nenhuma peça")
                                return False                              
                                
                            elif self.tabuleiro[row][col]['text'] == "O":
                                self.tabuleiro[row][col].config(text=self.last_clicked_button['text'], font=('Arial', 9, 'bold'), fg="yellow")
                                self.last_clicked_button['text'] = ""   
                                self.check_win_prata()
                                self.last_clicked_button = None
                                self.selected_letter = None                              
                                self.posicoes_pratas.remove((row, col))
                                self.posicoes_douradas.remove((last_row, last_col))
                                self.posicoes_douradas.append((row, col))
                                self.switch = 2
                                if self.Player_dourada:
                                        self.ia.turno_IA(-math.inf, math.inf, 4)
                                
                                return                
                            
                            elif self.tabuleiro[row][col]['text'] == "":
                                print("Não há peça para ser capturada")
                                return False 
                            
                            else:
                                return False
                            
                    # Movimento das pratas    
                    else:
                            if self.tabuleiro[row][col]['text'] == "X" or self.tabuleiro[row][col]['text'] == "@":
                                self.tabuleiro[row][col].config(text=self.last_clicked_button['text'], font=('Arial', 9, 'bold'), fg="silver")
                                self.last_clicked_button['text'] = ""   
                                self.check_win_prata()
                                self.last_clicked_button = None
                                self.selected_letter = None
                                self.posicoes_douradas.remove((row, col))
                                self.posicoes_pratas.remove((last_row, last_col))
                                self.posicoes_pratas.append((row, col))
                                self.switch = 1
                                if not self.Player_dourada:
                                        self.ia.turno_IA(-math.inf, math.inf, 4)
                                return
                            else:
                                return False   
        else:
                return False

#Função de movimento das peças                 
    def move_piece(self, row, col, last_row, last_col):
        if self.switch == 1:
                if self.Player_dourada:
                    pass
                else:
                    self.last_clicked_button = self.tabuleiro[last_row][last_col]
        else:
                if self.Player_dourada:
                    self.last_clicked_button = self.tabuleiro[last_row][last_col]
                else:
                    pass
            
        if self.check_captura(row, col,  last_row, last_col):
                return
        else:
                if self.is_valid_move(last_row, last_col, row, col):
                    # Movimento da peça dourada pelo player
                    if self.switch == 1 and self.Player_dourada:       
                            self.tabuleiro[row][col].config(text=self.last_clicked_button['text'], font=('Arial', 9, 'bold'), fg="yellow")
                            self.posicoes_douradas.remove((last_row, last_col))
                            self.posicoes_douradas.append((row, col))
                            self.last_clicked_button['text'] = ""
                            self.last_clicked_button = None
                            self.selected_letter = None   
                            self.check_win_dourada()    
                            self.switch = 2
                            self.ia.turno_IA(-math.inf, math.inf, 4)
                    
                    # Movimento da peça dourada pela IA      
                    elif self.switch == 1 and not self.Player_dourada:
                            self.tabuleiro[row][col].config(text=self.last_clicked_button['text'], font=('Arial', 9, 'bold'), fg="yellow")
                            self.posicoes_douradas.remove((last_row, last_col))
                            self.posicoes_douradas.append((row, col))
                            self.last_clicked_button['text'] = ""
                            self.last_clicked_button = None
                            self.selected_letter = None   
                            self.check_win_dourada()
                            self.switch = 2
                                                        
                    # Movimento da peça prata pelo player   
                    elif self.switch == 2 and not self.Player_dourada:
                            self.last_clicked_button = self.tabuleiro[last_row][last_col]
                            self.tabuleiro[row][col].config(text=self.last_clicked_button['text'], font=('Arial', 9, 'bold'), fg="silver") 
                            self.posicoes_pratas.remove((last_row, last_col))
                            self.posicoes_pratas.append((row, col))
                            self.last_clicked_button['text'] = ""
                            self.last_clicked_button = None
                            self.selected_letter = None
                            self.switch = 1
                            self.ia.turno_IA(-math.inf, math.inf, 4)
                            
                    # Movimento da peça prata pela IA
                    elif self.switch == 2 and self.Player_dourada:
                            self.last_clicked_button = self.tabuleiro[last_row][last_col]
                            self.tabuleiro[row][col].config(text=self.last_clicked_button['text'], font=('Arial', 9, 'bold'), fg="silver") 
                            self.posicoes_pratas.remove((last_row, last_col))
                            self.posicoes_pratas.append((row, col))
                            self.last_clicked_button['text'] = ""
                            self.last_clicked_button = None
                            self.selected_letter = None
                            self.switch = 1
                    
                            
                else:
                    return False

#Controle das peças douradas para o usuário
    def golden_user(self, row, col):
        if self.tabuleiro[row][col]['text'] == "X":
                self.selected_letter = "X"
                self.last_clicked_button = self.tabuleiro[row][col]
                    
        elif self.tabuleiro[row][col]['text'] == "@":
                self.selected_letter = "@"
                self.last_clicked_button = self.tabuleiro[row][col]
                    
        elif self.last_clicked_button is not None:
                last_row, last_col = self.get_button_position(self.last_clicked_button) 
                if self.selected_letter == "X":  
                    self.move_piece(row, col, last_row, last_col)
                                
                elif self.selected_letter == "@":
                    self.move_piece(row, col, last_row, last_col)
                else:
                    self.sekected_letter = None
                    self.last_clicked_button = None
                    
        return self.selected_letter, self.last_clicked_button   
    
    def silver_user(self, row, col):   
        if self.tabuleiro[row][col]['text'] == "O":
                self.selected_letter = "O"
                self.last_clicked_button = self.tabuleiro[row][col]
                
        elif self.last_clicked_button is not None:
                if self.selected_letter == "O":
                    last_row, last_col = self.get_button_position(self.last_clicked_button)
                    self.move_piece(row, col, last_row, last_col)
                else:
                    pass
        else:
                pass
                            
        return self.selected_letter, self.last_clicked_button     
        
# ================== CONDIÇÕES DE VITÓRIA ==================
    def check_win_dourada(self):
        for position in self.posicoes_douradas:
                row, col = position
                if self.tabuleiro[row][col]['text'] == "@":
                    if row == 0 or row == self.linhas - 1 or col == 0 or col == self.colunas - 1:
                            self.desativar_tabuleiro()
                            messagebox.showinfo("Game over", "Vitória das douradas!")
                            exit()
        return False

    def check_win_prata(self):
        for position in self.posicoes_douradas:
                row, col = position
                if self.tabuleiro[row][col]['text'] == "@":
                    return False

        self.desativar_tabuleiro()
        messagebox.showinfo("Game over", "Vitória das pratas!")
        exit()
    
# ============= CONTROLE DE INFORMAÇÃO DAS PEÇAS ==================
    def get_button_position(self, button):
        for i in range(self.linhas):
                for j in range(self.colunas):
                    if self.tabuleiro[i][j] == button:
                            return i, j
                                
    def start_pieces(self):
        linha_central = self.linhas // 2
        coluna_central = self.colunas // 2

        self.tabuleiro[linha_central][coluna_central].config(text="@", font=('Arial', 9, 'bold'), fg="yellow")
        self.posicoes_douradas.append((linha_central, coluna_central))

        for i in range(linha_central - 1, linha_central + 2):
                for j in range(coluna_central - 1, coluna_central + 2):
                    if (i, j) != (linha_central, coluna_central):
                            self.tabuleiro[i][j].config(text="X", font=('Arial', 9, 'bold'), fg="yellow")
                            self.posicoes_douradas.append((i, j))

        for i in range(2, 5):  
                self.tabuleiro[i][0].config(text="O", font=('Arial', 9, 'bold'), fg="silver")
                self.posicoes_pratas.append((i, 0))
                    
                self.tabuleiro[i][-1].config(text="O", font=('Arial', 9, 'bold'), fg="silver")
                self.posicoes_pratas.append((i, self.colunas - 1))

        for j in range(2, 5):  
                self.tabuleiro[0][j].config(text="O", font=('Arial', 9, 'bold'), fg="silver")
                self.posicoes_pratas.append((0, j))
                    
                self.tabuleiro[-1][j].config(text="O", font=('Arial', 9, 'bold'), fg="silver")
                self.posicoes_pratas.append((self.linhas - 1, j))
# ============================= MENUS =============================    
    def menu_principal(self):
        root = tk.Tk()
        root.title("Menu Principal")
        root.geometry("600x600")
        root.configure(bg="#13174b")
        root.resizable(False, False)

        def jogar():
                root.destroy()
                self.piece_selection()

        def sair():
                root.destroy()
                    
        btn_jogar = tk.Button(root, text="Jogar", command=jogar, width=15, height=2, font=('Arial', 15, 'bold'), bg="white")
        btn_jogar.pack(pady=(250, 10))
        btn_sair = tk.Button(root, text="Sair", command=sair, width=15, height=2, font=('Arial', 12, 'bold'), bg="white")
        btn_sair.pack(pady=10)
        root.mainloop()
        
    def piece_selection(self):
        root = tk.Tk()
        root.title("Escolha suas peças")
        root.geometry("600x600")
        root.configure(bg="#13174b")
        root.resizable(False, False)
        
        def douradas():
                self.Player_dourada = True
                root.destroy()
                newroot = tk.Tk()
                newroot.title("BreakThru")
                newroot.resizable(False, False)
                self.criar_tabuleiro(newroot)
                self.start_pieces()
        
        def pratas():
                self.Player_dourada = False
                root.destroy()
                newroot = tk.Tk()
                newroot.title("BreakThru")
                newroot.resizable(False, False)
                self.criar_tabuleiro(newroot)
                self.start_pieces()
                
        btn_douradas = tk.Button(root, text="Douradas", command=douradas, width=15, height=2, font=('Arial', 15, 'bold'), bg="white")
        btn_douradas.pack(pady=(250, 10))
        btn_pratas = tk.Button(root, text="Pratas", command=pratas, width=15, height=2, font=('Arial', 15, 'bold'), bg="white")
        btn_pratas.pack(pady=10)
        root.mainloop()
                

class IA_functions:

    def __init__(self, game):
        self.game = game    
        self.INICIAL_GOLD = 8
        self.INICIAL_SILVER = 12 
        
    def turno_IA(self, alpha, beta, depth):
        if len(self.game.posicoes_douradas) == 1:
                for position in self.game.posicoes_douradas:
                    row, col = position
                    if self.game.tabuleiro[row][col]['text'] == "@":
                            self.game.desativar_tabuleiro()
                            messagebox.showinfo("Game over", "As peças douradas se esgotaram!")
                            exit()
        else:
                pass
                    
        if len(self.game.posicoes_pratas) > 0:
                _, chosen_play = self.minimax_alpha_beta(depth, alpha, beta)
                if chosen_play is not None:
                    last_row, last_col, row, col = chosen_play
                    self.game.move_piece(row, col, last_row, last_col)
                else:
                    print("Não há jogadas possíveis para a IA")
        else:
                self.game.desativar_tabuleiro()
                messagebox.showinfo("Game over", "As peças pratas se esgotaram!")
                exit()
                

    def number_piece(self):
        if self.game.Player_dourada:
                return len(self.game.posicoes_pratas)/self.INICIAL_SILVER - len(self.game.posicoes_douradas)/self.INICIAL_GOLD
        else:
                return len(self.game.posicoes_douradas)/self.INICIAL_GOLD - len(self.game.posicoes_pratas)/self.INICIAL_SILVER

    def proximity_to_flagship(self):
        flagship_positions = [pos for pos in self.game.posicoes_douradas if self.game.tabuleiro[pos[0]][pos[1]]['text'] == "@"]
        min_distance = float('inf')
        for silver_pos in self.game.posicoes_pratas:
                for flagship_pos in flagship_positions:
                    distance = abs(silver_pos[0] - flagship_pos[0]) + abs(silver_pos[1] - flagship_pos[1])
                    min_distance = min(min_distance, distance)
        if self.game.Player_dourada:
                return -min_distance
        else:
                return min_distance
    
    def value_board(self):
        pieces = self.number_piece()
        proximity = self.proximity_to_flagship()
        if self.game.Player_dourada:
                return pieces - proximity
        else:
                return pieces + proximity

    
    def minimax_alpha_beta(self, depth, alpha, beta):
        
        if depth == 0 or self.game.check_win_dourada() or self.game.check_win_prata():
                return self.value_board(), None
                
        moves = self.possible_moves()
                
        max_eval = -math.inf
        for tabuleiro in moves:
                evaluation, _ = self.minimax_alpha_beta(depth - 1, alpha, beta)
                if evaluation > max_eval:
                    max_eval = evaluation
                    chosen_play = tabuleiro
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
        return max_eval, chosen_play
    
    def possible_moves(self):
        moves = []
        check_flagship = []
        win_flagship = []
        check_opponent_piece = []
        random_moves = []
        close_to_win = []  
        
        if self.game.switch == 1:
                for position in self.game.posicoes_douradas:
                    row, col = position
                    posicoes_adjacentes = [
                    (row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                    (row, col - 1),                     (row, col + 1),
                    (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)
                    ]
                    for adj_row, adj_col in posicoes_adjacentes:
                            if 0 <= adj_row < self.game.linhas and 0 <= adj_col < self.game.colunas:
                                
                                # Movimentos horizontais e verticais que levam à vitória
                                if self.game.tabuleiro[row][col]['text'] == "@" and (row == adj_row or col == adj_col):     
                                    if adj_row == 0 or adj_row == self.game.linhas - 1 or adj_col == 0 or adj_col == self.game.colunas - 1 and self.game.tabuleiro[adj_row][adj_col]['text'] == "":
                                        win_flagship.append((row, col, adj_row, adj_col))   
                                                                                
                                # Checa as diagonais
                                elif abs(adj_row - row) == 1 and abs(adj_col - col) == 1:
                                        # Movimentos do flagship sob situação de risco
                                        if self.game.tabuleiro[row][col]['text'] == "@":
                                            
                                            # Checa se o flagship pode ser capturado      
                                            if abs(adj_row - row) == 1 and abs(adj_col - col) == 1:
                                                    if self.game.tabuleiro[adj_row][adj_col]['text'] == "O":
                                                        # Confere se é possível capturar a peça prata
                                                        if self.game.tabuleiro[adj_row + 1][adj_col + 1]['text'] == "X":
                                                            check_flagship.append((adj_row + 1, adj_col + 1, adj_row, adj_col))
                                                        elif self.game.tabuleiro[adj_row + 1][adj_col - 1]['text'] == "X":
                                                            check_flagship.append((adj_row + 1, adj_col - 1, adj_row, adj_col))
                                                        elif self.game.tabuleiro[adj_row - 1][adj_col + 1]['text'] == "X":
                                                            check_flagship.append((adj_row - 1, adj_col + 1, adj_row, adj_col))
                                                        elif self.game.tabuleiro[adj_row - 1][adj_col - 1]['text'] == "X":
                                                            check_flagship.append((adj_row - 1, adj_col - 1, adj_row, adj_col))
                                                        
                                                        # Se não é possível capturar, fuja    
                                                        elif self.game.tabuleiro[adj_row][col]['text'] == "":
                                                                check_flagship.append((row, col, adj_row, col))     
                                                        elif self.game.tabuleiro[row][adj_col]['text'] == "":
                                                                check_flagship.append((row, col, row, adj_col))
                                                        else: 
                                                                pass
                                        
                                        # Checa se é possível capturar outra peça prata                  
                                        if self.game.tabuleiro[row][col]['text'] == "X":
                                                    if self.game.tabuleiro[adj_row][adj_col]['text'] == "O":
                                                        check_opponent_piece.append((row, col, adj_row, adj_col)) 
                                                        
                                else:
                                        # Tenta deixar o flagship mais perto da borda
                                        if self.game.tabuleiro[adj_row][adj_col]['text'] == "":
                                            if self.game.tabuleiro[row][col]['text'] == "@":
                                                    if adj_row - self.game.linhas < row - self.game.linhas or adj_col - self.game.colunas < col - self.game.colunas:
                                                        if self.game.tabuleiro[adj_row + 1][adj_col + 1]['text'] != "O" and self.game.tabuleiro[adj_row + 1][adj_col - 1]['text'] != "O" and self.game.tabuleiro[adj_row - 1][adj_col + 1]['text'] != "O" and self.game.tabuleiro[adj_row - 1][adj_col - 1]['text'] != "O":
                                                                close_to_win.append((row, col, adj_row, adj_col))
                                            
                                            elif self.game.tabuleiro[row][col]['text'] == "X":
                                                    random_moves.append((row, col, adj_row, adj_col))
                                                    
                if win_flagship:
                    moves.extend(win_flagship)
                elif check_flagship:
                    moves.extend(check_flagship)
                elif check_opponent_piece:
                    moves.extend(check_opponent_piece)
                elif close_to_win:
                    moves.extend(close_to_win)
                else:
                    random.shuffle(random_moves)
                    moves.extend(random_moves)

        else:
        
                for position in self.game.posicoes_pratas:
                    row, col = position
                    posicoes_adjacentes = [
                    (row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                    (row, col - 1),                     (row, col + 1),
                    (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)
                    ]
                    for adj_row, adj_col in posicoes_adjacentes:
                                
                            # Checa se a posição adjacente está dentro do tabuleiro
                            if 0 <= adj_row < self.game.linhas and 0 <= adj_col < self.game.colunas:
                                        
                                    # Checa se é possível realizar captura
                                if abs(adj_row - row) == 1 and abs(adj_col - col) == 1:
                                        
                                        # Checa se é possível capturar o flagship
                                        if self.game.tabuleiro[adj_row][adj_col]['text'] == "@":
                                            check_flagship.append((row, col, adj_row, adj_col))
                                                    
                                        # Checa se é possível capturar outra peça dourada
                                        elif self.game.tabuleiro[adj_row][adj_col]['text'] == "X":
                                            check_opponent_piece.append((row, col, adj_row, adj_col))
                                            
                                # Checa se é possível realizar outro movimento
                                else:
                                        if self.game.tabuleiro[adj_row][adj_col]['text'] == "" and (adj_row == row or adj_col == col):
                                            random_moves.append((row, col, adj_row, adj_col))
                            else:
                                pass    
                if check_flagship:
                    moves.extend(check_flagship)
                elif check_opponent_piece:
                    moves.extend(check_opponent_piece)
                else:
                    random.shuffle(random_moves)
                    moves.extend(random_moves)
                    
        return moves 
                
game = Game()
ia = IA_functions(game)
game.menu_principal()
