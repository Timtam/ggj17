from ..commons import *

class Control(object):
    def __init__(self, rect):
        self.rect = rect
        self.ui = get_common().get_ui()
        self.surface = None
        self.child_controls = []

    def add_child_control(self, control, center = False):
        self.transform_child_control(control, center)
        self.child_controls.append(control)

    def reset_child_controls(self):
        for control in self.child_controls:
            control.reset_child_controls()
            control.rect = control.original_rect
            control.transform_child_controls()
    def transform_child_control(self, control, center):
        control.reset_child_controls()
        control.original_rect = control.rect.copy()
        control.relative_center = center
        if center:
            control.rect.center = self.rect.center
        else:
            # transform relative to absolute coordinates
            control.rect.x += self.rect.x
            control.rect.y += self.rect.y
        control.transform_child_controls()
    def transform_child_controls(self):
        for control in self.child_controls:
            self.transform_child_control(control, control.relative_center)

    def _update(self):
        pass
    def update(self):
        self._update()
        for control in self.child_controls:
            control.update()

    def _draw(self, screen):
        pass
    def draw(self, screen):
        if self.surface != None:
            screen.blit(self.surface, self.rect)
        self._draw(screen)
        for control in self.child_controls:
            control.draw(screen)
