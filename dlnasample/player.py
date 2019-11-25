import pyglet
#pyglet.lib.load_library('avbin')
#pyglet.have_avbin=True

window = pyglet.window.Window(resizable=True)

@window.event
def on_draw():
    player.get_texture().blit(0, 0)

if __name__ == "__main__":
    player = pyglet.media.Player()
    source = pyglet.media.load("E:/xwdsh.mp4")
    player.queue(source)
    player.play()

    pyglet.app.run()