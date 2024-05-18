from altair import Chart
from pandas import DataFrame
import altair as alt
from altair import Tooltip, Color, Scale

def chart(df: DataFrame, x: str, y: str, target: str) -> Chart:
    """
    Creates a scatter plot using Altair with specified columns from a Pandas DataFrame.
    
    Parameters:
    df (pd.DataFrame): The DataFrame containing the data to plot.
    x (str): The column name to use for the x-axis.
    y (str): The column name to use for the y-axis.
    target (str): The column name to use for coloring the data points.
    
    Returns:
    Chart: An Altair Chart object representing the scatter plot.
    """
    
    # Check if '_id' column exists and drop it if it does
    if '_id' in df.columns:
        plot_df = df.drop('_id', axis=1)
    else:
        plot_df = df

    graph = (alt.Chart(plot_df, title=f'{y} by {x} for {target}', background='#1F1F1F', padding={'left': 50, 'top': 50, 'right': 50, 'bottom': 50}, width=450, height=450)
             .mark_circle(size=100)
             .encode(
                 x=x,
                 y=y,
                 tooltip=alt.Tooltip(plot_df.columns.to_list()),
                 color=alt.Color(f'{target}', scale=alt.Scale(scheme='teals'))
             )
             .configure_title(fontSize=18, color='teal')
             .configure_axis(labelColor='teal', titleColor='teal')
             .configure_legend(labelColor='teal', titleColor='teal'))

    return graph
