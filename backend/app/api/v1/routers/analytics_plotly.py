import json
import pandas as pd
import plotly.express as px
import plotly.io as pio
from fastapi import APIRouter, Response

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/rumor-trends")
async def get_rumor_trends():
    """
    Generates a Plotly trend line chart for rumor reporting over time.
    Returns the JSON representation of the figure to be natively rendered in React.
    """
    # Mock data for demonstration purposes
    df = pd.DataFrame({
        "Date": pd.date_range(start="2026-06-01", periods=30),
        "Reports": [max(5, x + (x % 5) * 10) for x in range(30)],
        "Verified Fake": [max(1, x // 2 + (x % 3) * 5) for x in range(30)]
    })
    
    fig = px.line(
        df, 
        x="Date", 
        y=["Reports", "Verified Fake"],
        title="Rumor Reports and Verifications (Last 30 Days)",
        template="plotly_dark", # Native dark mode to match UI
        labels={"value": "Count", "variable": "Metric"}
    )
    
    # Configure interactive hover options
    fig.update_layout(
        hovermode="x unified",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    
    # Return as raw JSON directly usable by react-plotly.js
    chart_json = pio.to_json(fig)
    return Response(content=chart_json, media_type="application/json")


@router.get("/hotspot-map")
async def get_hotspot_map():
    """
    Generates an interactive map layer highlighting regions with high rumor velocity.
    """
    # Mock geospatial data for India
    df = pd.DataFrame({
        "City": ["Delhi", "Mumbai", "Bangalore", "Chennai", "Kolkata"],
        "Lat": [28.6139, 19.0760, 12.9716, 13.0827, 22.5726],
        "Lon": [77.2090, 72.8777, 77.5946, 80.2707, 88.3639],
        "Severity": [85, 60, 45, 90, 30]
    })
    
    fig = px.scatter_mapbox(
        df, 
        lat="Lat", 
        lon="Lon", 
        hover_name="City",
        size="Severity",
        color="Severity",
        color_continuous_scale=px.colors.sequential.YlOrRd,
        zoom=4,
        title="Rumor Velocity Hotspots",
        mapbox_style="carto-darkmatter"
    )
    
    fig.update_layout(
        margin={"r":0,"t":40,"l":0,"b":0},
        paper_bgcolor="rgba(0,0,0,0)"
    )
    
    chart_json = pio.to_json(fig)
    return Response(content=chart_json, media_type="application/json")
