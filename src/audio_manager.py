"""Safe audio loading helpers."""
def load_sound(pygame, path, volume=1.0):
    try:
        sound = pygame.mixer.Sound(path); sound.set_volume(volume); return sound
    except (pygame.error, OSError):
        return None
