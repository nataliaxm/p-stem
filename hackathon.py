"""
"""
import pygame

import sys

class Hacking:
    answers: list[str]
    screen: pygame.Surface
    clock: pygame.time.Clock
    questions

    def __init__(self) -> None:
        self.answers = []
        questions = (
            ["Are you interested in academic RSOs?", 
            "Are you interested in Cultural or Identity-Based RSOs?",
            "Are you interested in Sports & Recreation?",
            ""
            
            
            ]
        )
        pygame.init()

        pygame.display.set_caption("RSO Finder")
        self.screen = pygame.display.set_mode((600, 600))
        self.clock = pygame.time.Clock()
        self.run_event_loop()
        

    def run_event_loop():
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                elif event.type == pygame.MOUSEBUTTONUP:
                    return 0
        self.draw_screen()
        self.clock.tick(24)

    def draw_screen(self) -> None:
        self.surface.fill(255, 128, 128)
        pygame.display.update()

if __name__ == "__main__":
    Hacking()
            

            
        