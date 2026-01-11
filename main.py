import fantas
from fantas import uimanager as u

import pygame

if fantas.PLATFORM == "Darwin":
    u.dpi_ratio = 2
else:
    u.dpi_ratio = 1

u.init(
    "Fantasy Snapshot",
    (1920, 1080),
    resizable=True,
    allow_high_dpi=True,
)

u.root = fantas.Root(pygame.Color("black"))

u.mainloop()
