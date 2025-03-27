import pygame
import random
from collections import deque

GAMESCREEN_WIDTH = 800
GAMESCREEN_HEIGHT = 600
SCREEN_WIDTH = 1200
FPS = 60

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
FREE = 'Computer-safe.png'
PROTECTED = 'Computer-protected.png'
HACKED = 'Computer-hacked.png'


arrow_q = deque()


class PopupArrow:
    def __init__(self, x1, y1, x2, y2, color):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.timer = 60

    def draw(self):
        pygame_facade.draw_line(self.x1, self.y1, self.x2, self.y2, self.color, 3)
        pygame_facade.draw_rectangle(self.x2 - 25, self.y2 - 25, 50, 50, self.color)
        self.timer -= 1


class Computer:
    def __init__(self, x, y, num):
        self.x = x
        self.y = y
        self.num = num
        self.power = random.randint(1, 3)
        self.connections = []
        self.occupied = FREE
        self.defence = random.randint(1, 4)

    def add_connection(self, c):
        self.connections.append(c)

    def __str__(self):
        return 'IP:' + str(self.num) + '\n' + 'Files: *REDACTED*\n' + 'Position: ' + str(self.x) + ' ' + str(self.y) + '\n' + 'Connections:' + str(self.connections)

    def draw(self):
        image = pygame_facade.load_image(self.occupied)
        pygame_facade.draw_image(image, (self.x - 20, self.y - 20))
        pygame_facade.write_text((self.x+10, self.y - 30), str(self.defence), 'Arial', 14, GREEN)
        pygame_facade.write_text((self.x+10, self.y + 10), str(self.power), 'Arial', 14, YELLOW)

    def get_uninfected(self):
        ans = []
        for c in self.connections:
            if comp_list[c].occupied != HACKED:
                ans.append(c)
        return ans


class PygameFacade:
    attacked = False    # Blocking stuff when attacked
    menumode = 'menu'    # Tech variable, used stop rendering menu buttons when info is open and otherwise
    moved = -1    # Drag and drop a computer!
    money = 1   # $$$
    av_price = 1    #Technical stuff
    av_av = 0   #How much antivirus you have
    using_av = False    # Tech stuff
    turns_left = -1 # How much left to survive
    power_upgrades = 0  # MORE $$$
    power_upgrades_applied = 0
    upgrading_power = False    #Even more tech stuff
    def_upgrades = 0    # P  R  O  T  E  C  C
    def_upgrades_applied = 0
    upgrading_def = False   #Yet here we are, just to suffer


    def __init__(self, screen_size, caption='No name'):
        """
        creates the game, lmao
        :param screen_size: size of screen
        :param caption: name of app
        """
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.money = 1
        self.av_price = 1
        self.turn = 0

    def draw_circle(self, x, y, color, radius):
        """
        :param x: center position
        :param y: same
        :param color: color bruh
        :param radius: radius of drawn circle
        :return: none
        """
        pygame.draw.circle(self.screen, color, (x, y), radius)

    def draw_rectangle(self, x, y, width, height, color):
        """
        draws a rectangle
        :param x: top left corner x
        :param y: top left corner y
        :param width: width of rect
        :param height: height of rect
        :param color: rect color
        :return: none
        """
        pygame.draw.rect(self.screen, color, pygame.Rect(x, y, width, height))

    def draw_poly(self, color, pointlist):
        """
        draws a polygon
        :param color: color of poly
        :param pointlist: list of (x, y) tuples to define points
        :return: none
        """
        pygame.draw.polygon(self.screen, color, pointlist, 0)

    def draw_line(self, x1, y1, x2, y2, color, width):
        """
        draws a line
        :param x1: start x
        :param y1: start y
        :param x2: end x
        :param y2: end y
        :param color: line color
        :param width: line width in px
        :return: none
        """
        pygame.draw.line(self.screen, color, (x1, y1), (x2, y2), width)

    @staticmethod
    def de_bg(imaga, colorkey=None):  # for deleting image bg
        """
        deletes image bg
        :param imaga: image
        :param colorkey: the color that gets removed
        :return: image without bg
        """
        imaga = imaga.convert_alpha()
        if colorkey is not None:
            if colorkey == -1:
                colorkey = imaga.get_at((0, 0))
            imaga.set_colorkey(colorkey)
        return imaga

    def load_image(self, imga):
        """
        loads an image with removed background
        :param imga: name of inage in files
        :return: loaded image
        """
        img = pygame.image.load(imga)
        out = self.de_bg(img)
        return out

    def draw_image(self, img, coords):
        """
        draws a loaded image
        :param img: the image that you loaded
        :param coords: coordinates of top left angle
        :return: none
        """
        self.screen.blit(img, coords)

    @staticmethod
    def update_screen():
        """
        updates screen
        :return: none
        """
        pygame.display.flip()

    def clear_screen(self):
        self.screen.fill((0, 0, 0))

    def write_text(self, coords, text, fontt, size, color):
        font = pygame.font.SysFont(fontt, size)
        text_surface = font.render(text, True, color)
        self.screen.blit(text_surface, coords)

    def attack(self):
        if self.attacked:
            pass
        else:
            self.backup = []
            for i in comp_list:
                self.backup.append(Computer(i.x, i.y, i.num))
                self.backup[-1].connections = i.connections
                self.backup[-1].power = i.power
                self.backup[-1].occupied = i.occupied
                self.backup[-1].defence = i.defence
            self.attacked = True
            self.virus = VirusAI()
            self.turns_left = 2*len(comp_list)


    def buy_av(self):
        if self.money < self.av_price ** 2:
            print('Not enough $$$')
        else:
            self.money -= self.av_price ** 2
            self.av_price += 1
            self.av_av += 1

    def use_av(self):
        if self.attacked is False and self.av_av > 0 and self.using_av is False and self.upgrading_power is False and self.upgrading_def is False:
            self.av_av -= 1
            self.using_av = True

    def buy_pu(self):
        if self.money < 1:
            print('Not enough $$$')
        else:
            self.money -= 1
            self.power_upgrades += 1

    def buy_du(self):
        if self.money < 2:
            print('Not enough $$$')
        else:
            self.money -= 2
            self.def_upgrades += 1

    def use_pu(self):
        if self.attacked is False and self.power_upgrades > 0 and self.using_av is False and self.upgrading_power is False and self.upgrading_def is False:
            self.power_upgrades_applied = self.power_upgrades
            self.power_upgrades = 0
            self.upgrading_power = True

    def use_du(self):
        if self.attacked is False and self.def_upgrades > 0 and self.using_av is False and self.upgrading_power is False and self.upgrading_def is False:
            self.def_upgrades_applied = self.def_upgrades
            self.def_upgrades = 0
            self.upgrading_def = True

    def end_turn(self):
        """
        Ends the turn, checks if anyone won
        :return: none lol
        """
        for v in comp_list:
            if v.occupied == FREE:
                v.defence += 1
            else:
                v.defence += 2
        num_n = 0
        for i in comp_list:
            if i.occupied == HACKED:
                num_n += 1
        if num_n != 0:
            self.virus.atk()
        num_y = 0
        num_n = 0
        for i in comp_list:
            if i.occupied == HACKED:
                num_n += 1
            else:
                num_y += 1
        if num_y == 0:
            print('You lost', end='')
            pygame.quit()
            exit(0)
        elif num_n == 0:
            print('no virus?')
            self.attacked = False
            self.turns_left = 1
        self.turns_left -= 1

    def show_info(self):
        self.menumode = 'info'

    def back_to_menu(self):
        self.menumode = 'menu'


class Button(pygame.Rect):
    """
    A wrapper, perhaps? Nah, using classes
    """
    def __init__(self, command, x, y, width, height, color, params):
        """
        Create your Button, command should be put in other classes cuz incapsulation
        :param command: What the button does
        :param x: where button
        :param y: where button
        :param width: x size of button
        :param height: y size of button
        :param color: color of your Button
        """
        super().__init__(x, y, width, height)
        self.command = command
        self.color = color
        self.params = params

    def activate(self):
        """
        run if button is pressed
        """
        self.command(self.params)

    def draw(self):
        """
        draws the button
        """
        pygame_facade.draw_rectangle(self.x, self.y, self.w, self.h, self.color)


class VirusAI:
    def __init__(self):
        self.strat = random.randint(1, 2) #Up to 5
        self.nxt = -1
        startnode = random.randint(0, len(comp_list)-1)
        self.inf = dict()
        self.inf[startnode] = 1
        comp_list[startnode].occupied = HACKED #If this is ur antivirus bastion, then womp womp
        m_def = 0
        for i in comp_list:
            if i.defence > m_def:
                m_def = i.defence
        comp_list[startnode].defence = m_def + random.randint(-3, 3)

    def atk(self):
        if self.strat == 1:
            self.bfs()
        elif self.strat == 2:
            self.dfs()

    def bfs(self):
        for y in self.inf.keys():
            if self.inf[y] == 1:
                for x in comp_list[y].connections:
                    if comp_list[x].occupied != HACKED:
                        comp_list[x].defence -= comp_list[y].defence
                        if comp_list[x].defence <= 0:
                            comp_list[x].defence = abs(comp_list[x].defence)
                            comp_list[y].defence = comp_list[x].defence // 2
                            comp_list[x].defence //= 2
                            self.inf[x] = 1
                            comp_list[x].occupied = HACKED
                            comp_list[x].defence += 2
                        else:
                            comp_list[y].defence = max(0, comp_list[y].defence - random.randint(2, 5))
                        arrow_q.append(PopupArrow(comp_list[y].x, comp_list[y].y, comp_list[x].x, comp_list[x].y, RED))
                        return y, x

    # noinspection PyUnboundLocalVariable
    def dfs(self):
        for y in self.inf.keys():
            if self.inf[y] == 1:
                for x in comp_list[y].connections:
                    if comp_list[x].occupied != HACKED:
                        max_x = x
        comp_list[max_x].defence -= comp_list[y].defence
        comp_list[y].defence = 1
        arrow_q.append(PopupArrow(comp_list[y].x, comp_list[y].y, comp_list[max_x].x, comp_list[max_x].y, RED))
        if comp_list[max_x].defence <= 0:
            self.inf[max_x] = 1
            comp_list[max_x].occupied = HACKED
            comp_list[max_x].defence *= -1
            return max_x


num_c = 0
c_list = []
pygame_facade = PygameFacade((SCREEN_WIDTH, GAMESCREEN_HEIGHT), "Viral")
chosen_to_spread_av = None

def edge_tree_generate(num):
    root = []
    left = []
    for q in range(1, num-1):
        left.append(q)
    riblist = []
    root.append(0)
    while len(left) > 0:
        s = root[random.randint(0, len(root)-1)]
        f = left[random.randint(0, len(left) - 1)]
        riblist.append((s, f))
        left.remove(f)
        root.append(f)
    return riblist

def startup():
    for i in range(random.randint(9, 12)):
        ok = False
        x = random.randint(30, GAMESCREEN_WIDTH - 30)
        y = random.randint(30, GAMESCREEN_HEIGHT - 30)
        while ok is False:
            x -= 1
            y -= 1
            x += 1
            y += 1   #Do not ask why, synchronisation
            x = random.randint(30, GAMESCREEN_WIDTH - 30)
            y = random.randint(30, GAMESCREEN_HEIGHT - 30)
            ok = True
            for c in c_list:
                if c.x - 40 <= x <= c.x + 40 and c.y - 40 <= y <= c.y + 40: #Prevents clipping
                    ok = False
            if c_list == []:
                ok = True
        c_list.append(Computer(x, y, i))
    return c_list

def add_edge(amount):
    """
    Adds an edge
    :param amount: amount of needed edges
    :return:
    """
    for g in range(amount):
        s = random.randint(0, len(c_list) - 1)
        ok = False
        while ok is False:
            f = random.randint(0, len(c_list) - 1)
            if f not in comp_list[s].connections and f != s:
                ok = True
                comp_list[s].connections.append(f)
                comp_list[f].connections.append(s)
                print(f, s)

comp_list = startup()
edge_list = edge_tree_generate(len(comp_list)+1)
for i in edge_list:
    comp_list[i[0]].add_connection(i[1])
    comp_list[i[1]].add_connection(i[0])
add_edge(7)
for i in comp_list:
    print(i)
    print('------------------')


buy_anti_virus_button = Button(PygameFacade.buy_av, GAMESCREEN_WIDTH + 30, 170, 340, 50, GREEN, PygameFacade)
attack_button = Button(PygameFacade.attack, GAMESCREEN_WIDTH + 30, 230, 340, 50, GREEN, PygameFacade)
info_button = Button(PygameFacade.show_info, SCREEN_WIDTH - 30, 0, 30, 30, GREEN, PygameFacade)
anti_info_button = Button(PygameFacade.back_to_menu, GAMESCREEN_WIDTH + 30, GAMESCREEN_HEIGHT - 50, 340, 50, GREEN, PygameFacade)
use_av_button = Button(PygameFacade.use_av, GAMESCREEN_WIDTH + 30, 290, 340, 50, GREEN, PygameFacade)
buy_powerup_button = Button(PygameFacade.buy_pu, GAMESCREEN_WIDTH + 30, 350, 340, 50, GREEN, PygameFacade)
use_powerup_button = Button(PygameFacade.use_pu, GAMESCREEN_WIDTH + 30, 410, 340, 50, GREEN, PygameFacade)
buy_defence_button = Button(PygameFacade.buy_du, GAMESCREEN_WIDTH + 30, 470, 340, 50, GREEN, PygameFacade)
use_defence_button = Button(PygameFacade.use_du, GAMESCREEN_WIDTH + 30, 530, 340, 50, GREEN, PygameFacade)
end_turn_button = Button(PygameFacade.end_turn, SCREEN_WIDTH - 60, GAMESCREEN_HEIGHT - 30, 60, 30, GREEN, PygameFacade)


menu_buttons = [attack_button, info_button, buy_anti_virus_button, use_av_button, buy_powerup_button, use_powerup_button, buy_defence_button, use_defence_button]

#TEST ZONE

#TEST ZONE END

running = True
while running:
    #attack_end
    if PygameFacade.turns_left == 0:
        PygameFacade.turns_left = -1
        for i in comp_list:
            if i.occupied != HACKED:
                PygameFacade.money += i.power
        PygameFacade.attacked = False
        comp_list = []
        for i in PygameFacade.backup:
            comp_list.append(i)
        comp_list.append(Computer(random.randint(20, GAMESCREEN_WIDTH - 20), random.randint(20, GAMESCREEN_HEIGHT - 20), len(comp_list)))
        for i in range(random.randint(1, 4)):
            yup = False
            while yup is False:
                new = random.randint(0, len(comp_list) - 2)
                if new not in comp_list[-1].connections:
                    comp_list[-1].connections.append(new)
                    yup = True
        for i in comp_list[-1].connections:
            comp_list[i].connections.append(len(comp_list) - 1)
    mx, my = pygame.mouse.get_pos()
    # event processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mx > GAMESCREEN_WIDTH:    # Button press
                if PygameFacade.menumode == 'menu':
                    for button in menu_buttons:
                        if button.collidepoint(mx, my):
                            button.activate()
                    if PygameFacade.attacked is True:
                        if end_turn_button.collidepoint(mx, my):
                            end_turn_button.activate()
                if PygameFacade.menumode == 'info':
                    if anti_info_button.collidepoint(mx, my):
                        anti_info_button.activate()
            elif not PygameFacade.attacked:
                for i in comp_list:
                    if i.x - 20 <= mx <= i.x + 20 and i.y - 20 <= my <= i.y + 20:
                        if i.occupied != PROTECTED and PygameFacade.using_av is True:
                            i.defence *= 2
                            i.occupied = PROTECTED
                            PygameFacade.using_av = False
                        elif PygameFacade.upgrading_power is True:
                            i.power += PygameFacade.power_upgrades_applied
                            PygameFacade.power_upgrades_applied = 0
                            PygameFacade.upgrading_power = False
                        elif PygameFacade.upgrading_def is True:
                            i.defence += PygameFacade.def_upgrades_applied
                            PygameFacade.def_upgrades_applied = 0
                            PygameFacade.upgrading_def = False
                        else:
                            PygameFacade.moved = i.num
            else:
                for i in comp_list:
                    if i.x - 20 <= mx <= i.x + 20 and i.y - 20 <= my <= i.y + 20:
                        if i.occupied == PROTECTED:
                            chosen_to_spread_av = i
                        if i.occupied == FREE and chosen_to_spread_av is not None:
                            if chosen_to_spread_av.num in i.connections:
                                arrow_q.append(PopupArrow(chosen_to_spread_av.x, chosen_to_spread_av.y, i.x, i.y, BLUE))
                                i.occupied = PROTECTED
                                i.defence *= 2
                                chosen_to_spread_av = None
                                end_turn_button.activate()
                        if i.occupied == HACKED and chosen_to_spread_av is not None:
                            if chosen_to_spread_av.num in i.connections:
                                arrow_q.append(PopupArrow(chosen_to_spread_av.x, chosen_to_spread_av.y, i.x, i.y, BLUE))
                                if chosen_to_spread_av.defence >= i.defence:
                                    i.occupied = PROTECTED
                                    PygameFacade.virus.inf[i.num] = 0
                                    n = (chosen_to_spread_av.defence - i.defence)//2
                                    i.defence = n
                                    chosen_to_spread_av.defence = n
                                    chosen_to_spread_av = None
                                    end_turn_button.activate()
                                else:
                                    i.defence -= chosen_to_spread_av.defence // 2
                                    chosen_to_spread_av.defence -= chosen_to_spread_av.defence // 2
                                    chosen_to_spread_av = None
                                    end_turn_button.activate()
        if event.type == pygame.MOUSEBUTTONUP:
            PygameFacade.moved = -1

    pygame_facade.clear_screen()
    pygame_facade.draw_rectangle(GAMESCREEN_WIDTH, 0, SCREEN_WIDTH - GAMESCREEN_HEIGHT, GAMESCREEN_HEIGHT, WHITE)

    #Test zone 2


    #Drawing computers, edges and attack paths
    if chosen_to_spread_av is not None and PygameFacade.attacked is True:
        pygame_facade.draw_circle(chosen_to_spread_av.x, chosen_to_spread_av.y, BLUE, 25)
    for i in comp_list:
        for f in i.connections:
            pygame_facade.draw_line(i.x, i.y, comp_list[f].x, comp_list[f].y, WHITE, 3)
    pops = 0
    for i in arrow_q:
        i.draw()
        if i.timer == 0:
            pops += 1
    for i in range(pops):
        arrow_q.popleft()
    for i in comp_list:
        i.draw()

    #Moving computers
    if PygameFacade.moved >= 0:
        if 20 <= mx <= GAMESCREEN_WIDTH - 20:
            comp_list[PygameFacade.moved].x = mx
        if 20 <= my <= GAMESCREEN_HEIGHT - 20:
            comp_list[PygameFacade.moved].y = my

    if PygameFacade.menumode == 'menu':
        # Stats
        pygame_facade.write_text((GAMESCREEN_WIDTH + 5, 0), 'Money: ' + str(PygameFacade.money), 'Arial', 24, (125, 125, 0))
        pygame_facade.write_text((GAMESCREEN_WIDTH + 5, 30), 'Antivirus price: ' + str(PygameFacade.av_price**2), 'Arial', 24, (125, 125, 0))
        pygame_facade.write_text((GAMESCREEN_WIDTH + 5, 60), 'Antivirus you have: ' + str(PygameFacade.av_av),'Arial', 24, (125, 125, 0))
        pygame_facade.write_text((GAMESCREEN_WIDTH + 5, 90), 'Power upgrades you have: ' + str(PygameFacade.power_upgrades),'Arial', 24, (125, 125, 0))
        pygame_facade.write_text((GAMESCREEN_WIDTH + 5, 120), 'Defence upgrades you have: ' + str(PygameFacade.def_upgrades),'Arial', 24, (125, 125, 0))
        # Menu buttons
        if PygameFacade.attacked is False:
            for button in menu_buttons: #GUI
                button.draw()
        info_button.draw()
        if PygameFacade.attacked:
            end_turn_button.draw()

        img = pygame_facade.load_image('info-logo.png')
        pygame_facade.draw_image(img, (info_button.x, info_button.y))
        if PygameFacade.attacked is False:
            pygame_facade.write_text((buy_anti_virus_button.x + 80, buy_anti_virus_button.y + 7), 'Buy antivirus','Calibri', 36, BLACK)
            pygame_facade.write_text((attack_button.x + 95, attack_button.y + 7), 'Start attack', 'Calibri', 36, BLACK)
            pygame_facade.write_text((use_av_button.x + 80, use_av_button.y + 7), 'Use antivirus', 'Calibri', 36, BLACK)
            pygame_facade.write_text((buy_powerup_button.x + 80, buy_powerup_button.y + 7), 'Buy powerup', 'Calibri', 36, BLACK)
            pygame_facade.write_text((use_powerup_button.x + 80, use_powerup_button.y + 7), 'Use powerup', 'Calibri', 36, BLACK)
            pygame_facade.write_text((buy_defence_button.x + 80, buy_defence_button.y + 7), 'Buy defence', 'Calibri', 36, BLACK)
            pygame_facade.write_text((use_defence_button.x + 80, use_defence_button.y + 7), 'Use defence', 'Calibri', 36, BLACK)
        if PygameFacade.using_av is True:
            pygame_facade.draw_rectangle(use_av_button.x, use_av_button.y, use_av_button.width, use_av_button.height, GRAY)

        #Attack stuff
        if PygameFacade.attacked is True:
            pygame_facade.write_text((end_turn_button.x+2, end_turn_button.y+8), 'end turn', 'Calibri', 16, BLACK)
            pygame_facade.write_text((attack_button.x + 70, attack_button.y + 7), ('Turns left: '+str(PygameFacade.turns_left)), 'Calibri', 36, RED)



    elif PygameFacade.menumode == 'info': #Showing info
        PygameFacade.write_text(pygame_facade, (GAMESCREEN_WIDTH + 5, 0), 'This is a simulation of a computer network surviving virus attacks.', 'Arial', 14, BLACK)
        PygameFacade.write_text(pygame_facade, (GAMESCREEN_WIDTH + 5, 15), 'The attack starts when you hit the "ATTACK" button.', 'Arial', 14, BLACK)
        PygameFacade.write_text(pygame_facade, (GAMESCREEN_WIDTH + 5, 30), 'After every attack all surviving computers will give you crypto.', 'Arial', 14, BLACK)
        PygameFacade.write_text(pygame_facade, (GAMESCREEN_WIDTH + 5, 45), "You can buy various money upgrades and anti-virus with it", 'Arial', 14, BLACK)
        PygameFacade.write_text(pygame_facade, (GAMESCREEN_WIDTH + 5, 60), "During an attack, anti-virus doubles the computer's defence stat", 'Arial', 14, BLACK)
        PygameFacade.write_text(pygame_facade, (GAMESCREEN_WIDTH + 5, 75), 'and you can spread it during your defensive turn. Attacks last 2n turns,', 'Arial', 14, BLACK)
        PygameFacade.write_text(pygame_facade, (GAMESCREEN_WIDTH + 5, 90), 'where n is the number of computers you have. ', 'Arial', 14, BLACK)
        PygameFacade.write_text(pygame_facade, (GAMESCREEN_WIDTH + 5, 105), 'Helpful stuff:', 'Arial', 14, BLACK)
        PygameFacade.write_text(pygame_facade, (GAMESCREEN_WIDTH + 5, 120), 'You can drag computers with your mouse (not while attacked)', 'Arial', 14, BLACK)
        PygameFacade.write_text(pygame_facade, (GAMESCREEN_WIDTH + 5, 135), 'Computers have their defence in green and power in yellow', 'Arial', 14, BLACK)
        PygameFacade.write_text(pygame_facade, (GAMESCREEN_WIDTH + 5, 150), 'Defence upgrades cost 2', 'Arial', 14, BLACK)
        PygameFacade.write_text(pygame_facade, (GAMESCREEN_WIDTH + 5, 165), 'Power (money-making) upgrades cost 1', 'Arial', 14, BLACK)
        PygameFacade.write_text(pygame_facade, (GAMESCREEN_WIDTH + 5, 180), 'Power ups are applied all at once, same for defence', 'Arial', 14, BLACK)
        PygameFacade.write_text(pygame_facade, (GAMESCREEN_WIDTH + 5, 195), 'Antivirus costs skyrocket, you apply one at a time.', 'Arial', 14, BLACK)
        PygameFacade.write_text(pygame_facade, (GAMESCREEN_WIDTH + 5, 210), '', 'Arial', 14, BLACK)
        PygameFacade.write_text(pygame_facade, (GAMESCREEN_WIDTH + 5, 225), 'P.S.: You can attack the virus with anti-virus!', 'Arial', 14, BLACK)
        PygameFacade.write_text(pygame_facade, (GAMESCREEN_WIDTH + 5, 240), '', 'Arial', 14, BLACK)
        anti_info_button.draw()

    pygame_facade.update_screen()
    pygame_facade.clock.tick(FPS)
