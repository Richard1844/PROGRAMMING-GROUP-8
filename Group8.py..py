from tkinter import *
from random import randint
from PIL import ImageTk, Image
from tkinter.messagebox import showinfo

# Contains constants for each type of pokemon
# And the name of each pokemon, use instead of magic numbers
class Pokemon():
    CHARIZARD = 1
    BLASTOISE = 2
    VENUSAUR  = 3

    names = ['Charizard', 'Blastoise', 'Venusaur']

# This is one User with credentials, for logging in
class User():
    def __init__ (self, username, password):
        self.username = username
        self.password = password

    def valid_credentials(self, username, password):
        print(self.username, username)
        return self.username == username and self.password == password

# This is one player in the game, there are only ever 2 players
class Player():
    def __init__ (self):
        self.reset()

    def reset (self):
        self.wins   = 0
        self.losses = 0
        self.draws  = 0

# This class takes care of the actual game logic
class Game():
    def __init__ (self):
        self.current_player = 0
        self.player = Player()
        self.enemy = Player()
        self.result_message = ''

    def attack (self, pokemon):
        enemy = randint(1, 3)

        if pokemon == enemy:
            self.draw()
            self.result_message = 'Draw!'

        if pokemon == Pokemon.CHARIZARD:
            if enemy == Pokemon.BLASTOISE:
                self.enemy_wins()
            elif enemy == Pokemon.VENUSAUR:
                self.player_wins()
                result = 'You win!'

        elif pokemon == Pokemon.BLASTOISE:
            if enemy == Pokemon.CHARIZARD:
                self.player_wins()
            elif enemy == Pokemon.VENUSAUR:
                self.enemy_wins()

        elif pokemon == Pokemon.VENUSAUR:
            if enemy == Pokemon.CHARIZARD:
                self.enemy_wins()
            elif enemy == Pokemon.BLASTOISE:
                self.player_wins()

        return '%s VS %s: %s' % (Pokemon.names[pokemon-1], Pokemon.names[enemy-1],
                self.result_message)

    def draw (self):
        self.player.draws += 1
        self.enemy.draws += 1

    def player_wins (self):
        self.player.wins += 1
        self.enemy.losses += 1
        self.result_message = 'You win!'

    def enemy_wins (self):
        self.player.losses += 1
        self.enemy.wins += 1
        self.result_message = 'You lose!'

    def get_score (self, player):
        return '%d/%d/%d' % (player.wins, player.losses, player.draws)

    def get_player_score (self):
        return self.get_score(self.player)

    def get_enemy_score (self):
        return self.get_score(self.enemy)

    def reset (self):
        self.player.reset()
        self.enemy.reset()

    def can_play (self):
        return self.player.wins < 10 and self.player.losses < 10

class App():
    def __init__ (self):
        self.users = []
        self.pokemon_selection = '1'
        self.pokemon_images = []
        self.pokemon_label = None
        self.login_tries = 0

        self.setup_tkinter()

        # add an example user
        self.users.append(User('bob', 'secret123'))
        self.game = Game()

    # Set up TK and login screen
    def setup_tkinter (self):
        self.root = Tk()
        self.root.title("Pokemon Rock-Paper-Scissors: Deluxe Edition")
        self.canvas = Canvas(self.root, width=440, height=300)

        self.login_frame = Frame(self.canvas, relief=GROOVE, borderwidth=2)

        self.user_input = StringVar()
        self.pass_input = StringVar()

        usern = Entry(self.login_frame, textvariable=self.user_input)
        usern.pack()
        passw = Entry(self.login_frame, textvariable=self.pass_input)
        passw.pack()

        self.canvas.create_window(2, 0, window=self.login_frame, anchor=NW)
        btnButton=Button(self.login_frame, text="Log in",
                command=self.try_login).pack(fill="none", expand="True")

    def setup_game_screen (self):
        # clear the screen
        self.login_frame.pack_forget()
        self.login_frame.destroy()

        # Setup game screen
        image_files = ['Charizard.png', 'Blastoise.png', 'Venusaur.png']

        for i in image_files:
            img = Image.open(i)
            img = img.resize((200, 200), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            self.pokemon_images.append(img)

        # Setup scores
        score_frame = Frame(self.canvas, relief=GROOVE, borderwidth=2,
                padx=5)
        Label(master=score_frame, text='Score (You/Enemy) (Win/Loss/Draw):').pack(side=LEFT)
        self.player_score = StringVar()
        self.enemy_score = StringVar()
        Label(master=score_frame, textvariable=self.player_score).pack(side=LEFT)
        Label(master=score_frame, textvariable=self.enemy_score).pack(side=LEFT)
        self.canvas.create_window(2, 0, window=score_frame, anchor=NW)

        # Setup pokemon image
        img = self.pokemon_images[0]
        p_frame = Frame(self.canvas, relief=GROOVE, borderwidth=2)
        self.pokemon_label = Label(p_frame, image = img)
        self.pokemon_label.image = img
        self.pokemon_label.pack(fill="both", expand="yes")
        btnButton=Button(p_frame, fg='red', text="Attack",
                command=self.attack_clicked).pack(fill="none", expand="True")
        self.canvas.create_window(150, 40, window=p_frame, anchor=NW)

        # Setup top menu
        menu = Menu(self.root)
        self.root.config(menu=menu)
        subMenu = Menu(menu)
        subMenu.add_command(label="Quit", command=self.on_quit_clicked)
        menu.add_cascade(label="File",menu=subMenu)
        menu.add_command(label="Rules",command=self.on_rules_clicked)
        menu.add_command(label="Restart",command=self.on_restart_clicked)

        # Select Pokemon option buttons
        frm0 = Frame(self.canvas, relief=GROOVE, borderwidth=2)
        Label(frm0, text='Choice:').pack(fill="none", expand="True")
        self.canvas.create_window(0, 40, window=frm0, anchor=NW)
        self.pokemon_selection = IntVar(frm0, 1)

        button_values = [('Charizard', '1'),
                ('Blastoise', '2'),
                ('Venusaur', '3')]

        for key, value in button_values:
            Radiobutton(frm0, text=key, variable=self.pokemon_selection,
                        value=value, command=self.on_pokemon_clicked).pack()

        # Setup game result
        self.result_text = StringVar()
        self.result_text.set('')
        result_frame = Frame(self.canvas, relief=GROOVE, borderwidth=2)
        Label(master=result_frame, textvariable=self.result_text).pack()
        self.canvas.create_window(200, 290, window=result_frame)
        self.update_scores()

    def on_pokemon_clicked (self):
        pokemon = self.pokemon_selection.get()
        img = self.pokemon_images[pokemon-1]
        self.pokemon_label.configure(image = img)
        self.pokemon_label.image = img

    def attack_clicked (self):
        if self.game.can_play():
            pokemon = self.pokemon_selection.get()
            attack_result = self.game.attack(pokemon)
            self.update_scores()
            self.result_text.set(attack_result)
        else:
            showinfo('Sorry', 'You can\'t play any more')

    def on_quit_clicked (self):
        exit()

    def on_rules_clicked (self):
        showinfo('Rules', 'Charizard beats Venusaur. Venusaur beats Blastoise. Blastoise beats Charizard.')

    def on_restart_clicked (self):
        self.game.reset()
        self.update_scores()
        self.result_text.set('')

    def update_scores (self):
        self.player_score.set(self.game.get_player_score())
        self.enemy_score.set(self.game.get_enemy_score())

    def run (self):
        self.canvas.pack()
        self.root.mainloop()

    # takes a username and password, and tries to find a User object
    # with the same credentials
    def try_login (self):
        username = self.user_input.get()
        password = self.pass_input.get()
        found = False

        for user in self.users:
            if user.valid_credentials(username, password):
                found = True
                break

        if found:
            self.setup_game_screen()
        else:
            self.login_tries += 1

            if self.login_tries == 3:
                exit()

app = App()
app.run()

