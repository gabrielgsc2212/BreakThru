import tkinter as tk
from tkinter import messagebox
import math
import random

class Game:
    def __init__(self):
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
                botao = tk.Button(root, text="", width=8, height=4, bg="black", command=lambda row=linha, col=coluna: self.on_button_click(row, col))
                botao.grid(row=linha, column=coluna, padx=1, pady=1)
                linha_tabuleiro.append(botao)
            self.tabuleiro.append(linha_tabuleiro)
        return self.tabuleiro

    def desativar_tabuleiro(self):
        for linha in self.tabuleiro:
            for botao in linha:
                botao.config(state="disabled")
      
    def on_button_click(self, row, col):
        if self.switch == 1:
            self.selected_letter, self.last_clicked_button = self.golden_user(row, col)
        else:
            self.ia.turno_IA(-math.inf, math.inf, 5)
                  
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
            if self.switch == 1:   
                   
                if self.tabuleiro[row][col]['text'] == "O":
                    self.tabuleiro[row][col].config(text=self.last_clicked_button['text'], font=('Arial', 9, 'bold'), fg="yellow")
                    self.last_clicked_button['text'] = ""   
                    self.check_win_prata()
                    self.last_clicked_button = None
                    self.selected_letter = None                              
                    self.posicoes_pratas.remove((row, col))
                    self.posicoes_douradas.remove((last_row, last_col))
                    self.posicoes_douradas.append((row, col))
                    self.switch = 2
                    self.ia.turno_IA(-math.inf, math.inf, 5)
                    return                
                    
                # Impede o flagship de realizar capturas
                if self.selected_letter == "@":
                    print("O @ não pode capturar nenhuma peça")
                    return False
   
                elif self.tabuleiro[row][col]['text'] == "":
                    print("Não há peça para ser capturada")
                    return False 
                  
                else:
                    return False
                        
            else:
                if self.tabuleiro[row][col]['text'] != "" and self.tabuleiro[row][col]['text'] != "O":
                    self.tabuleiro[row][col].config(text=self.last_clicked_button['text'], font=('Arial', 9, 'bold'), fg="silver")
                    self.last_clicked_button['text'] = ""   
                    self.check_win_prata()
                    self.last_clicked_button = None
                    self.selected_letter = None
                    self.posicoes_douradas.remove((row, col))
                    self.posicoes_pratas.remove((last_row, last_col))
                    self.posicoes_pratas.append((row, col))
                    self.switch = 1
                else:
                    return 
                  
        else:
            return False 
    
    #Função de movimento das peças                 
    def move_piece(self, row, col, last_row, last_col):
        if self.switch == 1:
            pass
        else:    
            self.last_clicked_button = self.tabuleiro[last_row][last_col]
              
        if self.check_captura(row, col,  last_row, last_col):
            return
        else:
            if self.is_valid_move(last_row, last_col, row, col):
                #Movimento da peça dourada
                if self.switch == 1:       
                    self.tabuleiro[row][col].config(text=self.last_clicked_button['text'], font=('Arial', 9, 'bold'), fg="yellow")
                    self.posicoes_douradas.remove((last_row, last_col))
                    self.posicoes_douradas.append((row, col))
                    self.last_clicked_button['text'] = ""
                    self.last_clicked_button = None
                    self.selected_letter = None   
                    self.check_win_dourada()    
                    self.switch = 2
                    self.ia.turno_IA(-math.inf, math.inf, 5)
                #Movimento da peça prata    
                else:
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
          
# ================== CONDIÇÕES DE VITÓRIA ==================
    def check_win_dourada(self):
        for position in self.posicoes_douradas:
            row, col = position
            if self.tabuleiro[row][col]['text'] == "@":
                if row == 0 or row == self.linhas - 1 or col == 0 or col == self.colunas - 1:
                    self.desativar_tabuleiro()
                    messagebox.showinfo("Vitória das douradas", "Você ganhou!")
                    exit()
        return False

    def check_win_prata(self):
        for position in self.posicoes_douradas:
            row, col = position
            if self.tabuleiro[row][col]['text'] == "@":
                return False

        self.desativar_tabuleiro()
        messagebox.showinfo("Vitória das pratas", "Você Perdeu!")
        exit()
        
# ============= CONTROLE DE INFORMAÇÃO DAS PEÇAS ==================
    def get_button_position(self, button):
        for i in range(self.linhas):
            for j in range(self.colunas):
                if self.tabuleiro[i][j] == button:
                    return i, j
                        
    def get_button(self, row, col):
        return self.tabuleiro[row][col]
            
    def start_pieces(self, tabuleiro):
        linha_central = self.linhas // 2
        coluna_central = self.colunas // 2

        tabuleiro[linha_central][coluna_central].config(text="@", font=('Arial', 9, 'bold'), fg="yellow")
        self.posicoes_douradas.append((linha_central, coluna_central))

        for i in range(linha_central - 1, linha_central + 2):
            for j in range(coluna_central - 1, coluna_central + 2):
                if (i, j) != (linha_central, coluna_central):
                    tabuleiro[i][j].config(text="X", font=('Arial', 9, 'bold'), fg="yellow")
                    self.posicoes_douradas.append((i, j))

        for i in range(2, 5):  
            tabuleiro[i][0].config(text="O", font=('Arial', 9, 'bold'), fg="silver")
            self.posicoes_pratas.append((i, 0))
                  
            tabuleiro[i][-1].config(text="O", font=('Arial', 9, 'bold'), fg="silver")
            self.posicoes_pratas.append((i, self.colunas - 1))

        for j in range(2, 5):  
            tabuleiro[0][j].config(text="O", font=('Arial', 9, 'bold'), fg="silver")
            self.posicoes_pratas.append((0, j))
                  
            tabuleiro[-1][j].config(text="O", font=('Arial', 9, 'bold'), fg="silver")
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
            newroot = tk.Tk()
            newroot.title("BreakThru")
            newroot.resizable(False, False)
            tabuleiro = self.criar_tabuleiro(newroot)
            self.start_pieces(tabuleiro)

        def sair():
            root.destroy()
                  
        btn_jogar = tk.Button(root, text="Jogar", command=jogar, width=15, height=2, font=('Arial', 15, 'bold'), bg="white")
        btn_jogar.pack(pady=(250, 10))
        btn_sair = tk.Button(root, text="Sair", command=sair, width=15, height=2, font=('Arial', 12, 'bold'), bg="white")
        btn_sair.pack(pady=10)
        root.mainloop()


class IA_functions:
    
    def __init__(self, game):
        self.game = game     
            
    def turno_IA(self, alpha, beta, depth):
        if len(self.game.posicoes_pratas) > 0:
            _, chosen_play = self.minimax_alpha_beta(depth, alpha, beta, True)
            if chosen_play is not None:
                last_row, last_col, row, col = chosen_play
                self.game.move_piece(row, col, last_row, last_col)
            else:
                print("Não há jogadas possíveis para a IA")
        else:
            self.game.desativar_tabuleiro()
            messagebox.showinfo("Vitória das douradas", "O inimigo não tem mais peças para jogar! Você ganhou!")
            exit()
                  
    
    def number_piece(self):
        return len(self.game.posicoes_douradas) - len(self.game.posicoes_pratas)
    
    def group_in_flagship(self):
        total_distance_to_flagship = 0
        for position in self.game.posicoes_pratas:
            row, col = position
            for goal_position in self.game.posicoes_douradas:
                goal_row, goal_col = goal_position
                distance_to_flagship = abs(row - goal_row) + abs(col - goal_col)
                total_distance_to_flagship += distance_to_flagship
        return -total_distance_to_flagship

      
    def minimax_alpha_beta(self, depth, alpha, beta, is_maximizing):
        if depth == 0 or self.game.check_win_dourada() or self.game.check_win_prata():
            return self.number_piece(), None
            
        moves = self.possible_moves()
            
        if is_maximizing:
            max_eval = -math.inf
            for tabuleiro in moves:
                evaluation, _ = self.minimax_alpha_beta(depth - 1, alpha, beta, False)
                if evaluation > max_eval:
                    max_eval = evaluation
                    chosen_play = tabuleiro
                alpha = max(alpha, evaluation)
                if beta <= alpha:
                    break
            return max_eval, chosen_play
        else:
            min_eval = math.inf
            for tabuleiro in moves:
                evaluation, _ = self.minimax_alpha_beta(depth - 1, alpha, beta, True)
                if evaluation < min_eval:
                    min_eval = evaluation
                    chosen_play = tabuleiro
                beta = min(beta, evaluation)
                if beta <= alpha:
                    break
            return min_eval, chosen_play
        
    def possible_moves(self):
        moves = []
        check_flagship = []
        check_opponent_piece = []
        random_moves = []
            
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
                                    
                    # Checa se é possível realizar movimento
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
