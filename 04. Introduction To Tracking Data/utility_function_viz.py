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
    field_color = 'mediumseagreen'
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
    ax.plot([0, 0], [-half_pitch_width, half_pitch_width], 'whitesmoke', linewidth)
    ax.scatter(0, 0, marker='o', facecolor='whitesmoke', s=20)

    ## x and y coordinates for center circle
    y = np.linspace(-1, 1, 50) * center_circle_radius
    x = np.sqrt(center_circle_radius**2 - y**2)

    ## plotting the center circle
    ax.plot(x, y, 'whitesmoke', linewidth)
    ax.plot(-x, y, 'whitesmoke', linewidth)

    ## plot each halves
    for s in signs:
        ## plotting pitch boundary
        ax.plot([-half_pitch_length, half_pitch_length], [s * half_pitch_width, s * half_pitch_width], 'whitesmoke', linewidth)
        ax.plot([s * half_pitch_length, s * half_pitch_length], [- half_pitch_width, half_pitch_width], 'whitesmoke', linewidth)

        ## plot the goal post
        ax.plot([s * half_pitch_length, s * half_pitch_length], [-goal_line_width / 2, goal_line_width / 2], 'ws', linewidth, markersize=6)

        ## plotting six yard box
        ax.plot([s * half_pitch_length, s * half_pitch_length - s * box_length], [box_width / 2, box_width / 2], 'whitesmoke', linewidth)
        ax.plot([s * half_pitch_length, s * half_pitch_length - s * box_length], [-box_width / 2, -box_width / 2], 'whitesmoke', linewidth)
        ax.plot([s * half_pitch_length - s * box_length, s * half_pitch_length - s * box_length], [box_width / 2, -box_width / 2], 'whitesmoke', linewidth)

        ## plotting penalty area
        ax.plot([s * half_pitch_length, s * half_pitch_length - s * area_length], [area_width / 2, area_width / 2], 'whitesmoke', linewidth)
        ax.plot([s * half_pitch_length, s * half_pitch_length - s * area_length], [- area_width / 2, - area_width / 2], 'whitesmoke', linewidth)
        ax.plot([s * half_pitch_length - s * area_length, s * half_pitch_length - s * area_length], [area_width / 2, - area_width / 2], 'whitesmoke', linewidth)

        ## plotting penalty spot
        ax.scatter(s * half_pitch_length - s * penalty_spot, 0, marker='o', facecolor='whitesmoke', s=20)

        ## plotting corner flag
        y = np.linspace(0,1,50) * corner_radius
        x = np.sqrt(corner_radius**2 - y**2)
        ax.plot(s * half_pitch_length - s * x, -half_pitch_width + y, 'whitesmoke', linewidth)
        ax.plot(s * half_pitch_length - s * x, half_pitch_width - y, 'whitesmoke', linewidth)

        ## plotting the D
        y = np.linspace(-1, 1, 50) * D_length
        x = np.sqrt(D_radius**2 - y**2) + D_pos
        ax.plot(s * half_pitch_length - s * x, y, 'whitesmoke', linewidth)

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
    
def shot_map(df, fig, ax):
    '''
    This function will plot the shot map for the given shot
    dataframe.
    
    Argument:
    df -- dataframe object, the dataframe passed(home or away).
    fig -- figure object.
    ax -- axis object.
    
    Returns:
    fig, ax -- figure and axis object.
    '''
    fig, ax = fig, ax

    ## iterating thorugh the shot dataframe
    for row_num, shot in df.iterrows():
        if shot['Subtype'][-5:] == '-GOAL':
            color = 'bo'
            label = 'Goal'
        else: 
            color = 'ro'
            label = 'No Goal'

        dist = 1 if shot['Period'] == 2 else -1
        ## plotting the point where the shot took place                
        plt.plot(shot['Start X'] * dist, shot['Start Y'] * dist, color, label=label)

        ## adding an arrow to see the direction of the shot
        ax.annotate("", xy=shot[['End X', 'End Y']] * dist, xytext=shot[['Start X', 'Start Y']] * dist, 
                arrowprops=dict(arrowstyle='->', color=color[0]))

    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='best', bbox_to_anchor=(0.9, 1, 0, 0), fontsize=12)

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
        dist = 1 if event['Period'] == 2 else -1
        color = (
            'bo'
            if event['Type'] == 'SHOT' and event['Subtype'][-5:] == '-GOAL'
            else 'ro'
        )

        ## plotting the events
        plt.plot(event['Start X'] * dist, event['Start Y'] * dist, color)
        ## adding arrows
        ax.annotate(
            f'{count}',
            xy=event[['End X', 'End Y']] * dist,
            xytext=event[['Start X', 'Start Y']] * dist,
            arrowprops=dict(arrowstyle='->', color=color[0]),
        )

    return fig, ax

def plot_frame(home_team_loc, away_team_loc, fig, ax, event_row=None):
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
    team_colors = ('r', 'b')
    ## red for home team and blue for away team

    dist = 1 if home_team_loc['Period'] == 2 else -1
    for team, color in zip([home_team_loc, away_team_loc], team_colors):
        x_cols = [col for col in team.keys() if col[-1] == 'X' and col != 'ball_X']
        y_cols = [col for col in team.keys() if col[-1] == 'Y' and col != 'ball_Y']

        label = 'Home Team' if color == 'r' else 'Away Team'
        ax.plot(
            team[x_cols] * dist,
            team[y_cols] * dist,
            f'{color}o',
            MarkerSize=10,
            label=label,
        )


    ax.plot(home_team_loc['ball_X'] * dist, away_team_loc['ball_Y'] * dist, 'ko', MarkerSize=6)

    if event_row is not None:
        ax.annotate('', xy=event_row[['End X', 'End Y']] * dist, 
                    xytext=event_row[['Start X', 'Start Y']] * dist,
                    arrowprops=dict(arrowstyle='->', color='m'))

    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc='best', bbox_to_anchor=(0.9, 1, 0, 0), fontsize=12)

    return fig, ax



