import sys
import pygame
pygame.init()


def draw_chess_board(screen, green):
    pos_x = 25
    pos_y = 625
    last_color = green
    last_num = 0
    pygame.draw.line(screen, "Black", (97, 95), (97, 700), 5)
    pygame.draw.line(screen, "Black", (100, 97), (704, 97), 5)
    pygame.draw.line(screen, "Black", (95, 702), (702, 702), 5)
    pygame.draw.line(screen, "Black", (702, 100), (702, 702), 5)
    for count1 in range(8):
        for count2 in range(8):
            if last_color == "White":
                color = green
            else:
                color = "White"
            last_color = color
            pos_x += 75
            coordinate = (pos_x, pos_y, 75, 75)
            pygame.draw.rect(screen, color, pygame.Rect(coordinate))
            last_num += 1
            if count2 == 7:
                pos_x = 25
                pos_y -= 75
                if last_color == "White":
                    last_color = green
                else:
                    last_color = "White"


def find_figur(all_groups, clicked_position):
    x, y = clicked_position
    for group in all_groups.values():
        for figur in group:
            figur_x, figur_y = figur.rect.center
            if x in range(figur_x - 20, figur_x + 20) and y in range(figur_y - 20, figur_y + 20):
                return figur
    return None


def take_figur(all_groups, clicked_position, crosshair_group):
    clicked_figur = find_figur(all_groups, clicked_position)
    all_groups[type(clicked_figur)].remove(clicked_figur)
    name_of_figur = clicked_figur
    crosshair_group.empty()
    crosshair_group.add(clicked_figur)
    return name_of_figur, list(clicked_figur.rect.center)


def delete_figure_allowed(all_groups, clicked_position):
    # mouse_sprite = crosshair_group.sprites()[0]
    clicked_figure = find_figur(all_groups, clicked_position)
    if clicked_figure is not None:
        all_groups[type(clicked_figure)].remove(clicked_figure)


def set_figur(clicked_position, all_groups, crosshair_group):
    delete_figure_allowed(all_groups, clicked_position)
    mouse_sprite = crosshair_group.sprites()[0]
    mouse_sprite.rect.center = clicked_position
    all_groups[type(mouse_sprite)].add(mouse_sprite)
    crosshair_group.empty()
    crosshair_group.add(Crosshair())
    return True


def moved_way_is_free(all_groups, check_for_occupation):
    if check_for_occupation is None:
        return True
    for cor in check_for_occupation:
        figur = find_figur(all_groups, cor)
        if figur is not None:
            return False
    return True


def clicked_field(coordinates, clicked_position):
    mouse_pos_x, mouse_pos_y = clicked_position
    for cor in coordinates:
        x, y = cor
        if x in range(mouse_pos_x - 30, mouse_pos_x + 30) and y in range(mouse_pos_y - 30, mouse_pos_y + 30):
            return [x, y]
        else:
            continue
    return None


def possible_positions(coordinates):
    x, y = 60, 60
    for cor_1 in range(8):
        y += 75
        x = 60
        for cor_2 in range(8):
            x += 75
            coordinates.append([x, y])
    return coordinates


def call_figur_classes(coordinates, figures):
    coordinates = possible_positions(coordinates)
    figures.farmers()
    figures.runners()
    figures.horses()
    figures.towers()
    figures.kings()
    figures.queens()
    return coordinates


def step_back(taken_position, all_groups, crosshair_group):
    mouse_sprite = crosshair_group.sprites()[0]
    mouse_sprite.rect.center = taken_position
    all_groups[type(mouse_sprite)].add(mouse_sprite)
    crosshair_group.empty()
    crosshair_group.add(Crosshair())


def clean_up_list(the_ist):
    clean_list = []
    for element in the_ist:
        if element not in clean_list:
            clean_list.append(element)
    return clean_list


def get_allowed_moves(taken_figure, taken_position, coordinates, all_groups):
    allowed_pos_changes = []
    moved_way = []
    clicked_pos = clicked_field(coordinates, taken_figure.rect.center)
    taken_position = list(taken_position)
    afm = AllowedFigureMoves(taken_position.copy(), taken_figure.color, all_groups, coordinates)
    ffm_2 = MovedWay(taken_position, clicked_pos, taken_figure.color)
    if isinstance(taken_figure, Farmer):
        allowed_pos_changes = afm.far()
        moved_way = ffm_2.farmer()
    elif isinstance(taken_figure, Runner):
        allowed_pos_changes = afm.run()
        #moved_way = ffm_2.runner()
    elif isinstance(taken_figure, Horse):
        allowed_pos_changes = afm.hor()
    elif isinstance(taken_figure, Tower):
        allowed_pos_changes = afm.tow()
        moved_way = ffm_2.tower()
    elif isinstance(taken_figure, King):
        allowed_pos_changes = afm.kin()
    elif isinstance(taken_figure, Queen):
        allowed_pos_changes = afm.run() + afm.tow()
        moved_way = ffm_2.runner() + ffm_2.tower()
    if taken_position in allowed_pos_changes:
        allowed_pos_changes.remove(taken_position)
    # a_p_s = allowed_pos_changes
    # if the player tried to move oblique with the tower or straight with the runner this check returns nou a_p_s
    # if not moved_way_is_free(all_groups, moved_way):
    #     allowed_pos_changes = []
        return allowed_pos_changes
    else:
        return allowed_pos_changes


def set_figur_is_allowed(clicked_position, allowed_pos_changes):
    if clicked_position not in allowed_pos_changes:
        return False
    else:
        return True


def chess(all_groups, coordinates):
    all_allowed_moves = []
    for group in all_groups.values():
        for figure in group:
            if figure.color == "black" and isinstance(figure, Tower):
                allowed_figure_moves = get_allowed_moves(figure, figure.rect.center, coordinates, all_groups)
                # if not set_figur_is_allowed()
                for move in allowed_figure_moves:
                    all_allowed_moves.append(move)


def is_enemy_figure(color_1, color_2):
    if color_1 == color_2:
        return False
    return True


def is_in_coordinates(coordinates, allowed_cors):
    is_included = []
    for cor in allowed_cors:
        if cor in coordinates:
            is_included.append(cor)
    return is_included


class Crosshair(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/input-mouse-icon.png")
        self.rect = self.image.get_rect()
        self.current_pos = pygame.mouse.get_pos()

    def update(self):
        self.rect.center = pygame.mouse.get_pos()


class CrosshairGroup(pygame.sprite.Group):
    def update(self):
        super().update()
        mouse_sprite = self.sprites()[0]
        mouse_sprite.rect.center = pygame.mouse.get_pos()


class Farmer(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, group, current_color):
        super().__init__()
        self.farmer_image1 = pygame.image.load("images/Black Figures/farmer.black.png")
        self.farmer_image2 = pygame.image.load("images/White Figures/farmer.white.png")
        if current_color == 1:
            self.color = "black"
            farmer = self.farmer_image1
        else:
            self.color = "white"
            farmer = self.farmer_image2
        self.image = pygame.transform.scale(farmer, (70, 70))
        self.rect = self.image.get_rect()
        self.group = group
        self.rect.center = [pos_x, pos_y]
        self.image.fill("White", self.rect)


class Runner(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, group, current_runner):
        super().__init__()
        self.runner_image1 = pygame.image.load("images/Black Figures/runner.black.png")
        self.runner_image2 = pygame.image.load("images/White Figures/runner.white.png")
        if current_runner == 1:
            self.color = "black"
            runner = self.runner_image1
        else:
            self.color = "white"
            runner = self.runner_image2
        self.image = pygame.transform.scale(runner, (70, 70))
        self.rect = self.image.get_rect()
        self.group = group
        self.rect.center = [pos_x, pos_y]


class Tower(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, group, current_tower):
        super().__init__()
        self.tower_image1 = pygame.image.load("images/Black Figures/tower.black.png")
        self.tower_image2 = pygame.image.load("images/White Figures/tower.white.png")
        if current_tower == 1:
            self.color = "black"
            tower = self.tower_image1
        else:
            self.color = "white"
            tower = self.tower_image2
        self.image = pygame.transform.scale(tower, (70, 70))
        self.rect = self.image.get_rect()
        self.group = group
        self.rect.center = [pos_x, pos_y]


class Horse(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, group, current_horse):
        super().__init__()
        self.horse_image1 = pygame.image.load("images/Black Figures/horse.black.png")
        self.horse_image2 = pygame.image.load("images/White Figures/horse.white.png")
        if current_horse == 1:
            self.color = "black"
            horse = self.horse_image1
        else:
            self.color = "white"
            horse = self.horse_image2
        self.image = pygame.transform.scale(horse, (70, 70))
        self.rect = self.image.get_rect()
        self.group = group
        self.rect.center = [pos_x, pos_y]


class King(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, group, current_king):
        super().__init__()
        self.king_image1 = pygame.image.load("images/Black Figures/king.black.png")
        self.king_image2 = pygame.image.load("images/White Figures/king.white.png")
        if current_king == 1:
            self.color = "black"
            king = self.king_image1
        else:
            self.color = "white"
            king = self.king_image2
        self.image = pygame.transform.scale(king, (70, 70))
        self.rect = self.image.get_rect()
        self.group = group
        self.rect.center = [pos_x, pos_y]


class Queen(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, group, current_queen):
        super().__init__()
        self.queen_image1 = pygame.image.load("images/Black Figures/queen.black.png")
        self.queen_image2 = pygame.image.load("images/White Figures/queen.white.png")
        if current_queen == 1:
            self.color = "black"
            queen = self.queen_image1
        else:
            self.color = "white"
            queen = self.queen_image2
        self.image = pygame.transform.scale(queen, (70, 70))
        self.rect = self.image.get_rect()
        self.group = group
        self.rect.center = [pos_x, pos_y]


class Figures:

    def __init__(self, all_groups):
        super().__init__()
        self.all_groups = all_groups
        self.farmer_group = self.all_groups[Farmer]
        self.runner_group = self.all_groups[Runner]
        self.horse_group = self.all_groups[Horse]
        self.tower_group = self.all_groups[Tower]
        self.king_group = self.all_groups[King]
        self.queen_group = self.all_groups[Queen]

    def farmers(self):
        pos_x = 135
        pos_y = 585
        current_color = 1
        count = 0
        for farmer in range(16):
            if count == 8:
                current_color = 2
                pos_x = 135
                pos_y = 210
            new_farmer = Farmer(pos_x, pos_y, self.farmer_group, current_color)
            self.farmer_group.add(new_farmer)
            pos_x += 75
            count += 1

    def runners(self):
        pos_x = 285
        pos_y = 660
        current_runner = 1
        count = 0
        for runner_2 in range(4):
            if count == 2:
                current_runner = 2
                pos_y = 135
                pos_x = 285
            new_runner = Runner(pos_x, pos_y, self.runner_group, current_runner)
            self.runner_group.add(new_runner)
            pos_x += 225
            count += 1

    def horses(self):
        pos_x = 210
        pos_y = 660
        current_horse = 1
        count = 0
        for horse_2 in range(4):
            if count == 2:
                current_horse = 2
                pos_y = 135
                pos_x = 210
            new_horse = Horse(pos_x, pos_y, self.horse_group, current_horse)
            self.horse_group.add(new_horse)
            pos_x += 375
            count += 1

    def towers(self):
        pos_x = 135
        pos_y = 660
        current_tower = 1
        count = 0
        for tower_2 in range(4):
            if count == 2:
                current_tower = 2
                pos_y = 135
                pos_x = 135
            new_tower = Tower(pos_x, pos_y, self.horse_group, current_tower)
            self.tower_group.add(new_tower)
            pos_x += 525
            count += 1

    def kings(self):
        pos_x = 435
        pos_y = 660
        current_king = 1
        count = 0
        for king_2 in range(2):
            if count == 1:
                current_king = 2
                pos_y = 135
                pos_x = 435
            new_king = King(pos_x, pos_y, self.king_group, current_king)
            self.king_group.add(new_king)
            pos_x += 75
            count += 1

    def queens(self):
        pos_x = 360
        pos_y = 660
        current_queen = 1
        count = 0
        for queen_2 in range(2):
            if count == 1:
                current_queen = 2
                pos_y = 135
                pos_x = 360
            new_queen = Queen(pos_x, pos_y, self.queen_group, current_queen)
            self.queen_group.add(new_queen)
            pos_x += 75
            count += 1


class AllowedFigureMoves:
    def __init__(self, cor, figur_color, all_groups, coordinates):
        self.cor = cor
        self.figur_color = figur_color
        self.all_groups = all_groups
        self.coordinates = coordinates
        self.all_groups = all_groups

    def far(self):
        allowed_cors = []
        if self.cor is not None:
            x, y = self.cor
            if y == 210 or y == 585:
                len_range = 2
            else:
                len_range = 1
            if self.figur_color == "white":
                direction = 1
            else:
                direction = -1
            right = find_figur(self.all_groups, [x + 75, y + 75 * direction])
            if right is not None and is_enemy_figure(self.figur_color, right.color):
                allowed_cors.append([x + 75, y + 75 * direction])
            left = find_figur(self.all_groups, [x - 75, y + 75 * direction])
            if left is not None and is_enemy_figure(self.figur_color, left.color):
                allowed_cors.append([x - 75, y + 75 * direction])
            for cor in range(len_range):
                y += 75 * direction
                allowed_cor = [x, y]
                forward = find_figur(self.all_groups, allowed_cor)
                if forward is None:
                    allowed_cors.append(allowed_cor)
            allowed_cors = is_in_coordinates(self.coordinates, allowed_cors.copy())
            allowed_cors = clean_up_list(allowed_cors)
            if len(allowed_cors) > 1:
                result = []
                mw = MovedWay(self.cor, allowed_cors[1], self.figur_color)
                moved_way = mw.farmer()
                if not moved_way_is_free(self.all_groups, moved_way):
                    result.append(allowed_cors[1])
                    return result
            return allowed_cors

    def run(self):
        allowed_cors = []
        count = 0
        if self.cor is not None:
            x, y = self.cor
            for n in range(28):
                count += 1
                if count == 8 or count == 15 or count == 22:
                    x, y = self.cor
                if n in range(0, 7):
                    x += 75
                    y += 75
                if n in range(7, 14):
                    x -= 75
                    y -= 75
                if n in range(14, 21):
                    x += 75
                    y -= 75
                if n in range(21, 28):
                    x -= 75
                    y += 75
                allowed_cor = [x, y]
                clicked_position = find_figur(self.all_groups, allowed_cor)
                if clicked_position is None:
                    allowed_cors.append(allowed_cor)
                else:
                    if is_enemy_figure(self.figur_color, clicked_position.color):
                        allowed_cors.append(allowed_cor)
            allowed_cors = is_in_coordinates(self.coordinates, allowed_cors.copy())
            allowed_cors = clean_up_list(allowed_cors)
            if self.cor in allowed_cors:
                allowed_cors.remove(self.cor)
            result = []
            for pos in allowed_cors:
                mw = MovedWay(self.cor, pos, self.figur_color)
                moved_way = mw.runner()
                print(moved_way)
            return []
            #     if moved_way is not None and moved_way_is_free(self.all_groups, moved_way):
            #         result.append(cor)
            #         print(result)
            #         return result
            #     else:
            #         break
            # print(allowed_cors)
            # return allowed_cors

    def hor(self):
        possible_allowed_cors = []
        allowed_cors = []
        count = 0
        for n in range(28):
            x, y = self.cor
            count += 1
            if count == 1:
                x -= 75
                y -= 150
            if count == 2:
                x += 75
                y -= 150
            if count == 3:
                x += 150
                y += 75
            if count == 4:
                x += 150
                y -= 75
            if count == 5:
                x -= 150
                y += 75
            if count == 6:
                x -= 150
                y -= 75
            if count == 7:
                x += 75
                y += 150
            if count == 8:
                x -= 75
                y += 150
            allowed_cor = [x, y]
            possible_allowed_cors.append(allowed_cor)
        possible_allowed_cors = is_in_coordinates(self.coordinates, possible_allowed_cors.copy())
        possible_allowed_cors = clean_up_list(possible_allowed_cors)
        for cor in possible_allowed_cors.copy():
            clicked_figure = find_figur(self.all_groups, cor)
            if clicked_figure is None:
                allowed_cors.append(cor)
            elif is_enemy_figure(self.figur_color, clicked_figure.color):
                allowed_cors.append(cor)
        allowed_cors.remove(self.cor)
        return allowed_cors

    def tow(self):
        possible_allowed_cors = []
        allowed_cors = []
        x, y = self.cor
        count = 0
        if self.cor is not None:
            for n in range(28):
                count += 1
                if count == 8 or count == 15 or count == 22:
                    x, y = self.cor
                if n in range(0, 7):
                    y += 75
                if n in range(7, 14):
                    y -= 75
                if n in range(14, 21):
                    x += 75
                if n in range(21, 28):
                    x -= 75
                allowed_cor = [x, y]
                possible_allowed_cors.append(allowed_cor)
            possible_allowed_cors = is_in_coordinates(self.coordinates, possible_allowed_cors.copy())
            possible_allowed_cors = clean_up_list(possible_allowed_cors)
            for cor in possible_allowed_cors.copy():
                clicked_figure = find_figur(self.all_groups, cor)
                if clicked_figure is None:
                    allowed_cors.append(cor)
                elif is_enemy_figure(self.figur_color, clicked_figure.color):
                    allowed_cors.append(cor)
            return allowed_cors

    def kin(self):
        x, y = self.cor
        allowed_cors = []
        possible_allowed_cors = [[x, y - 75], [x - 75, y], [x + 75, y], [x, y + 75], [x - 75, y - 75], [x + 75, y - 75],
                                 [x - 75, y + 75], [x + 75, y + 75]]
        possible_allowed_cors = is_in_coordinates(self.coordinates, possible_allowed_cors.copy())
        possible_allowed_cors = clean_up_list(possible_allowed_cors)
        for cor in possible_allowed_cors.copy():
            clicked_figure = find_figur(self.all_groups, cor)
            if clicked_figure is None:
                allowed_cors.append(cor)
            elif is_enemy_figure(self.figur_color, clicked_figure.color):
                allowed_cors.append(cor)
        return allowed_cors


class MovedWay:
    def __init__(self, start_cor, goal_cor, figure_color):
        self.goal_cor = goal_cor
        self.start_cor = start_cor
        self.color = figure_color

    def farmer(self):
        if self.color == "white" and self.goal_cor[1] == self.start_cor[1] + 150:
            return [[self.start_cor[0], self.start_cor[1] + 75]]
        elif self.color == "black" and self.goal_cor[1] == self.start_cor[1] - 150:
            return [[self.start_cor[0], self.start_cor[1] - 75]]

    def tower(self):
        moved_way = []
        # right
        if self.start_cor[0] < self.goal_cor[0]:
            for i in range(6):
                self.start_cor[0] += 75
                moved_way.append([self.start_cor[0], self.start_cor[1]])
                if self.start_cor[0] == self.goal_cor[0] - 75:
                    return moved_way
        # down
        elif self.start_cor[1] < self.goal_cor[1]:
            for i in range(6):
                self.start_cor[1] += 75
                moved_way.append([self.start_cor[0], self.start_cor[1]])
                if self.start_cor[1] == self.goal_cor[1] - 75:
                    return moved_way
        # left
        elif self.start_cor[0] > self.goal_cor[0]:
            for i in range(6):
                self.start_cor[0] -= 75
                moved_way.append([self.start_cor[0], self.start_cor[1]])
                if self.start_cor[0] == self.goal_cor[0] + 75:
                    return moved_way
        # up
        elif self.start_cor[1] > self.goal_cor[1]:
            for i in range(6):
                self.start_cor[1] -= 75
                moved_way.append([self.start_cor[0], self.start_cor[1]])
                if self.start_cor[1] == self.goal_cor[1] + 75:
                    return moved_way
        # Todo: here is the mistake, if no of these options is returning something we have to return something that
        # Todo: gives us a sign that allowed_pos_changes has to be nothing
        return []

    def runner(self):
        moved_way = []
        # moved only one field
        if self.start_cor[0] - 75 == self.goal_cor[0] and self.start_cor[1] + 75 == self.goal_cor[1] or\
                self.start_cor[0] + 75 == self.goal_cor[0] and self.start_cor[1] + 75 == self.goal_cor[1] or\
                self.start_cor[0] - 75 == self.goal_cor[0] and self.start_cor[1] - 75 == self.goal_cor[1] or \
                self.start_cor[0] + 75 == self.goal_cor[0] and self.start_cor[1] - 75 == self.goal_cor[1]:
            return []
        # moved down right
        if self.start_cor[0] < self.goal_cor[0] and self.start_cor[1] < self.goal_cor[1]:
            for i in range(6):
                self.start_cor[0] += 75
                self.start_cor[1] += 75
                moved_way.append([self.start_cor[0], self.start_cor[1]])
                if self.start_cor[0] == self.goal_cor[0]-75 and self.start_cor[1] == self.goal_cor[1]-75:
                    return moved_way
        # moved up right
        elif self.start_cor[0] < self.goal_cor[0] and self.start_cor[1] > self.goal_cor[1]:
            for i in range(6):
                self.start_cor[0] += 75
                self.start_cor[1] -= 75
                moved_way.append([self.start_cor[0], self.start_cor[1]])
                if self.start_cor[0] == self.goal_cor[0]-75 and self.start_cor[1] == self.goal_cor[1]+75:
                    return moved_way
        # moved up left
        elif self.start_cor[0] > self.goal_cor[0] and self.start_cor[1] > self.goal_cor[1]:
            for i in range(6):
                self.start_cor[0] -= 75
                self.start_cor[1] -= 75
                moved_way.append([self.start_cor[0], self.start_cor[1]])
                if self.start_cor[0] == self.goal_cor[0]+75 and self.start_cor[1] == self.goal_cor[1]+75:
                    return moved_way
        # moved down left
        elif self.start_cor[0] > self.goal_cor[0] and self.start_cor[1] < self.goal_cor[1]:
            for i in range(6):
                self.start_cor[0] -= 75
                self.start_cor[1] += 75
                moved_way.append([self.start_cor[0], self.start_cor[1]])
                if self.start_cor[0] == self.goal_cor[0]+75 and self.start_cor[1] == self.goal_cor[1]-75:
                    return moved_way
        return "apfel"


def main():
    # create a screen
    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()

    # Create crosshair group
    crosshair = Crosshair()
    crosshair_group = CrosshairGroup()
    crosshair_group.add(crosshair)
    pygame.mouse.set_visible(False)

    # button to step back
    button = pygame.image.load("images/Other Icons/Chess-Button.png")
    button_rect = button.get_rect()
    button_rect.center = [50, 50]

    # create farmers
    farmer_group = pygame.sprite.Group()

    # create runners
    runner_group = pygame.sprite.Group()

    # create horses
    horse_group = pygame.sprite.Group()

    # create towers
    tower_group = pygame.sprite.Group()

    # create kings
    king_group = pygame.sprite.Group()

    # create queens
    queen_group = pygame.sprite.Group()

    # place all figures on the start positions
    all_groups = {
        Farmer: farmer_group,
        Runner: runner_group,
        Horse: horse_group,
        Tower: tower_group,
        King: king_group,
        Queen: queen_group
    }
    figures = Figures(all_groups)

    # coordinates including all possible position were a figur can be placed
    coordinates = []

    # colors
    green = (25, 144, 0)

    # some start conditions
    running = True
    taken_position = None
    taken_figure = None
    phase = "take"

    # place all figures on the start positions
    coordinates = call_figur_classes(coordinates, figures)

    while running:
        screen.fill("White")
        clicked_position = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            step_back_gets_pressed = button_rect.collidepoint(clicked_position)
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked_position = clicked_field(coordinates, clicked_position)
                if step_back_gets_pressed:
                    if taken_figure is None:
                        continue
                    step_back(taken_position.copy(), all_groups, crosshair_group)
                    phase = "take"
                    continue

                if clicked_position is None:
                    continue

                if phase == "take":
                    taken_figure = find_figur(all_groups, clicked_position)
                    if taken_figure is not None:
                        kind_of_figure, taken_position = take_figur(all_groups, clicked_position, crosshair_group)
                        phase = "set"
                # set phase
                else:
                    allowed_pos_changes = get_allowed_moves(taken_figure, taken_position, coordinates, all_groups)
                    if not set_figur_is_allowed(clicked_position, allowed_pos_changes):
                        continue

                    if set_figur(clicked_position, all_groups, crosshair_group):
                        chess(all_groups, coordinates)
                        phase = "take"
                    taken_figure = None

        screen.blit(button, button_rect)
        draw_chess_board(screen, green)
        # draw and update crosshair
        crosshair_group.draw(screen)
        crosshair_group.update()

        # farmers
        farmer_group.draw(screen)
        farmer_group.update()

        # runners
        runner_group.draw(screen)
        runner_group.update()

        # horses
        horse_group.draw(screen)
        horse_group.update()

        # towers
        tower_group.draw(screen)
        tower_group.update()

        # kings
        king_group.draw(screen)
        king_group.update()

        # queens
        queen_group.draw(screen)
        queen_group.update()

        pygame.display.update()
        clock.tick(60)


main()
# [135, 510], [360, 585], [435, 510], [510, 435], [585, 360], [660, 285]
