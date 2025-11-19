import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def crear_grafico_2d_plotly(xx, yy, Bx, By, titulo="Campo Magnético 2D", geometria=None):
    """
    Crea un gráfico 2D interactivo del campo magnético usando Plotly.
    
    Args:
        xx, yy: Mallas de coordenadas
        Bx, By: Componentes del campo magnético
        titulo: Título del gráfico
        geometria: dict con información de la geometría
    
    Returns:
        fig: Figura de Plotly
    """
    # Calcular magnitud del campo
    B_mag = np.sqrt(Bx**2 + By**2)
    
    # Crear figura
    fig = go.Figure()
    
    # Añadir heatmap de magnitud
    fig.add_trace(go.Heatmap(
        x=xx[0, :],
        y=yy[:, 0],
        z=B_mag,
        colorscale='Viridis',
        colorbar=dict(title='|B| (T)'),
        name='Magnitud',
        hovertemplate='x: %{x:.3f}<br>y: %{y:.3f}<br>|B|: %{z:.3e} T<extra></extra>'
    ))
    
    # Añadir vectores del campo (subsample para no saturar)
    step = max(1, len(xx) // 15)
    xx_sub = xx[::step, ::step]
    yy_sub = yy[::step, ::step]
    Bx_sub = Bx[::step, ::step]
    By_sub = By[::step, ::step]
    B_mag_sub = B_mag[::step, ::step]
    
    # Normalizar para visualización
    B_max = np.max(B_mag)
    if B_max > 0:
        scale = 0.08 * (xx.max() - xx.min())
        Bx_scaled = Bx_sub / B_max * scale
        By_scaled = By_sub / B_max * scale
    else:
        Bx_scaled = Bx_sub
        By_scaled = By_sub
    
    # Añadir quiver (vectores)
    for i in range(xx_sub.shape[0]):
        for j in range(xx_sub.shape[1]):
            x0, y0 = xx_sub[i, j], yy_sub[i, j]
            dx, dy = Bx_scaled[i, j], By_scaled[i, j]
            
            fig.add_trace(go.Scatter(
                x=[x0, x0 + dx],
                y=[y0, y0 + dy],
                mode='lines',
                line=dict(color='white', width=1.5),
                showlegend=False,
                hoverinfo='skip'
            ))
            
            # Flecha
            fig.add_trace(go.Scatter(
                x=[x0 + dx],
                y=[y0 + dy],
                mode='markers',
                marker=dict(
                    symbol='arrow',
                    size=8,
                    color='white',
                    angle=np.degrees(np.arctan2(dy, dx)),
                    angleref='previous'
                ),
                showlegend=False,
                hoverinfo='skip'
            ))
    
    # Dibujar geometría
    if geometria:
        if geometria['tipo'] in ['alambre', 'ambos']:
            L = geometria.get('L', 2)
            z_offset = geometria.get('z_offset_alambre', 0)
            # En vista 2D (XY), el alambre se ve como un punto en (0,0)
            fig.add_trace(go.Scatter(
                x=[0],
                y=[0],
                mode='markers',
                marker=dict(size=12, color='red', symbol='circle', line=dict(width=2, color='white')),
                name='Alambre',
                hovertemplate=f'Alambre (eje Z)<br>L={L} m<br>z_offset={z_offset} m<extra></extra>'
            ))
        
        if geometria['tipo'] in ['espira', 'ambos']:
            a = geometria.get('a', 0.5)
            z_offset = geometria.get('z_offset_espira', 0)
            theta = np.linspace(0, 2*np.pi, 100)
            fig.add_trace(go.Scatter(
                x=a*np.cos(theta),
                y=a*np.sin(theta),
                mode='lines',
                line=dict(color='cyan', width=3),
                name='Espira',
                hovertemplate=f'Espira<br>Radio={a} m<br>z_offset={z_offset} m<extra></extra>'
            ))
    
    # Configurar layout
    fig.update_layout(
        title=titulo,
        xaxis=dict(title='x (m)', scaleanchor='y', scaleratio=1),
        yaxis=dict(title='y (m)'),
        width=700,
        height=700,
        showlegend=True,
        hovermode='closest'
    )
    
    return fig


def crear_grafico_3d_plotly(x, y, z, Bx, By, Bz, titulo="Campo Magnético 3D", geometria=None):
    """
    Crea un gráfico 3D interactivo del campo magnético usando Plotly.
    
    Args:
        x, y, z: Coordenadas de los puntos (arrays 1D)
        Bx, By, Bz: Componentes del campo magnético
        titulo: Título del gráfico
        geometria: dict con información de la geometría
    
    Returns:
        fig: Figura de Plotly
    """
    # Calcular magnitud
    B_mag = np.sqrt(Bx**2 + By**2 + Bz**2)
    
    # Normalizar vectores para visualización
    B_max = np.max(B_mag)
    if B_max > 0:
        scale = 0.15
        Bx_norm = Bx / B_max * scale
        By_norm = By / B_max * scale
        Bz_norm = Bz / B_max * scale
    else:
        Bx_norm = Bx
        By_norm = By
        Bz_norm = Bz
    
    # Crear figura
    fig = go.Figure()
    
    # Añadir vectores usando Cone plot
    fig.add_trace(go.Cone(
        x=x, y=y, z=z,
        u=Bx_norm, v=By_norm, w=Bz_norm,
        colorscale='Viridis',
        sizemode='absolute',
        sizeref=0.3,
        colorbar=dict(title='|B| (T)'),
        cmin=0,
        cmax=B_max,
        hovertemplate='x: %{x:.2f}<br>y: %{y:.2f}<br>z: %{z:.2f}<br>|B|: %{marker.color:.3e} T<extra></extra>',
        showscale=True
    ))
    
    # Dibujar geometría
    if geometria:
        if geometria['tipo'] in ['alambre', 'ambos']:
            L = geometria.get('L', 2)
            z_offset = geometria.get('z_offset_alambre', 0)
            zs = np.linspace(-L/2 + z_offset, L/2 + z_offset, 50)
            fig.add_trace(go.Scatter3d(
                x=np.zeros_like(zs),
                y=np.zeros_like(zs),
                z=zs,
                mode='lines',
                line=dict(color='red', width=6),
                name='Alambre',
                hovertemplate=f'Alambre<br>L={L} m<extra></extra>'
            ))
        
        if geometria['tipo'] in ['espira', 'ambos']:
            a = geometria.get('a', 0.5)
            z_offset = geometria.get('z_offset_espira', 0)
            theta = np.linspace(0, 2*np.pi, 100)
            fig.add_trace(go.Scatter3d(
                x=a*np.cos(theta),
                y=a*np.sin(theta),
                z=np.full_like(theta, z_offset),
                mode='lines',
                line=dict(color='cyan', width=6),
                name='Espira',
                hovertemplate=f'Espira<br>Radio={a} m<extra></extra>'
            ))
    
    # Configurar layout
    fig.update_layout(
        title=titulo,
        scene=dict(
            xaxis=dict(title='x (m)'),
            yaxis=dict(title='y (m)'),
            zaxis=dict(title='z (m)'),
            aspectmode='cube'
        ),
        width=700,
        height=700,
        showlegend=True
    )
    
    return fig
