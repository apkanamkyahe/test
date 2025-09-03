import arcade
print(arcade.__version__)

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Robot Science Game"
PLAYER_SPEED = 5
GRAVITY = 1
JUMP_SPEED = 20

class RobotGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.SKY_BLUE)

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.platform_list = arcade.SpriteList()
        self.collectibles = arcade.SpriteList()
        self.goal_list = arcade.SpriteList()

        # Player
        self.player_sprite = arcade.Sprite(center_x=100, center_y=150)
        self.player_sprite.texture = arcade.make_soft_square_texture(40, arcade.color.RED, outer_alpha=255)
        self.player_list.append(self.player_sprite)

        # Physics engine
        self.physics_engine = None

        # Camera
        self.camera = arcade.Camera2D()

    def setup(self):
        tile_width = arcade.Sprite("floor_image.png", scale=0.1).width  # replace with your image width in pixels
        num_tiles = int(SCREEN_WIDTH // tile_width + 1)
        # fill the whole screen

        for i in range(num_tiles):
            floor = arcade.Sprite("floor_image.png", scale=0.1, hit_box_algorithm="Detailed" )
            floor.left = i * tile_width
            floor.bottom = 0
            self.platform_list.append(floor)

        # Floor using your own image



        # Platforms (still using solid colors)
        p1 = arcade.SpriteSolidColor(200, 20, arcade.color.BROWN)
        p1.center_x = 300
        p1.center_y = 150
        self.platform_list.append(p1)

        p2 = arcade.SpriteSolidColor(150, 20, arcade.color.BROWN)
        p2.center_x = 600
        p2.center_y = 250
        self.platform_list.append(p2)

        # Collectible
        crystal = arcade.SpriteSolidColor(20, 20, arcade.color.BLUE)
        crystal.center_x = 600
        crystal.center_y = 280
        self.collectibles.append(crystal)

        # Goal flag
        goal_flag = arcade.SpriteSolidColor(20, 40, arcade.color.RED)
        goal_flag.center_x = 700
        goal_flag.center_y = 400
        self.goal_list.append(goal_flag)

        # Physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, self.platform_list, gravity_constant=GRAVITY
        )

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.platform_list.draw()
        self.player_list.draw()
        self.collectibles.draw()
        self.goal_list.draw()

    def on_update(self, delta_time):
        self.physics_engine.update()

        # Collectibles
        hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.collectibles)
        for item in hit_list:
            item.remove_from_sprite_lists()

        # Goal
        hit_goal = arcade.check_for_collision_with_list(self.player_sprite, self.goal_list)
        for goal in hit_goal:
            print("You reached the goal!")
            goal.remove_from_sprite_lists()

        # Smooth camera
        screen_center_x = self.player_sprite.center_x
        screen_center_y = self.player_sprite.center_y
        self.camera.position = (screen_center_x, screen_center_y)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_SPEED
        elif key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = JUMP_SPEED

    def on_key_release(self, key, modifiers):
        if key in (arcade.key.LEFT, arcade.key.RIGHT):
            self.player_sprite.change_x = 0

# Run the game
game = RobotGame()
game.setup()
arcade.run()
