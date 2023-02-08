import pygame, sys, random 

pygame.init()
screen = pygame.display.set_mode((450,600))
window = pygame.Surface((150,200))

tile = pygame.image.load('tile.png')
frame_1 = pygame.image.load('standing_1.png')
frame_2 = pygame.image.load('standing_2.png')
frame_3 = pygame.image.load('standing_3.png')
frame_4 = pygame.image.load('standing_4.png')
character = [frame_1, frame_2, frame_3, frame_4]
bg_img = pygame.image.load('background.png')
clock = pygame.time.Clock()
map_rect = []

# main menu, score, sounds effects, death when down

level = [[0,0,0,0,0,1,0,1,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,1,1,1,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],                      
        [0,0,1,0,0,0,0,0,0,0],
        [0,0,0,0,1,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,1,0,0,0,0],
        [0,0,0,0,0,0,0,1,0,0],
        [0,0,0,0,0,0,0,0,0,0],
        [1,1,1,0,1,0,1,1,1,1]]

def collision_test(rect, tiles):
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(player, tiles):
    player.rect.x += player.movement[0]
    hit_list = collision_test(player.rect, tiles)
    for tile in hit_list:
        if player.movement[0] > 0:
            player.rect.right = tile.left
        if player.movement[0] < 0:
            player.rect.left = tile.right
    player.rect.y += player.movement[1]
    hit_list = collision_test(player.rect, tiles)
    for tile in hit_list:
        if player.movement[1] > 0:
            player.rect.bottom = tile.top  
            player.momentum = 0
            player.can_jump = 2
        if player.movement[1] < 0:
            player.rect.top = tile.bottom         

    return player  

class Main_menu:
    def __init__(self):
        self.font = pygame.font.Font('freesansbold.ttf', 30)
        self.text = self.font.render("press s button to play", True, (255,255,255))
        self.rect = self.text.get_rect()
        self.rect.centerx = 225
        self.rect.y = 10
        self.animation = 0
        self.font_2 = pygame.font.Font('freesansbold.ttf', 30)
        self.text_2 = self.font_2.render('highest score', True, (0,0,255))
        self.rect_2 = self.text_2.get_rect()
        self.rect_2.centerx = 225
        self.rect_2.centery = 150
        self.score_file = open('score.txt', 'r')
        self.high_score = self.score_file.read()
        self.high_score_display = self.font_2.render(self.high_score, True, (0,0,255))
        self.high_score_rect  = self.high_score_display.get_rect()
        self.high_score_rect.top = self.rect_2.bottom
        self.high_score_rect.centerx = 225


    def draw(self): 
        self.animation += 1
        if self.animation <= 45:
            screen.blit(self.text, self.rect)
        if self.animation >= 60:
            self.animation = 0  

        screen.blit(self.text_2, self.rect_2)   
        screen.blit(self.high_score_display, self.high_score_rect)      

class Player:
    def __init__(self):
        self.image = character[0]
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.movement = [0,0]
        self.right = False
        self.left = False 
        self.jump = False 
        self.momentum = 0
        self.animation = 0
        self.direction = "right"
        self.can_jump = 2 
        self.jump_sound = pygame.mixer.Sound('jump_sound.wav')


    def update(self):
        self.momentum += 0.2
        if self.momentum >= 4:
            self.momentum = 4
        if self.jump:
            self.jump_sound.play()
            self.can_jump -= 1 
            self.momentum = -4
            self.jump = False 
        self.movement = [0,0]
        self.movement[1] = self.momentum
        if self.right:
            self.movement[0] = 2
            self.direction = "right"
        if self.left:
            self.movement[0] = -2
            self.direction = "left"

        # animate the player -------------------
        self.animation += 1
        if self.animation >= 60:
            self.animation = 0
        self.value = int(self.animation/15) 
        self.image = character[self.value]
        
        if self.direction == "left":
            self.image = pygame.transform.flip(self.image, True, False)

        self.image.set_colorkey((0,0,0))    
            
    def draw(self, scroll):
        window.blit(self.image, (self.rect.x, self.rect.y+scroll))    

class Score:
    def __init__(self):
        self.score = 0
        self.update_counter = 0

    def update(self):
        self.update_counter += 1
        if self.update_counter == 60:
            self.score += 1
            self.update_counter = 0

    def draw(self): 
        font = pygame.font.Font('freesansbold.ttf', 50)
        text = font.render(str(self.score), True, (0,0,0))
        screen.blit(text, (0,0))  

def initiate_game():
    scroll = 0
    scroll_velocity = 0.5
    player_scroll = 0
    scroll_counter = 0
    diffculty = 0
    stop = False 
    player = Player()
    score = Score()
    game_state = False
    main_menu = Main_menu()

def main():
    pygame.mixer.music.load("zero.mp3")
    pygame.mixer.music.play()
    scroll = 0
    scroll_velocity = 0.5
    player_scroll = 0
    scroll_counter = 0
    diffculty = 0
    stop = False 
    player = Player()
    score = Score()
    main_menu = Main_menu()
    game_state = False
    fps = 60

    while True:         
        window.fill((0,0,0))      

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    player.right = True
                if event.key == pygame.K_LEFT:
                    player.left = True 
                if event.key == pygame.K_UP:
                    if player.can_jump > 0:
                        player.jump = True
                if event.key == pygame.K_s:
                    if not game_state:
                        game_state = True 
                        scroll = 0
                        scroll_velocity = 0.5
                        player_scroll = 0
                        scroll_counter = 0
                        diffculty = 0
                        stop = False 
                        player = Player()
                        score = Score()
                        main_menu = Main_menu()
                        fps = 60
                                   
                if event.key == pygame.K_q:
                    game_state = False        

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    player.right = False
                if event.key == pygame.K_LEFT:
                    player.left = False 

        # game objects and draw bg ----------------------------------------------------------------
        
        scroll += scroll_velocity
        tiles_rect = []  

        # game screen while game is inactive (menus) -----------------------------------------------
        if not game_state:
            screen.blit(pygame.transform.scale(window, (450,600)), (0,0))           
            main_menu.draw()

        # game screen while active ------------------------------------------------------------------
        if game_state:
            window.blit(bg_img, (0,0))

            # draw the level and gets its rect --------------------------------------------------------
            y = 0
            for row in level:
                x = 0
                for cel in row:
                    if cel == 1:
                        window.blit(tile, (16*x, 16*y+scroll))  
                        tiles_rect.append(pygame.Rect(x*16, y*16, 16, 16))  
                    x += 1       
                y += 1  

            player = move(player, tiles_rect)    
            player.update()
            player.draw(scroll) 

            # stop the player from moving out of the screen on the X axes -----------------------------------------
            if player.rect.x < 0:
                player.rect.x = 0
            if player.rect.x >= (150 - 16):
                player.rect.x = 150 - 16
            if player.rect.y >= 200:
                pass

            # stop the player from moving out of the screen, kill him if he falls ---------
            if player.rect.x >= 134:
                player.rect.x = 134
            if player.rect.x < 0:
                player.rect.x = 0
            if player.rect.y >= 200:
                game_state = False    
                file = open("score.txt", "r")   
                high_score = int(file.read())
                if score.score > high_score:
                    file.close()
                    file = open('score.txt', 'w')
                    new_score = str(score.score)
                    file.write(new_score)
                    file.close()
                    main_menu = Main_menu()

            # add new randomly generated rows at the top of the level ---------------------------------------------
            if scroll >= 32 :          
                new_row = [0,0,0,0,0,0,0,0,0,0] 
                level.insert(0, new_row)
                new_row = []
                for i in range(0,10):
                    value = random.randint(0, 6)
                    if value == 0:
                        new_row.append(1)
                    else:
                        new_row.append(0)
                level.insert(0, new_row) 
                scroll = 0
                player.rect.y += 32

            # optimise the level, get rid of rows we dont need ------------------------------------------------
            if len(level) > 14:
                level.pop(-1)

            # update window, draw it on screen, display score -------------------------------------------------        
            screen.blit(pygame.transform.scale(window, (450,600)), (0,0))
            score.update()
            score.draw()

            # adjust the games diffuculty, the longer you play the harder it gets -----------------------------
            diffculty += 1
            if diffculty >= 300:
                fps += 1       
                diffculty = 0  
                print(fps)    

        # update the screen and lock the game at 60fps --------------------------------------------------------
        pygame.display.update()
        clock.tick(fps)

main()






