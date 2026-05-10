"""
pygame implementation

"""
import pygame

import sys

class Hacking:
    answers: list[bool | String]
    screen: pygame.Surface
    clock: pygame.time.Clock
    questions: list[str]
    academic_questions: list[str]

    yes_button = pygame.Rect(150, 250, 100, 50)
    no_button = pygame.Rect(350, 250, 100, 50)
    def __init__(self) -> None:
        self.answers = []
        questions = (
            ["Are you interested in academic RSOs?", 
            "Are you interested in Cultural or Identity-Based RSOs?",
            "Are you interested in Sports & Recreation?",
            "Are you interested in Art, Media, or Entertainment?",
            "Are you interested in Community Service or Activism?",
            "Are you interested in Student Government?",
            "Are you interested in Spiritual Groups?"
            ]
        )
        academic_questions = (
            ["What is your major affiliation?",
            "Are you Pre-Med?",
            "Are you Pre-Law?",
            "Are you interested in tech?"
            ]
        )
        cultural_questions = (
            ["What is your cultural affiliation?",
            "Do you have another cultural affiliation?",
            "Do you speak/want to speak any languages?"
            ]
        )
        sports_questions = (
            ["Are you interested in any of these sports?"]
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
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    print(f"Mouse clicked at {event.pos}")
                    if yes_button.collidepoint(event.pos):
                        answers.append(True)
                    elif no_button.collidepoint(event.pos):
                        answers.append(False)
                    
        self.draw_screen()
        self.clock.tick(24)

    def draw_screen(self) -> None:
        self.surface.fill(255, 128, 128)
        pygame.display.update()

if __name__ == "__main__":
    Hacking()
            

            
        