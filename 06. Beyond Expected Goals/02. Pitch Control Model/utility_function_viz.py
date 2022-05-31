"""
Created on Sat Apr 18 20:09:17 2020

@author: slothfulwave612
This Python module will contain function for visualization.

Module Used(2):
---------------
1. matplotlib -- plotting library in Python.
2. numpy -- numerical computing library.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def plot_pitch():
    '''
    Function to plot a football pitch, here we have
    used all the dimensions in meters by converting 
    from yards.
    
    Returns:
    fig, ax -- figure and axis object
    '''

    ## creating a figure
    fig, ax = plt.subplots(figsize=(12,8))

    ## defining some of the parameters, will be used while plotting
    field_dims = (105, 68)
    field_color = 'whitesmoke'
    linewidth = 2

    ## field dimensions in meters
    border_dims = (3, 3)                     ## border around the field of 3x3 meters
    meters_per_yard = 0.9144                 ## unit conversion from yards to meters
    half_pitch_length = field_dims[0] / 2    ## length of half pitch
    half_pitch_width = field_dims[1] / 2     ## width of half pitch
    signs = [-1, 1]                          ## to plot pitch taking origin as center point

    ## Football field dimensions are typically defined in yards, so converting them to meters
    goal_line_width = 8 * meters_per_yard
    box_width = 20 * meters_per_yard
    box_length = 6 * meters_per_yard
    area_width = 44 * meters_per_yard
    area_length = 18 * meters_per_yard
    penalty_spot = 12 * meters_per_yard
    corner_radius = meters_per_yard
    D_length = 8 * meters_per_yard
    D_radius = 10 * meters_per_yard
    D_pos = 12 * meters_per_yard
    center_circle_radius = 10 * meters_per_yard

    ## setting the background color to 'mediumseagreen'
    ax.set_facecolor(field_color)

    ## plot the half way line and the center circle
    ax.plot([0, 0], [-half_pitch_width, half_pitch_width], 'black', linewidth)
    ax.scatter(0, 0, marker='o', facecolor='black', s=20)

    ## x and y coordinates for center circle
    y = np.linspace(-1, 1, 50) * center_circle_radius
    x = np.sqrt(center_circle_radius**2 - y**2)

    ## plotting the center circle
    ax.plot(x, y, 'black', linewidth)
    ax.plot(-x, y, 'black', linewidth)

    ## plot each halves
    for s in signs:
        ## plotting pitch boundary
        ax.plot([-half_pitch_length, half_pitch_length], [s * half_pitch_width, s * half_pitch_width], 'black', linewidth)
        ax.plot([s * half_pitch_length, s * half_pitch_length], [- half_pitch_width, half_pitch_width], 'black', linewidth)

        ## plot the goal post
        ax.plot([s * half_pitch_length, s * half_pitch_length], [-goal_line_width / 2, goal_line_width / 2], 'ks', linewidth, markersize=6)

        ## plotting six yard box
        ax.plot([s * half_pitch_length, s * half_pitch_length - s * box_length], [box_width / 2, box_width / 2], 'black', linewidth)
        ax.plot([s * half_pitch_length, s * half_pitch_length - s * box_length], [-box_width / 2, -box_width / 2], 'black', linewidth)
        ax.plot([s * half_pitch_length - s * box_length, s * half_pitch_length - s * box_length], [box_width / 2, -box_width / 2], 'black', linewidth)

        ## plotting penalty area
        ax.plot([s * half_pitch_length, s * half_pitch_length - s * area_length], [area_width / 2, area_width / 2], 'black', linewidth)
        ax.plot([s * half_pitch_length, s * half_pitch_length - s * area_length], [- area_width / 2, - area_width / 2], 'black', linewidth)
        ax.plot([s * half_pitch_length - s * area_length, s * half_pitch_length - s * area_length], [area_width / 2, - area_width / 2], 'black', linewidth)

        ## plotting penalty spot
        ax.scatter(s * half_pitch_length - s * penalty_spot, 0, marker='o', facecolor='black', s=20)

        ## plotting corner flag
        y = np.linspace(0,1,50) * corner_radius
        x = np.sqrt(corner_radius**2 - y**2)
        ax.plot(s * half_pitch_length - s * x, -half_pitch_width + y, 'black', linewidth)
        ax.plot(s * half_pitch_length - s * x, half_pitch_width - y, 'black', linewidth)

        ## plotting the D
        y = np.linspace(-1, 1, 50) * D_length
        x = np.sqrt(D_radius**2 - y**2) + D_pos
        ax.plot(s * half_pitch_length - s * x, y, 'black', linewidth)

    ## removing the ticks and the axis labels
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.set_xticks([])
    ax.set_yticks([])

    ## setting the axis limits
    x_max = (field_dims[0] / 2) + border_dims[0]
    y_max = (field_dims[1] / 2) + border_dims[0]
    ax.set_xlim([-x_max, x_max])
    ax.set_ylim([-y_max, y_max])
    ax.set_axisbelow(True)

    return fig, ax
    
    
def plot_events(df, fig, ax):
    '''
    Function to plot events.
    
    Arguments:
    df -- dataframe object, the dataframe passed
    fig -- figure object
    ax -- axis object
    
    Returns:
    fig -- figure object
    ax -- axis object
    '''
    for count, (row_num, event) in enumerate(df.iterrows(), start=1):
        ## iterating through each row 

        color = (
            'bo'
            if event['Type'] == 'SHOT' and event['Subtype'][-5:] == '-GOAL'
            else 'ro'
        )

        ## plotting the events
        ax.plot(event['Start X'], event['Start Y'], color)
        ## adding arrows
        ax.annotate(
            f'{count}',
            xy=event[['End X', 'End Y']],
            xytext=event[['Start X', 'Start Y']],
            arrowprops=dict(arrowstyle='->', color=color[0]),
        )

    return fig, ax

def plot_frame(home_team_loc, away_team_loc, fig, ax):
    '''
    Function will plot a frame for all 11 players at the pitch at 
    any given time.
    
    Arguments:
    home_team_loc -- row for home team frame.
    away_team_loc -- row for away team frame.
    fig, ax -- figure and axis object.
    event_row -- row when particular event has occurred.
    
    Retrns:
    fig, ax -- figure and axis object.
    '''    
    colors = ('r', 'b')
    ## red color for home team and blue for away team

    for team, color in zip([home_team_loc, away_team_loc], colors):
        x_cols = [cols for cols in team.keys() if cols[-1] == 'X' and cols[:4] != 'ball']
        y_cols = [cols for cols in team.keys() if cols[-1] == 'Y' and cols[:4] != 'ball']

        ## plotting players
        ax.plot(team[x_cols], team[y_cols], f'{color}o', MarkerSize=10, alpha=0.7)

        vx_cols = [f'{cols[:-2]}_vx' for cols in x_cols]
        vy_cols = [f'{cols[:-2]}_vy' for cols in y_cols]

        ## plotting velocity vectors
        ax.quiver(team[x_cols], team[y_cols], team[vx_cols], team[vy_cols], color=color, 
                  scale_units='inches', scale=10., width=0.0015, 
                  headlength=5, headwidth=3, alpha=0.7)

    ## plotting ball
    ax.plot(team['ball_X'], team['ball_Y'], 'ko', alpha=0.7)

    return fig, ax
    
def save_match_clip(home_team, away_team, fname, fpath, fps=25, colors=('r', 'b')):
    '''
    Function to create and save a match clip.
    
    Arguments:
    home_team -- dataframe object, tracking data for home team.
    away_team -- dataframe object, tracking data for away team.
    fname -- str, video name.
    fpath -- str, path where the video will be saved.
    fps -- int, frames per second.
    colors -- tuple, having color values for home and away teams
    '''
    ## check if the indices are matched for both the dataframe
    assert np.all(home_team.index == away_team.index), "Home and away team index must be the same."

    ## field dimensions
    field_dims = (105, 68)

    ## getting the starting index
    index = home_team.index    

    ## figure and movie settings
    fig, ax = plot_pitch()
    ffmpeg = animation.writers['ffmpeg']
    writer = ffmpeg(fps=fps)
    fname = f'{fpath}/{fname}.mp4'

    print('Generating Moive...', end='')

    ## create the clip and save it
    with writer.saving(fig, fname, dpi=100):
        for i in index:
            fig_obj = []
            ## empty list which will contain axis object 
            ## so to delete them after each frame

            for team, color in zip([home_team.loc[i], away_team.loc[i]], colors):
                x_cols = [cols for cols in team.keys() if cols[-1] == 'X' and cols != 'ball_X']
                y_cols = [cols for cols in team.keys() if cols[-1] == 'Y' and cols != 'ball_Y']

                ## plotting player
                (objs,) = ax.plot(
                    team[x_cols],
                    team[y_cols],
                    f'{color}o',
                    MarkerSize=10,
                    alpha=0.7,
                )

                fig_obj.append(objs)

                vx_cols = [f'{cols[:-2]}_vx' for cols in x_cols]
                vy_cols = [f'{cols[:-2]}_vy' for cols in y_cols]

                ## plotting velocity vectors
                objs = ax.quiver(team[x_cols], team[y_cols], team[vx_cols], team[vy_cols],
                                  scale_units='inches', scale=10., width=0.0015, 
                                  headlength=5, headwidth=3, alpha=0.7)
                fig_obj.append(objs)

            ## plotting the ball
            objs, = ax.plot(team['ball_X'], team['ball_Y'], 'ko', MarkerSize=7, alpha=0.5)
            fig_obj.append(objs)

            ## include match time
            frame_minus = int(team['Time [s]'] / 60)
            frame_secs = (team['Time [s]'] / 60 - frame_minus) * 60
            timestring = '%d: %1.2f' % (frame_minus, frame_secs)
            objs = plt.text(-2.5, field_dims[1] / 2, timestring, fontsize=15)
            fig_obj.append(objs)

            writer.grab_frame()

            ## delete all figure object
            for obj in fig_obj:
                obj.remove()

    print('done')
    plt.clf()
    plt.close(fig)
            
