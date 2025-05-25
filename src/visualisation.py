import plotly.graph_objects as go
import numpy as np

def create_gain_plot(gain_values, is_pay_early_better, favorable_scenarios):
    strategy = "Paying Early" if is_pay_early_better else "Keeping Loan"
    min_gain = np.floor(min(gain_values) / 2500) * 2500
    max_gain = np.ceil(max(gain_values) / 2500) * 2500
    
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=gain_values,
        histnorm='probability',
        opacity=0.7,
        marker_color='#00CC96',
        name=strategy,
        xbins=dict(
            start=min_gain,
            end=max_gain,
            size=2500
        )
    ))
    
    fig.update_layout(
        title=dict(
            text=f'Expected Financial Gain from {strategy}',
            x=0.5,
            xanchor='center'
        ),
        xaxis_title='Expected Gain (£)',
        yaxis_title='Probability (%)',
        font=dict(size=14),
        showlegend=False,
        hovermode='x unified',
        title_font_size=20,
        height=450,
        yaxis=dict(
            tickformat='.0%'
        ),
        margin=dict(t=90, l=50, r=50, b=50)
    )
    
    fig.add_vline(
        x=0,
        line_dash='dot',
        line_color='black',
        annotation_text='Break-even point',
        annotation_position='top',
        annotation=dict(
            yshift=10,
            xshift=-10,
            font=dict(size=14),
            xanchor='right'
        )
    )
    
    mean_gain = np.mean(gain_values)
    fig.add_vline(
        x=mean_gain,
        line_dash='dash',
        line_color='black',
        annotation_text=f'Average gain: £{mean_gain:,.0f}',
        annotation_position='top',
        annotation=dict(
            yshift=10,
            xshift=10,
            font=dict(size=14),
            xanchor='left'
        )
    )
    
    message = f"In {favorable_scenarios:.1%} of<br>scenarios you will gain<br>by"
    message += " paying off your<br>student loan early" if is_pay_early_better else " keeping your loan<br>and investing"
    
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.98, y=0.98,
        showarrow=False,
        font=dict(size=14),
        bgcolor="rgba(255, 255, 255, 0.8)",
        bordercolor="black",
        borderwidth=1,
        borderpad=4,
        align="center",
        width=160
    )
    
    return fig

def create_distribution_plot(payments_arr, investments_arr, current_loan):
    min_val = np.floor(min(min(payments_arr), min(investments_arr)) / 2500) * 2500
    max_val = np.ceil(max(max(payments_arr), max(investments_arr)) / 2500) * 2500
    
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=payments_arr,
        name='Loan Repayments',
        histnorm='probability',
        opacity=0.7,
        marker_color='#FF2B2B',
        xbins=dict(
            start=min_val,
            end=max_val,
            size=2500
        )
    ))
    
    fig.add_trace(go.Histogram(
        x=investments_arr,
        name='Investment Returns',
        histnorm='probability',
        opacity=0.7,
        marker_color='#0068C9',
        xbins=dict(
            start=min_val,
            end=max_val,
            size=2500
        )
    ))
    
    fig.update_layout(
        title=dict(
            text='Distribution of Total Values',
            x=0.5,
            xanchor='center'
        ),
        xaxis_title='Total Value (£)',
        yaxis_title='Probability (%)',
        font=dict(size=14),
        showlegend=True,
        hovermode='x unified',
        title_font_size=20,
        height=450,
        yaxis=dict(
            tickformat='.0%'
        ),
        margin=dict(t=90, l=50, r=50, b=50),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99
        ),
        barmode='overlay'
    )
    
    fig.add_vline(
        x=current_loan,
        line_dash='dot',
        line_color='black',
        annotation_text=f'Original Loan: £{current_loan:,}',
        annotation_position='top',
        annotation=dict(
            yshift=10,
            font=dict(size=14)
        )
    )
    
    return fig 
