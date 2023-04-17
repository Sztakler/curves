import pygame
import thorpy

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
pygame.display.flip()

points = []


slider = thorpy.SliderX(100, (12, 35), "My Slider")
button = thorpy.make_button("Quit", func=thorpy.functions.quit_func)
box = thorpy.Box(elements=[slider,button])
#we regroup all elements on a menu, even if we do not launch the menu
menu = thorpy.Menu(box)
#important : set the screen as surface for all elements
for element in menu.get_population():
    element.surface = screen
#use the elements normally...
box.set_topleft((100,100))
box.blit()
box.update()


while running:
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    
    # Rendering game
    for point in points:
        pygame.draw.circle(surface = screen, color = "green", center = point, radius = 2.0)

    if len(points) > 1:
        pygame.draw.aalines(surface = screen, color = "yellow", closed=True, points=points)

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60) # limits FPS to 60

    # poll for events
    # pygame.QUIT event means the user clicked X to close your windowk 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        left_mouse_button_lock = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            left_mouse_button_lock = True
            points.append(pygame.mouse.get_pos())
        if event.type == pygame.MOUSEBUTTONUP:
            left_mouse_button_lock = False

        menu.react(event) #the menu automatically integrate your elements

  

pygame.quit()
