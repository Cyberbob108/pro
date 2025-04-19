class UndoStack:
    def __init__(self):
        self.stack = []        # History of images
        self.redo_stack = []   # Redo buffer

    def push(self, image):
        if image:
            self.stack.append(image.copy())
            self.redo_stack.clear()  # Reset redo history after new action

    def undo(self):
        if len(self.stack) > 1:
            self.redo_stack.append(self.stack.pop())
        return self.stack[-1] if self.stack else None

    def redo(self):
        if self.redo_stack:
            self.stack.append(self.redo_stack.pop())
        return self.stack[-1] if self.stack else None

    def get_current(self):
        return self.stack[-1] if self.stack else None
