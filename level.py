import pygame
from support import import_csv_layout, import_cut_graphic
from settings import tile_size, screen_height, screen_width
from tiles import Tile, StaticTile, Crate, Coin, Tree2, Tree3, AnimatedTile, Stomp, Sign, Mushroom, Mushroom2, Rock, Small_bush
from enemy import Enemy
from decoration import Sky, Water, Clouds
from player import Player
from particles import ParticleEffect
from game_data import levels

class Level:
    def __init__(self, current_level, surface, create_overworld, change_coins, change_health):
        #setup
        self.display_surface = surface
        self.world_shift = 0
        self.current_x = None

        #overworld connection
        self.create_overworld = create_overworld
        self.current_level = current_level
        level_data = levels[self.current_level]
        self.new_max_level = level_data["unlock"]
        #level_content = level_data["content"]
        #level_display
        #self.font = pygame.font.Font(None, 40)
        #self.text_surf = self.font.render(level_content, True, "white")
        #self.text_rect = self.text_surf.get_rect(center=(screen_width/2, screen_height / 2))

        #player
        player_layout = import_csv_layout(level_data["player"])
        self.player = pygame.sprite.GroupSingle()
        self.goal = pygame.sprite.GroupSingle()
        self.player_setup(player_layout, change_health)
        #ui
        self.change_coins = change_coins
        #kurz
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False
        #wybuch
        self.explosion_sprites = pygame.sprite.Group()
        #terrain setup
        terrain_layout = import_csv_layout(level_data["terrain"])
        self.terrain_sprites = self.create_tile_group(terrain_layout, "terrain")
        #trawa
        grass_layout = import_csv_layout(level_data["grass"])
        self.grass_sprites = self.create_tile_group(grass_layout, "grass")
        #skrzynki
        crates_layout = import_csv_layout(level_data["crates"])
        self.crates_sprites = self.create_tile_group(crates_layout, "crates")
        #kamien
        rock_layout = import_csv_layout(level_data["bg rock"])
        self.rock_sprites = self.create_tile_group(rock_layout, "bg rock")
        #monety
        coin_layout = import_csv_layout(level_data["coins"])
        self.coins_sprites = self.create_tile_group(coin_layout, "coins")
        #znaki
        sign_layout = import_csv_layout(level_data["bg sign"])
        self.sign_sprites = self.create_tile_group(sign_layout, "bg sign")
        #grzyby
        mushroom_layout = import_csv_layout(level_data["bg mushrooms"])
        self.mushroom_sprites = self.create_tile_group(mushroom_layout, "bg mushrooms")
        #grzyby2
        mushroom2_layout = import_csv_layout(level_data["bg mushrooms2"])
        self.mushroom2_sprites = self.create_tile_group(mushroom2_layout, "bg mushrooms2")
        #pniaki
        bg_stomps_layout = import_csv_layout(level_data["bg stomps"])
        self.bg_stomps_sprites = self.create_tile_group(bg_stomps_layout, "bg stomps")
        #small_bushes
        bg_bushes_layout = import_csv_layout(level_data["bg bushes"])
        self.bg_bushes_sprites = self.create_tile_group(bg_bushes_layout, "bg bushes")
        #bg drzewa1
        bg_trees_layout = import_csv_layout(level_data["bg trees"])
        self.bg_trees_sprites = self.create_tile_group(bg_trees_layout, "bg trees")
        #bg drzewa2
        bg_trees_layout2 = import_csv_layout(level_data["bg trees2"])
        self.bg_trees2_sprites = self.create_tile_group(bg_trees_layout2, "bg trees2")
        #przeciwnicy
        enemy_layout = import_csv_layout(level_data["enemies"])
        self.enemies_sprites = self.create_tile_group(enemy_layout, "enemies")
        #ogranicznik
        constraint_layout = import_csv_layout(level_data["constraints"])
        self.constraint_sprites = self.create_tile_group(constraint_layout, "constraints")
        #decoration
        self.sky = Sky(8)
        level_width = len(terrain_layout[0]) * tile_size
        self.water = Water(screen_height - 30, 1.3 * level_width)
        self.clouds = Clouds(400, level_width, 30)

    def create_tile_group(self, layout, type):
        sprite_group = pygame.sprite.Group()

        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                if val != "-1":
                    x = col_index * tile_size
                    y = row_index * tile_size
                    if type == "terrain":
                        terrain_tile_list = import_cut_graphic("./graphics/Tiles/123456789101112131415161718192021.png")
                        tile_surface = terrain_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == "grass":
                        grass_tile_list = import_cut_graphic("./graphics/Object/grass.png")
                        tile_surface = grass_tile_list[int(val)]
                        sprite = StaticTile(tile_size, x, y, tile_surface)

                    if type == "crates":
                        sprite = Crate(tile_size, x, y)

                    if type == "bg trees":
                        sprite = Tree2(tile_size, x, y)

                    if type == "bg trees2":
                        sprite = Tree3(tile_size, x, y)

                    if type == "bg stomps":
                        sprite = Stomp(tile_size, x, y)

                    if type == "bg sign":
                        sprite = Sign(tile_size, x, y)

                    if type == "bg mushrooms":
                        sprite = Mushroom(tile_size, x, y)

                    if type == "bg mushrooms2":
                        sprite = Mushroom2(tile_size, x, y)

                    if type == "bg bushes":
                        sprite = Small_bush(tile_size, x, y)

                    if type == "bg rock":
                        sprite = Rock(tile_size, x, y)

                    if type == "coins":
                        if val == "0":
                            sprite = Coin(tile_size, x, y,"./graphics/coins/gold", 5)
                        if val == "1":
                            sprite = Coin(tile_size, x, y, "./graphics/coins/silver", 1)

                    if type == "enemies":
                        sprite = Enemy(tile_size, x, y)

                    if type == "constraints":
                        sprite = Tile(tile_size, x, y)
                        sprite.image.set_alpha(0)

                    sprite_group.add(sprite)

        return sprite_group

    def player_setup(self, layout, change_health):
        for row_index, row in enumerate(layout):
            for col_index, val in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if val == "0":
                    sprite = Player((x, y), self.display_surface, self.create_jump_particles, change_health)
                    self.player.add(sprite)
                if val == "1":
                    koncowy_znak = pygame.image.load("./graphics/Object/Sign_CV.png").convert_alpha()
                    sprite = StaticTile(tile_size, x, y, koncowy_znak)
                    self.goal.add(sprite)

    def enemy_collision_reverse(self):
        for enemy in self.enemies_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.constraint_sprites, False):
                enemy.reverse()

    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, 5)
        else:
            pos += pygame.math.Vector2(10, -5)
        jump_particle_sprite = ParticleEffect(pos, "jump")
        self.dust_sprite.add(jump_particle_sprite)

    def poziome_zderzenia(self):
        player = self.player.sprite
        # jesli nie ma kolizji to dodac update, inaczej spokoj
        player.collision_rect.x += player.direction.x * player.speed
        dotyk = self.terrain_sprites.sprites() + self.crates_sprites.sprites()
        for sprite in dotyk:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.x < 0:
                    player.collision_rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.collision_rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def pionowe_zderzenia(self):
        player = self.player.sprite
        player.dodaj_grawitacje()
        dotyk = self.terrain_sprites.sprites() + self.crates_sprites.sprites()

        for sprite in dotyk:
            if sprite.rect.colliderect(player.collision_rect):
                if player.direction.y > 0:
                    player.collision_rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.collision_rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False

    def scroll_x(self):
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width / 2.5 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - (screen_width / 2.5) and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8

    def get_player_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, "land")
            self.dust_sprite.add(fall_dust_particle)

    def check_death(self):
        if self.player.sprite.rect.top > screen_height:
            self.create_overworld(self.current_level, 0)

    def check_win(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.goal, False):
            self.create_overworld(self.current_level, self.new_max_level)

    def check_coin_collision(self):
        collided_coins = pygame.sprite.spritecollide(self.player.sprite, self.coins_sprites, True)
        if collided_coins:
            for coin in collided_coins:
                self.change_coins(coin.value)

    def check_enemy_collisions(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemies_sprites, False)
        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.player.sprite.direction.y = -8
                    explosion_sprite = ParticleEffect(enemy.rect.center, "explosion")
                    self.explosion_sprites.add(explosion_sprite)
                    enemy.kill()
                else:
                    self.player.sprite.get_damage()

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            self.create_overworld(self.current_level, self.new_max_level)
        if keys[pygame.K_ESCAPE]:
            self.create_overworld(self.current_level, 0)

    def run(self):
        self.input()
        #self.display_surface.blit(self.text_surf, self.text_rect)
        # decoration
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)
        #kurz
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)
        #poziom
        self.terrain_sprites.update(self.world_shift)
        self.terrain_sprites.draw(self.display_surface)
        #skrzynka
        self.crates_sprites.update(self.world_shift)
        self.crates_sprites.draw(self.display_surface)
        # pniak
        self.bg_stomps_sprites.update(self.world_shift)
        self.bg_stomps_sprites.draw(self.display_surface)
        # trawa
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)
        #bg_drzewa
        self.bg_trees_sprites.update(self.world_shift)
        self.bg_trees_sprites.draw(self.display_surface)
        # bg_drzewa2
        self.bg_trees2_sprites.update(self.world_shift)
        self.bg_trees2_sprites.draw(self.display_surface)
        #znaki
        self.sign_sprites.update(self.world_shift)
        self.sign_sprites.draw(self.display_surface)
        #grzyby
        self.mushroom_sprites.update(self.world_shift)
        self.mushroom_sprites.draw(self.display_surface)
        #grzyby2
        self.mushroom2_sprites.update(self.world_shift)
        self.mushroom2_sprites.draw(self.display_surface)
        #kamienie
        self.rock_sprites.update(self.world_shift)
        self.rock_sprites.draw(self.display_surface)
        #kamienie
        self.bg_bushes_sprites.update(self.world_shift)
        self.bg_bushes_sprites.draw(self.display_surface)
        #przeciwnicy
        self.enemies_sprites.update(self.world_shift)
        #self.constraint_sprites.update(self.world_shift)
        self.enemy_collision_reverse()
        self.enemies_sprites.draw(self.display_surface)
        self.explosion_sprites.update(self.world_shift)
        self.explosion_sprites.draw(self.display_surface)
        #ograniczenia
        self.constraint_sprites.update(self.world_shift)
        self.constraint_sprites.draw(self.display_surface)
        #monety
        self.coins_sprites.update(self.world_shift)
        self.coins_sprites.draw(self.display_surface)
        #Interakcja gracza
        self.player.update()
        self.pionowe_zderzenia()
        self.get_player_on_ground()
        self.poziome_zderzenia()
        self.create_landing_dust()

        self.scroll_x()
        self.player.draw(self.display_surface)
        self.goal.update(self.world_shift)
        self.goal.draw(self.display_surface)

        self.check_death()
        self.check_win()
        self.check_coin_collision()
        self.check_enemy_collisions()
        #water
        self.water.draw(self.display_surface, self.world_shift)
