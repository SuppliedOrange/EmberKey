def minimize(window):
    """
    Fixed PySimpleGUI's minimize method to support Windows - Dhruv
    """
    window.TKroot.update_idletasks()  # call all pending tkinter tasks (some of you Mac users may need to disable this and the line below)
    window.TKroot.wm_overrideredirect(False) #to let window manager perform functions
    if not window._is_window_created('tried Window.minimize'):
        return
    #self.TKroot.state('withdrawn')  # This works as an alternate but does not provide a taskbar icon
    window.TKroot.state('iconic')
    window.maximized = False