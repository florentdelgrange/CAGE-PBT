import numpy as np
import matplotlib.pyplot as plt


class clicker_class(object):
    def __init__(self, ax, pix_err=1, stepx=100, stepy=1e-2*2):
        self.ax = ax
        self.canvas = ax.get_figure().canvas
        self.cid = None
        self.pt_lst = []
        self.pt_plot = ax.plot([], [], markersize=2, marker='o', color='r',
                               alpha=0.4,
                               linestyle='none', zorder=5)[0]
        self.pix_err = pix_err
        self.connect_sf()
        self.points_list = []
        self.stepx=stepx
        self.stepy=stepy

    def set_visible(self, visible):
        '''sets if the curves are visible '''
        self.pt_plot.set_visible(visible)

    def clear(self):
        '''Clears the points'''
        self.pt_lst = []
        self.redraw()

    def connect_sf(self):
        if self.cid is None:
            self.cid = self.canvas.mpl_connect('button_press_event',
                                               self.click_event)

    def disconnect_sf(self):
        if self.cid is not None:
            self.canvas.mpl_disconnect(self.cid)
            self.cid = None

    def click_event(self, event):
        ''' Extracts locations from the user'''
        if event.key == 'shift':
            self.pt_lst = []
            return
        if event.xdata is None or event.ydata is None:
            return
        if event.button == 1:
            self.pt_lst.append((event.xdata, event.ydata))
            self.points_list.append(
                self.ax.annotate('%1.f' % event.xdata,
                    xy=(event.xdata, event.ydata),
                    xytext=(event.xdata + self.stepx, event.ydata - self.stepy),
                    fontsize=7,
                    arrowprops=dict(arrowstyle='-', alpha=0.5),
                )
            )
            #self.canvas.draw()

        elif event.button == 3:
            self.remove_pt((event.xdata, event.ydata))
        self.redraw()

    def remove_pt(self, loc):
        if len(self.pt_lst) > 0:
            self.pt_lst.pop(np.argmin(map(lambda x:
                                          np.sqrt((x[0] - loc[0]) ** 2 +
                                                  (x[1] - loc[1]) ** 2),
                                          self.pt_lst)))
            self.points_list.pop(np.argmin(map(lambda x:
                                          np.sqrt((x[0] - loc[0]) ** 2 +
                                                  (x[1] - loc[1]) ** 2),
                                          self.points_list))).remove()

    def redraw(self):
        if len(self.pt_lst) > 0:
            x, y = zip(*self.pt_lst)
        else:
            x, y = [], []
        self.pt_plot.set_xdata(x)
        self.pt_plot.set_ydata(y)

        self.canvas.draw()

    def return_points(self):
        '''Returns the clicked points in the format the rest of the
        code expects'''
        return np.vstack(self.pt_lst).T
