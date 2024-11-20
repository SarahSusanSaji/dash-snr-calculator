import dash
from dash import dcc, html, Input, Output
import plotly.graph_objects as go
import math

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("SNR Calculator", style={'textAlign': 'center'}),
    html.Div([
        html.Label("Star Signal (N*):"),
        dcc.Input(id='star-signal', type='number', placeholder="Enter N* (e/sec)", value=100, style={'marginRight': '10px'}),
        html.Label("Exposure Time (t):"),
        dcc.Input(id='exposure-time', type='number', placeholder="Enter t (seconds)", value=300, style={'marginRight': '10px'}),
        html.Label("Sky Brightness (S):"),
        dcc.Input(id='sky-brightness', type='number', placeholder="Enter S (e/sec/pixel)", value=0.2, style={'marginRight': '10px'}),
        html.Label("Number of Pixels (p):"),
        dcc.Input(id='num-pixels', type='number', placeholder="Enter p", value=20, style={'marginRight': '10px'}),
        html.Label("Read Noise (R):"),
        dcc.Input(id='read-noise', type='number', placeholder="Enter R (e)", value=5, style={'marginRight': '10px'}),
    ], style={'marginBottom': '20px'}),
    html.Button("Update Plot", id='update-plot-btn', n_clicks=0, style={'marginTop': '10px'}),
    dcc.Graph(id='snr-plot', style={'marginTop': '20px'}),
    html.Div(id='snr-output', style={'marginTop': '20px', 'fontSize': '18px', 'textAlign': 'center'})
])

# Callback to calculate and update the plot
@app.callback(
    [Output('snr-plot', 'figure'),
     Output('snr-output', 'children')],
    Input('update-plot-btn', 'n_clicks'),
    [
        Input('star-signal', 'value'),
        Input('exposure-time', 'value'),
        Input('sky-brightness', 'value'),
        Input('num-pixels', 'value'),
        Input('read-noise', 'value')
    ]
)
def update_plot(n_clicks, star_signal, exposure_time, sky_brightness, num_pixels, read_noise):
    if n_clicks > 0:
        # Check if inputs are valid
        if None in (star_signal, exposure_time, sky_brightness, num_pixels, read_noise):
            return {}, "Please fill in all fields."
        
        try:
            # Create an array of exposure times for plotting
            exposure_times = [t for t in range(10, int(exposure_time) + 1, 10)]
            snr_values = []

            # SNR for each exposure time
            for t in exposure_times:
                signal_star = star_signal * t
                noise_star = math.sqrt(signal_star)
                noise_sky = math.sqrt(num_pixels * sky_brightness * t)
                noise_read = math.sqrt(num_pixels) * read_noise
                total_noise = math.sqrt(noise_star**2 + noise_sky**2 + noise_read**2)
                snr = signal_star / total_noise
                snr_values.append(snr)
         
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=exposure_times, y=snr_values, mode='lines+markers', name='SNR'))
            fig.update_layout(
                title="SNR vs Exposure Time",
                xaxis_title="Exposure Time (seconds)",
                yaxis_title="Signal-to-Noise Ratio (SNR)",
                template="plotly_white"
            )

            # Final SNR for the given exposure time
            signal_star = star_signal * exposure_time
            noise_star = math.sqrt(signal_star)
            noise_sky = math.sqrt(num_pixels * sky_brightness * exposure_time)
            noise_read = math.sqrt(num_pixels) * read_noise
            total_noise = math.sqrt(noise_star**2 + noise_sky**2 + noise_read**2)
            final_snr = signal_star / total_noise

            return fig, f"The calculated Signal-to-Noise Ratio (SNR) for t = {exposure_time}s is: {final_snr:.2f}"
        
        except Exception as e:
            return {}, f"Error in calculation: {str(e)}"
    
    return {}, "Enter values and click Update Plot."

if __name__ == '__main__':
    app.run_server(debug=True)
