import customtkinter as ctk
import copy

# Imports de tes modules
from sudoku_engine import init_game, has_error, is_victory
from infos import start_timer, stop_timer, get_system_stats
from backtracking import resoudre_sudoku
from force_brute import resoudre_force_brute
from force_brute_dichotomique import resoudre_optimise

# --- Palette de couleurs ---
COLORS = {
    "bg": "#0f0f14", "surface": "#1a1a24", "border_thin": "#2e2e42",
    "border_thick": "#c8a96e", "text_fixed": "#e8e6f0", "text_player": "#7c6fcd",
    "error_bg": "#3a1c20", "error_text": "#e05c6a", "success": "#5cc98a",
    "success_flash": "#2e7a4d", "info": "#4da6ff"
}

class SudokuApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku - Édition Premium & Benchmark")
        self.geometry("600x850") # Fenêtre un peu plus haute pour les stats
        self.configure(fg_color=COLORS["bg"])
        ctk.set_appearance_mode("dark")
        
        self.cells = {}
        self.completed_groups = set()
        self.show_menu()

    # ─── VUES (Menu, Jeu, Solveur) ───────────────────────────────────────────

    def show_menu(self):
        self.clear_window()
        menu_frame = ctk.CTkFrame(self, fg_color="transparent")
        menu_frame.pack(expand=True, fill="both", padx=40, pady=80)

        ctk.CTkLabel(menu_frame, text="✦ JEU & ALGORITHMES ✦", font=("DM Sans", 14, "bold"), text_color=COLORS["border_thick"]).pack(pady=(0, 10))
        ctk.CTkLabel(menu_frame, text="SUDOKU", font=("Playfair Display", 60, "bold"), text_color=COLORS["text_fixed"]).pack(pady=(0, 20))
        
        sep = ctk.CTkFrame(menu_frame, width=80, height=3, fg_color=COLORS["border_thick"], corner_radius=2)
        sep.pack(pady=(0, 40))

        # Bouton Mode Joueur
        btn_play = ctk.CTkButton(
            menu_frame, text="▶ JOUER UNE PARTIE", font=("DM Sans", 16, "bold"),
            height=50, fg_color=COLORS["surface"], border_width=2,
            border_color=COLORS["border_thick"], text_color=COLORS["border_thick"],
            hover_color="#2a241c", command=self.start_game
        )
        btn_play.pack(fill="x", padx=50, pady=10)

        # Bouton Mode Solveur
        btn_solve = ctk.CTkButton(
            menu_frame, text="⚙️ BENCHMARK SOLVEUR", font=("DM Sans", 16, "bold"),
            height=50, fg_color=COLORS["surface"], border_width=2,
            border_color=COLORS["info"], text_color=COLORS["info"],
            hover_color="#1c2a3a", command=self.start_solver
        )
        btn_solve.pack(fill="x", padx=50, pady=10)

    def build_header(self, title_text, color):
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(20, 10))
        self.lbl_status = ctk.CTkLabel(header, text=title_text, font=("Playfair Display", 28, "bold"), text_color=COLORS["text_fixed"])
        self.lbl_status.pack(side="left")
        btn_menu = ctk.CTkButton(header, text="🏠 Menu", width=80, fg_color=COLORS["surface"], hover_color="#252533", command=self.show_menu)
        btn_menu.pack(side="right", padx=(10, 0))

    def build_grid_ui(self, is_interactive=True):
        main_grid_frame = ctk.CTkFrame(self, fg_color=COLORS["border_thick"], corner_radius=0)
        main_grid_frame.pack(pady=10, padx=20)

        for block_y in range(3):
            for block_x in range(3):
                block_frame = ctk.CTkFrame(main_grid_frame, fg_color=COLORS["border_thick"], corner_radius=0)
                block_frame.grid(row=block_y, column=block_x, padx=1.5, pady=1.5)

                for cell_y in range(3):
                    for cell_x in range(3):
                        y, x = block_y * 3 + cell_y, block_x * 3 + cell_x
                        val = self.player_grid[y][x]
                        is_fixed = self.fixed[y][x]

                        cell = ctk.CTkEntry(
                            block_frame, width=45, height=45,
                            justify="center", font=("DM Sans", 22, "bold"),
                            corner_radius=0, border_width=1, border_color=COLORS["border_thin"]
                        )
                        cell.grid(row=cell_y, column=cell_x, padx=0.5, pady=0.5)
                        self.cells[(y, x)] = cell

                        if is_fixed:
                            cell.insert(0, str(val))
                            cell.configure(state="disabled", fg_color=COLORS["surface"], text_color=COLORS["text_fixed"])
                        else:
                            if val != ' ': cell.insert(0, str(val))
                            if not is_interactive:
                                cell.configure(state="disabled", fg_color="#252533", text_color=COLORS["info"])
                            else:
                                cell.configure(fg_color="#252533", text_color=COLORS["text_player"])
                                cell.bind("<KeyRelease>", lambda e, r=y, c=x: self.on_key_release(e, r, c))
                                cell.bind("<Up>", lambda e, r=y, c=x: self.move_focus(r-1, c))
                                cell.bind("<Down>", lambda e, r=y, c=x: self.move_focus(r+1, c))
                                cell.bind("<Left>", lambda e, r=y, c=x: self.move_focus(r, c-1))
                                cell.bind("<Right>", lambda e, r=y, c=x: self.move_focus(r, c+1))

    # ─── MODE JOUER ──────────────────────────────────────────────────────────

    def start_game(self):
        self.clear_window()
        self.solution, self.fixed, self.puzzle, self.player_grid = init_game()
        self.cells.clear()
        self.completed_groups.clear()
        self.build_header("SUDOKU", COLORS["text_fixed"])
        self.build_grid_ui(is_interactive=True)
        self.refresh_all_colors()

    # (Ici se trouvent les fonctions on_key_release, update_errors, animate_flash du code précédent)
    # J'ai gardé la même logique pour le mode joueur
    def on_key_release(self, event, y, x):
        if event.keysym in ["Up", "Down", "Left", "Right", "Tab"]: return
        cell = self.cells[(y, x)]
        val = cell.get()
        if len(val) > 1:
            val = val[-1]
            cell.delete(0, 'end')
            cell.insert(0, val)

        if val in "123456789": self.player_grid[y][x] = int(val)
        else:
            self.player_grid[y][x] = ' '
            cell.delete(0, 'end')

        self.refresh_all_colors()
        self.check_victory()

    def refresh_all_colors(self):
        for (y, x), cell in self.cells.items():
            if not self.fixed[y][x]:
                if self.player_grid[y][x] != ' ' and has_error(self.player_grid, y, x):
                    cell.configure(fg_color=COLORS["error_bg"], text_color=COLORS["error_text"])
                else:
                    cell.configure(fg_color="#252533", text_color=COLORS["text_player"])

    def check_victory(self):
        if is_victory(self.player_grid, self.solution):
            self.lbl_status.configure(text="🎉 VICTOIRE !", text_color=COLORS["success"])
            for cell in self.cells.values(): cell.configure(state="disabled")

    def move_focus(self, y, x):
        new_y, new_x = y % 9, x % 9
        target_cell = self.cells[(new_y, new_x)]
        if target_cell.cget("state") != "disabled": target_cell.focus()
        else:
            if y != new_y: self.move_focus(new_y + (1 if y > new_y else -1), new_x)
            elif x != new_x: self.move_focus(new_y, new_x + (1 if x > new_x else -1))

    # ─── MODE SOLVEUR & BENCHMARK ────────────────────────────────────────────

    def start_solver(self):
        self.clear_window()
        self.solution, self.fixed, self.puzzle, self.player_grid = init_game()
        self.cells.clear()

        self.build_header("BENCHMARK", COLORS["info"])
        self.build_grid_ui(is_interactive=False) # Grille en lecture seule

        # Panneau de contrôle
        ctrl_frame = ctk.CTkFrame(self, fg_color="transparent")
        ctrl_frame.pack(fill="x", padx=30, pady=10)

        self.algo_var = ctk.StringVar(value="Backtracking Classique")
        dropdown = ctk.CTkOptionMenu(
            ctrl_frame, variable=self.algo_var,
            values=["Backtracking Classique", "Force Brute (Lent)", "MRV Optimisé (Rapide)"],
            fg_color=COLORS["surface"], button_color=COLORS["border_thin"]
        )
        dropdown.pack(side="left", fill="x", expand=True, padx=(0, 10))

        btn_run = ctk.CTkButton(ctrl_frame, text="▶ RÉSOUDRE", command=self.run_algorithm, fg_color=COLORS["info"], hover_color="#2b7bcf")
        btn_run.pack(side="right")

        # Panneau des statistiques
        self.stats_frame = ctk.CTkFrame(self, fg_color=COLORS["surface"])
        self.stats_frame.pack(fill="x", padx=30, pady=10)
        self.lbl_stats = ctk.CTkLabel(self.stats_frame, text="En attente...", font=("DM Sans", 14), justify="left")
        self.lbl_stats.pack(padx=15, pady=15)

    def run_algorithm(self):
        self.lbl_status.configure(text="Calcul...", text_color=COLORS["border_thick"])
        self.lbl_stats.configure(text="Résolution en cours...\n(L'interface peut figer brièvement)")
        self.update() # Force l'interface à s'actualiser avant le gel du calcul

        algo = self.algo_var.get()
        grille_test = copy.deepcopy(self.puzzle)

        # Lancement chronomètre et stats initiales
        t0 = start_timer()

        # Exécution selon le choix
        if algo == "Backtracking Classique":
            resoudre_sudoku(grille_test)
        elif algo == "Force Brute (Lent)":
            resoudre_force_brute(grille_test)
        elif algo == "MRV Optimisé (Rapide)":
            resoudre_optimise(grille_test)

        # Fin chronomètre et stats finales
        t_total = stop_timer(t0)
        system_stats = get_system_stats()

        # Affichage des résultats
        self.player_grid = grille_test
        self.update_solved_grid_ui()
        self.lbl_status.configure(text="TERMINÉ", text_color=COLORS["success"])
        
        # Mise en page des infos
        stats_text = (
            f"⏱️ Temps : {t_total:.4f} secondes\n"
            f"🧠 CPU : {system_stats['cpu_usage']} ({system_stats['cpu_cores']} cœurs)\n"
            f"💾 RAM : {system_stats['ram_used']} utilisés ({system_stats['ram_percent']})"
        )
        self.lbl_stats.configure(text=stats_text)

    def update_solved_grid_ui(self):
        for y in range(9):
            for x in range(9):
                if not self.fixed[y][x]:
                    cell = self.cells[(y, x)]
                    cell.configure(state="normal")
                    cell.delete(0, "end")
                    cell.insert(0, str(self.player_grid[y][x]))
                    cell.configure(state="disabled", text_color=COLORS["info"]) # Chiffres résolus en bleu

    # ─── UTILITAIRES ─────────────────────────────────────────────────────────
    def clear_window(self):
        for widget in self.winfo_children(): widget.destroy()

if __name__ == "__main__":
    app = SudokuApp()
    app.mainloop()