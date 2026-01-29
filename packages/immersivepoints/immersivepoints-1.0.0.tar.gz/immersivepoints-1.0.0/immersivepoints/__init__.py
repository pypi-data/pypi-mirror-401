"""
ImmersivePoints - Render point clouds inline in Jupyter notebooks.

Usage:
    import immersivePoints as ip
    ip.renderPoints(points)  # points is Nx4 (XYZI) or Nx6 (XYZRGB) numpy array
"""

import base64
import json
import numpy as np
import threading
import socket
import os
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from IPython.display import IFrame, HTML, display

# Global server state
_server = None
_server_port = None
_server_thread = None
_point_data_store = {}  # Store point data by ID for serving


# The viewer HTML template with Three.js
VIEWER_HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, user-scalable=no, minimum-scale=1.0, maximum-scale=1.0">
    <style>
        body {{ margin: 0; overflow: hidden; }}
        #info {{ 
            position: absolute; top: 10px; left: 10px; color: white; 
            font-family: sans-serif; font-size: 12px; 
            background: rgba(0,0,0,0.5); padding: 5px 10px; border-radius: 4px;
        }}
    </style>
</head>
<body>
    <div id="info">Drag to rotate, scroll to zoom, right-click to pan</div>
    <script>
        window.POINT_DATA = "{point_data}";
        window.POINT_TYPE = "{point_type}";
        window.POINT_SIZE = {point_size};
        window.BACKGROUND_COLOR = {background_color};
        window.SHOW_AXES = {show_axes};
    </script>
    <script type="module">
        import * as THREE from "https://cdn.jsdelivr.net/npm/three@0.121.1/build/three.module.js";
        import {{ OrbitControls }} from "https://cdn.jsdelivr.net/npm/three@0.121.1/examples/jsm/controls/OrbitControls.js";

        const pointData = window.POINT_DATA;
        const pointType = window.POINT_TYPE;
        const pointSize = window.POINT_SIZE;
        const backgroundColor = window.BACKGROUND_COLOR;
        const showAxes = window.SHOW_AXES;

        const scene = new THREE.Scene();
        scene.background = new THREE.Color(backgroundColor);

        const camera = new THREE.PerspectiveCamera(60, window.innerWidth / window.innerHeight, 0.1, 1000);
        camera.position.set(0, 5, 20);

        const renderer = new THREE.WebGLRenderer({{ antialias: true }});
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.setSize(window.innerWidth, window.innerHeight);
        document.body.appendChild(renderer.domElement);

        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true;
        controls.dampingFactor = 0.05;

        function base64ToArrayBuffer(base64) {{
            const binaryString = atob(base64);
            const bytes = new Uint8Array(binaryString.length);
            for (let i = 0; i < binaryString.length; i++) {{
                bytes[i] = binaryString.charCodeAt(i);
            }}
            return bytes.buffer;
        }}

        function loadPoints() {{
            const buffer = base64ToArrayBuffer(pointData);
            const dataView = new DataView(buffer);
            const numFloats = buffer.byteLength / 4;
            const floats = new Float32Array(numFloats);
            
            for (let i = 0; i < numFloats; i++) {{
                floats[i] = dataView.getFloat32(i * 4, false);
            }}

            const pointsPerRow = pointType === "XYZRGB" ? 6 : 4;
            const numPoints = Math.floor(numFloats / pointsPerRow);
            
            const positions = new Float32Array(numPoints * 3);
            const colors = new Float32Array(numPoints * 3);
            
            for (let i = 0; i < numPoints; i++) {{
                const idx = i * pointsPerRow;
                positions[i * 3] = floats[idx];
                positions[i * 3 + 1] = floats[idx + 1];
                positions[i * 3 + 2] = floats[idx + 2];
                
                if (pointType === "XYZRGB") {{
                    colors[i * 3] = floats[idx + 3];
                    colors[i * 3 + 1] = floats[idx + 4];
                    colors[i * 3 + 2] = floats[idx + 5];
                }} else {{
                    const hue = floats[idx + 3];
                    const color = new THREE.Color();
                    color.setHSL(hue, 1.0, 0.5);
                    colors[i * 3] = color.r;
                    colors[i * 3 + 1] = color.g;
                    colors[i * 3 + 2] = color.b;
                }}
            }}

            const geometry = new THREE.BufferGeometry();
            geometry.setAttribute("position", new THREE.BufferAttribute(positions, 3));
            geometry.setAttribute("color", new THREE.BufferAttribute(colors, 3));
            geometry.computeBoundingSphere();

            const material = new THREE.PointsMaterial({{
                size: pointSize,
                vertexColors: true,
                sizeAttenuation: true
            }});

            const points = new THREE.Points(geometry, material);
            scene.add(points);

            const center = geometry.boundingSphere.center;
            const radius = geometry.boundingSphere.radius;
            camera.position.set(center.x, center.y + radius * 0.5, center.z + radius * 2);
            controls.target.copy(center);
            controls.update();
        }}

        loadPoints();

        if (showAxes) {{
            const axesHelper = new THREE.AxesHelper(5);
            scene.add(axesHelper);
        }}

        function animate() {{
            requestAnimationFrame(animate);
            controls.update();
            renderer.render(scene, camera);
        }}
        animate();

        window.addEventListener("resize", () => {{
            camera.aspect = window.innerWidth / window.innerHeight;
            camera.updateProjectionMatrix();
            renderer.setSize(window.innerWidth, window.innerHeight);
        }});
    </script>
</body>
</html>'''


class PointCloudHandler(BaseHTTPRequestHandler):
    """HTTP handler for serving point cloud viewers."""
    
    def do_GET(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        
        if parsed.path == '/viewer' and 'id' in query:
            data_id = query['id'][0]
            if data_id in _point_data_store:
                data = _point_data_store[data_id]
                html = VIEWER_HTML_TEMPLATE.format(
                    point_data=data['base64'],
                    point_type=data['point_type'],
                    point_size=data['point_size'],
                    background_color=data['background_color'],
                    show_axes='true' if data['show_axes'] else 'false'
                )
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(html.encode('utf-8'))
                return
        
        # 404 for unknown paths
        self.send_response(404)
        self.end_headers()
    
    def log_message(self, format, *args):
        pass  # Suppress logging


def _find_free_port():
    """Find an available port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]


def _ensure_server():
    """Ensure the embedded HTTP server is running."""
    global _server, _server_port, _server_thread
    
    if _server is not None:
        return _server_port
    
    _server_port = _find_free_port()
    _server = HTTPServer(('127.0.0.1', _server_port), PointCloudHandler)
    
    _server_thread = threading.Thread(target=_server.serve_forever, daemon=True)
    _server_thread.start()
    
    return _server_port


def _numpy_to_base64(points: np.ndarray) -> str:
    """Convert numpy array to base64 string in the format expected by the viewer."""
    points_float32 = np.asarray(points, dtype=np.float32)
    # Byteswap for big-endian format (as expected by the viewer)
    points_bytes = points_float32.byteswap().tobytes()
    return base64.b64encode(points_bytes).decode('ascii')


def renderPoints(
    points: np.ndarray,
    point_type: str = None,
    point_size: float = 0.04,
    width: int = 800,
    height: int = 600,
    background_color: int = 0x2d4aa8,
    show_axes: bool = True
):
    """
    Render a point cloud inline in a Jupyter notebook using a local server.
    
    Parameters
    ----------
    points : np.ndarray
        Point cloud data. Should be Nx4 for XYZI format (x, y, z, hue) 
        or Nx6 for XYZRGB format (x, y, z, r, g, b).
        - For XYZI: hue should be 0.0-1.0
        - For XYZRGB: r, g, b should be 0.0-1.0
    point_type : str, optional
        'XYZI' or 'XYZRGB'. Auto-detected from array shape if not specified.
    point_size : float, optional
        Size of each point. Default is 0.04.
    width : int, optional
        Width of the viewer in pixels. Default is 800.
    height : int, optional
        Height of the viewer in pixels. Default is 600.
    background_color : int, optional
        Background color as hex integer. Default is 0x2d4aa8 (blue).
    show_axes : bool, optional
        Whether to show XYZ axes. Default is True.
    
    Returns
    -------
    IPython.display.IFrame
        An IFrame that renders the point cloud inline via local server.
    
    Examples
    --------
    >>> import numpy as np
    >>> import immersivePoints as ip
    >>> 
    >>> # Create random point cloud with XYZI format
    >>> points = np.random.randn(1000, 4).astype(np.float32)
    >>> points[:, 3] = np.clip(points[:, 3], 0, 1)  # Hue 0-1
    >>> ip.renderPoints(points)
    >>> 
    >>> # Create point cloud with RGB colors
    >>> points_rgb = np.random.randn(1000, 6).astype(np.float32)
    >>> points_rgb[:, 3:6] = np.clip(points_rgb[:, 3:6], 0, 1)  # RGB 0-1
    >>> ip.renderPoints(points_rgb, point_type='XYZRGB')
    """
    points = np.asarray(points)
    
    # Auto-detect point type from shape
    if point_type is None:
        if points.shape[1] == 6:
            point_type = 'XYZRGB'
        elif points.shape[1] == 4:
            point_type = 'XYZI'
        elif points.shape[1] == 3:
            # Add default intensity/hue
            points = np.column_stack([points, np.ones(len(points)) * 0.5])
            point_type = 'XYZI'
        else:
            raise ValueError(f"Points array should have 3, 4, or 6 columns, got {points.shape[1]}")
    
    # Ensure server is running
    port = _ensure_server()
    
    # Convert to base64 and store
    point_data_b64 = _numpy_to_base64(points)
    data_id = str(uuid.uuid4())
    
    _point_data_store[data_id] = {
        'base64': point_data_b64,
        'point_type': point_type,
        'point_size': point_size,
        'background_color': background_color,
        'show_axes': show_axes
    }
    
    # Create URL to the viewer
    viewer_url = f"http://127.0.0.1:{port}/viewer?id={data_id}"
    
    return IFrame(viewer_url, width=width, height=height)


def renderPointsVR(
    points: np.ndarray,
    point_type: str = None,
    point_size: float = 0.04
) -> str:
    """
    Generate a URL to view the point cloud in VR on immersivepoints.com.
    
    Parameters
    ----------
    points : np.ndarray
        Point cloud data. Should be Nx4 for XYZI or Nx6 for XYZRGB.
    point_type : str, optional
        'XYZI' or 'XYZRGB'. Auto-detected from array shape if not specified.
    point_size : float, optional
        Size of each point. Default is 0.04.
    
    Returns
    -------
    str
        URL to view the point cloud in VR.
    """
    points = np.asarray(points)
    
    # Auto-detect point type from shape
    if point_type is None:
        if points.shape[1] == 6:
            point_type = 'XYZRGB'
        elif points.shape[1] == 4:
            point_type = 'XYZI'
        elif points.shape[1] == 3:
            points = np.column_stack([points, np.ones(len(points)) * 0.5])
            point_type = 'XYZI'
        else:
            raise ValueError(f"Points array should have 3, 4, or 6 columns, got {points.shape[1]}")
    
    # Convert to base64
    point_data_b64 = _numpy_to_base64(points)
    
    # Create JSON config
    config = {
        "points": [{
            "source": "base64",
            "base64": point_data_b64,
            "type": point_type,
            "pointSize": point_size
        }]
    }
    
    # Encode config as base64
    config_b64 = base64.urlsafe_b64encode(json.dumps(config).encode()).decode('ascii')
    
    url = f"https://immersivepoints.com/oculus.html?jsonb64={config_b64}"
    return url


def showVR(
    points: np.ndarray,
    point_type: str = None,
    point_size: float = 0.04
):
    """
    Display a clickable link to view the point cloud in VR.
    
    Parameters
    ----------
    points : np.ndarray
        Point cloud data. Should be Nx4 for XYZI or Nx6 for XYZRGB.
    point_type : str, optional
        'XYZI' or 'XYZRGB'. Auto-detected from array shape if not specified.
    point_size : float, optional
        Size of each point. Default is 0.04.
    """
    url = renderPointsVR(points, point_type, point_size)
    display(HTML(f'<a href="{url}" target="_blank">View in VR</a>'))


def stop_server():
    """Stop the embedded HTTP server."""
    global _server, _server_port, _server_thread
    if _server is not None:
        _server.shutdown()
        _server = None
        _server_port = None
        _server_thread = None


def clear_data():
    """Clear all stored point cloud data."""
    global _point_data_store
    _point_data_store = {}


# Convenience aliases
render = renderPoints
show = renderPoints
